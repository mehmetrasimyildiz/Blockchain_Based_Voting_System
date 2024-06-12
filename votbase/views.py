import datetime
import math
from hashlib import sha512, sha256

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pytz import timezone

from . import models
from .extra import get_vote_auth, decrypt
from .merkleTree import merkleTree


# Create your views here.

def index(request):
    error = False
    try:
        time = get_vote_auth()
        format = "%d/%m/%Y at %H:%M:%S %Z%z"
        asia_start = time[0].start.astimezone(timezone("Asia/İstanbul"))
        asia_end = time[0].end.astimezone(timezone("Asia/İstanbul"))
        context = {
            'error': error,
            'start': asia_start.strftime(format),
            'end': asia_end.strftime(format)
        }
    except:
        error = True
        context = {
            'error': error,
        }

    return render(request, 'index.html')


@login_required(login_url='user/login')
def vote(request):
    candidates = models.Candidate.objects.all()
    context = {'candidates': candidates}
    return render(request, 'vote.html', context)


def retDate(v):
    v.timestamp = datetime.datetime.fromtimestamp(v.timestamp)
    return v


@login_required(login_url='login')
def create(request, pk):
    voter = models.Voter.objects.filter(username=request.user.username)[0]
    if request.method == 'POST' and request.user.is_authenticated and not voter.has_voted:
        vote = pk
        lenVoteList = len(models.Voter.objects.all())
        if lenVoteList > 0:
            block_id = math.floor(lenVoteList / 5) + 1
        else:
            block_id = 1
        phrase = request.POST.get('phrase')
        username = request.user.username

        voterpvt = models.Voter_Pvt.objects.filter(username=username).values()

        try:
            privateKey_d, privateKey_n = decrypt(phrase, voterpvt[0]['private=key_d'], voterpvt[0]['private=key_n'],
                                                 voterpvt[0]['salt'])
        except:
            logout(request)
            return render(request, 'failure.html', {'fail':'Invalid Passphrase Please Login And Vote Again.'})

        priv_key = {'n': int(privateKey_n), 'd': int(privateKey_d)}
        pub_key = {'n': int(voter.public_key_n), 'e': int(voter.public_key_e)}
        timestamp = datetime.datetime.now.timestamp()
        ballot = "{}|{}".format(vote, timestamp)
        h = int.from_bytes(sha512(ballot.encode()).digest(), byteorder='big')
        signature = pow(h, priv_key['d'], pub_key['n'])

        hfromSignature = pow(signature, pub_key['e'], pub_key['n'])

        if hfromSignature == h:
            new_vote = models.Vote(vote=pk)
            new_vote.block_id = block_id
            voter.has_voted = True
            voter.save()
            new_vote.save()
            status = 'ballot signed successfully'

            context = {
              'ballot': ballot,
              'signature': signature,
              'status': status,
              'id': new_vote.id,
              }
            return render(request, 'status.html', context)
    logout(request)
    return render(request, 'failure.html', {})


@login_required(login_url='login')
def seal(request):
    if request.method == 'POST':
        vote_id = request.POST.get('vote_id')
        if len(models.Vote.objects.all()) % 5 != 0:
            logout(request)
            return render(request, 'votesucces.html', {'code': vote_id})
        else:
            transactions = models.Vote.objects.order_by('block_id').reverse()
            transactions = list(transactions)[:5]
            block_id = transactions[0].block_id

            str_transactions = [str(x) for x in transactions]

            merkle_tree = merkleTree.merkleTree()
            merkle_tree.makeTreeFromArray(str_transactions)
            merkle_hash = merkle_tree.calculateMerkleRoot()

            nonce = 0
            timestamp = datetime.datetime.now().timestamp()

            vote_auth = models.Vote_Auth.objects.get(username='admin')
            prev_hash = vote_auth.prev_hash
            while True:
                self_hash = sha256('{}{}{}{}'.format(prev_hash, merkle_hash, nonce, timestamp).encode()).hexdigest()
                if self_hash[0] == '0':
                    break
                nonce += 1
            vote_auth.prev_hash = self_hash
            vote_auth.save()
            block = models.Block(id=block_id, prev_hash=prev_hash, self_hash=self_hash, merkle_hash=merkle_hash,
                                 nonce=nonce, timestamp=timestamp)
            block.save()
            print('Block {} has been mined'.format(block_id))
            logout(request)
            return render(request, 'votesucces.html', {'code': vote_id})
    logout(request)
    return redirect("index")


