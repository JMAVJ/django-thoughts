from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re

# Create your views here.


def auth(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed')

    for key in request.POST:
        if len(request.POST[key]) < 1:
            messages.error(request, 'All fields are required')
            return redirect('/')

    EMAIL_REGEX = re.compile(
        r'^[a-z-A-Z0-9.+_-]+@[a-z-A-Z0-9.+_-]+\.[a-zA-Z]+$')

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(
            request, 'The email must be valid'
        )
        return redirect('/')

    user = authenticate(
        username=request.POST['email'],
        password=request.POST['password']
    )

    if user == None:
        messages.error(request, 'Wrong email or password')
        return redirect('/')

    login(request, user)
    return redirect('/thoughts')


def register(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed')

    error = False

    for key in request.POST:
        if len(request.POST[key]) < 1:
            messages.error(request, 'All fields are required')
            return redirect('/')

    EMAIL_REGEX = re.compile(
        r'^[a-z-A-Z0-9.+_-]+@[a-z-A-Z0-9.+_-]+\.[a-zA-Z]+$')

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(
            request, 'The email must be valid'
        )
        error = True

    if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) < 2:
        messages.error(
            request, 'The first and last name must be at least 2 characters long'
        )
        error = True

    if len(request.POST['password']) < 8:
        messages.error(
            request, 'The password must be at least 8 characters long')
        error = True

    if request.POST['password'] != request.POST['password_confirmation']:
        messages.error(
            request, 'The passwords do not match')
        error = True

    if User.objects.filter(email=request.POST['email']).exists():
        messages.error(request, 'The email is already registered')
        error = True

    if error:
        return redirect('/')

    user = User.objects.create_user(
        username=request.POST['email'],
        email=request.POST['email'],
        password=request.POST['password'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'])

    login(request, user)

    return redirect('/thoughts')


def end_session(request):
    logout(request)
    return redirect('/')


def update_password(request):
    if request.method != 'POST':
        return redirect('/signin')

    user = authenticate(
        username=request.user.email, password=request.POST['old_password'])

    if user == None:
        print('Wrong current password')
        return redirect('/users/edit')

    user.set_password(request.POST['new_password'])
    user.save()
    logout(request)
    return redirect('/signin')
