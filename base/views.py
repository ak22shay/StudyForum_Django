import http
from multiprocessing import context
from re import L
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

import base
from .models import Room, Topic
# Create your views here.

# room_data =[
#     {'id':1, 'name': 'spring boot developement'},
#     {'id':2, 'name': 'python developement'},
#     {'id':3, 'name': 'react frontend'},
# ]
def logoutuser(request):
    logout(request)
    return redirect('home') 

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method==('POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user:
             login(request, user)
             return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect ')
    content = {'page':page} 
    return render(request, 'base/login_register.html', content)

def registerUser(request):
    page = 'register'
    content = {'page':page} 
    return render(request, 'base/login_register.html', content)

def home(request):

    q=request.GET.get('q') if request.GET.get('q')!= None else ''

    room_data = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topic = Topic.objects.all()

    room_count = room_data.count()
    content = {'room_data':room_data, 'topics' :topic, 'room_count':room_count}
    return render(request, 'base/home.html', content)

def rooms(request, pk):
    room_id = Room.objects.get(id=pk)
    return render(request, 'base/rooms.html', {'room_id':room_id})

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method=="POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html' , {'form':form})

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Access Restricted')

    if request.method=="POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    content = {'form':form}
    return render(request, 'base/room_form.html', content)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Access Restricted')
    if request.method=="POST":
        room.delete()
        return redirect('home')
    content = {}
    return render(request, 'base/delete.html', content)