def result(request):
    time = get_vote_auth()
    if time[0].end < datetime.datetime.now(datetime.timezone.utc):
        if request.method == 'GET':
            voterVerification = verifyVotes()
            if len(voterVerification):
                return render(request, 'result.html', {'voterVerification': voterVerification})

            vote_auth = models.Vote_Auth.objects.get(username='admin')
            resultCalculated = vote_auth.resultCalculated
            if not resultCalculated:
                vote_auth.result_Calculated = True
                vote_auth.save()
                list_of_votes = models.Vote.objects.all()
                for vote in list_of_votes:
                    candidate = models.Vote.objects.filter(candidateID=vote.vote)[0]
                    candidate.save()

            context = {"candidates": models.Candidate.objects.order_by('count'),
                       "winner": models.Candidate.objects.order_by('count').reverse()[0]}
            return render(request, 'result.html', context)
    else:
        format("%d/%m/%Y at %H:%M:%S %Z%z")
        asia = time[0].end.astimezone(timezone('Asia/İstanbul'))
        context = {
            'fail': 'result well be displayed after' + asia.strftime(format),
        }
        return render(request, 'failure.html', context)


def verify(request):
    time = get_vote_auth()
    if time[0].end < datetime.datetime.now(datetime.timezone.utc):
        if request.method == 'GET':
            verification = ''
            tampered_block_list = verifyVotes()
            votes = []
            if tampered_block_list:
                verification = 'Verification Failed. Following blocks have been tampered --> {}.\
                    The authority will resolve the issue'.format(tampered_block_list)
                error = True
            else:
                verification = 'Verification successful. All votes are intact!'
                error = False
                votes = models.Vote.objects.order_by('timestamp')
                votes = [retDate(x) for x in votes]

            context = {'verification': verification, 'error': error, 'votes': votes}
            return render(request, 'verification.html', context)
        if request.method == 'POST':
            unique_id = request.POST.get('unique_id')
            try:
                tampered_block_list = verifyVotes()
                if tampered_block_list:
                    verification = 'Verification Failed. Following blocks have been tampered --> {}.\
                    The authority will resolve the issue'.format(tampered_block_list)
                    error = True
                else:
                    verification = 'Verification successful. The Vote is intact!'
                    error = False
                    vote = models.Vote.objects.filter(id=unique_id)
                    vote = [retDate(x) for x in vote]
            except:
                vote = []
                error = True
                verification = 'Invalid Unique ID'
            context = {'verification': verification, 'error': error, 'votes': vote}
            return render(request, 'verification.html', context)
    else:
        format = "%d/%m/%Y at %H:%M:%S %Z%z"
        asia = time[0].end.astimezone(timezone('Asia/Kolkata'))
        context = {
            'fail': "Verification will enable on " + asia.strftime(format),
        }
        return render(request, 'failure.html', context)


def verifyVotes():
    block_count = models.Block.objects.count()
    tampered_block_list = []
    for i in range(1, block_count + 1):
        block = models.Block.objects.get(id=i)
        transactions = models.Vote.objects.filter(block_id=i)
        str_transactions = [str(x) for x in transactions]

        merkle_tree = merkleTree.merkleTree()
        merkle_tree.makeTreeFromArray(str_transactions)
        merkle_tree.calculateMerkleRoot()

        if block.merkle_hash == merkle_tree.getMerkleRoot():
            continue
        else:
            tampered_block_list.append(i)

    return tampered_block_list
