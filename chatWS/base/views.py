from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import MessageForm, RegisterUserForm
from .models import BaseMessage, Friends, User

import asyncio
import websockets
from dotenv import load_dotenv
import os
import json


load_dotenv()


async def send_data(data):
    url = f'ws://{os.getenv("WS_HOST")}:{os.getenv("WS_PORT")}'
    # print(f"conecting to {url=}")

    async with websockets.connect(url) as ws:
        # print("sending data")
        await ws.send(json.dumps(data))


@login_required(login_url='/login_user')
def home(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            _form = form.save(commit=False)
            _form.sender = request.user
            _form.save()

            sender = request.user.id

            text = form.cleaned_data["message"]
            recipient = User.objects.get(
                username=form.cleaned_data["recipient"])

            data = {
                'text': text,
                'sender':  sender,
                'recipient': recipient.id
            }
            print(f'{data=}')
            asyncio.run(send_data(data))
            return redirect('home')

    form = MessageForm()
    messages = BaseMessage.objects.all().order_by('-id')
    context = {
        'forms': form,
        'messages': messages,
        'host': os.getenv("WS_HOST"),
        'port': os.getenv("WS_PORT")
    }

    return render(request, 'index.html', context=context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            data = {
                'text': '',
                'sender':  user.id,
                'recipient': user.id
            }
            asyncio.run(send_data(data))
            return redirect('home')
        else:
            messages.success(
                request, ('Неправильний логін чи пароль. Спробуйте знову'))
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': form})


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('home')
    logout(request)
    messages.success(request, ('Ви вийшли з акаунту'))
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'register.html', {'form': form})
