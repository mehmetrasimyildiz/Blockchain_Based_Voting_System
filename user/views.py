import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from pytz import timezone

from votbase.extra import get_vote_auth


# Create your views here.

def login(request):
    time = get_vote_auth()
    if time[0].end > datetime.datetime.now(datetime.timezone.utc) > time[0].start:
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, 'You are now logged in.')
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password.')
                return redirect('login')
        else:
            form = AuthenticationForm()
            return render(request, 'user/login.html', {'form': form})

    else:
        format = "%d/%m/%Y at %H:%M:%S %Z%z"
        if time[0].end < datetime.datetime.now(datetime.timezone.utc):
            asia = time[0].end.astimezone(timezone('Asia/Kolkata'))
            context = {
                'fail': "Voting ended on " + asia.strftime(format),
            }
            return render(request, 'user/login.html', context)
        elif time[0].start > datetime.datetime.now(datetime.timezone.utc):
            asia = time[0].start.astimezone(timezone("Asia/Kolkata"))
            context = {
                'fail': "Voting will start on " + asia.strftime(format),
            }
            return render(request, 'failure.html', context)




def register(request):
    time = get_vote_auth()
    format = "%d/%m/%Y at %H:%M:%S %Z%z"
    if time[0].end < datetime.datetime.now(datetime.timezone.utc):
        asia = time[0].end.astimezone(timezone('Asia/İstanbul'))
        context = {
            'fail': "cannot register! voting ended on" + asia.strftime(format)

        }
        return render(request, 'failure.html', context)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        RePassword = request.POST['RePassword']

        if password == RePassword:

            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, 'Username is already taken.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(request, messages.WARNING, 'email is already taken.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'You are now registered.')
                    return redirect('login')

        else:
            print('password error')
            return redirect('register')

    else:
        return render(request, 'user/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, 'You are now logged out.')
    return redirect('index')
