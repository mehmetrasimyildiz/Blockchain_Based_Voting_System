import hashlib
from datetime import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse

from . import models
from .forms import UserRegistrationForm, CandidatesInfoForm
from .models import Candidate, Vote, Block, MerkleTree


# Create your views here.


def index(request):
    return render(request, 'index.html/')


def hash_string(data_string):
    return hashlib.sha256(data_string.encode()).hexdigest()


def register_view(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()

            username_hash = hash_string(user.username)
            email_hash = hash_string(user.email)
            first_name_hash = hash_string(user.first_name)
            last_name_hash = hash_string(user.last_name)

            combined_hash = f"{username_hash},{email_hash},{first_name_hash},{last_name_hash}"
            Block.add_block(combined_hash)

            login(request, user)
            return redirect('index')

    return render(request, 'register2.html', {'form': form})


def show_encrypted_info(request):
    blocks = Block.objects.all()
    data = [block.data for block in blocks]
    merkle_tree = MerkleTree(data)
    root_hash = merkle_tree.get_root()
    return render(request, 'encrypted_info.html', {'blocks': blocks, 'root_hash': root_hash})


@login_required(login_url='login')
def vote(request):
    if request.method == 'POST':
        candidate_id = request.POST.get("candidate_id")
        candidate = Candidate.objects.get(id=candidate_id)
        Vote.objects.create(user=request.user, vote_to_who=candidate, has_voted=True)

        return render(request, 'status.html')

    candidates = Candidate.objects.all()
    return render(request, 'vote.html', {'candidates': candidates})


def singing(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('vote'))
        else:
            return render(request, 'failure.html', {'fail': 'Invalid Credentials! Try Logging In Again.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required()
def result(request):
    candidates = models.Candidate.objects.all()
    candidates_with_votes = []
    for candidate in candidates:
        candidate.count = models.Vote.objects.filter(vote_to_who=candidate).count()
        candidates_with_votes.append(candidate)
    context = {
        'candidates': candidates,
        'candidates_with_votes': candidates_with_votes,
    }
    return render(request, 'result.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def candidate(request):
    form = CandidatesInfoForm(request.POST or None)
    context = {
        'form': form
    }

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')

    return render(request, 'candidate.html', context)


@login_required(login_url='login')
def create(request):
    vote_exist_or_not = models.Vote.objects.filter(user=request.user).exists()

    if vote_exist_or_not:
        context = {
            'message': 'already has voted'
        }
        return render(request, 'vote.html', context)
    else:
        if request.method == 'POST':
            candidate_id = request.POST["candidate_id"]
            models.Vote.objects.create(user=request.user, vote_to_who_id=candidate_id, has_voted=True)

            return render(request, 'status.html')

    return render(request, 'failure.html')


@login_required
def vote_list(request):
    votes = Vote.objects.all().order_by('-timestamp')
    return render(request, 'vote_list.html', {'votes': votes})
