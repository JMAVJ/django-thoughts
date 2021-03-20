from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from django.db.models.functions import Length
from django.db.models import Count


def index(request):
    if request.user.is_authenticated:
        return redirect('/thoughts')

    return render(request, 'index.html')


@login_required(login_url='/')
def thoughts(request):
    context = {
        'posts': Post.objects.all().annotate(likes=Count('liked_by')).order_by('-likes'),
    }
    return render(request, 'thoughts.html', context)


@login_required(login_url='/')
def add_thought(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')

    if len(request.POST['thought']) < 1:
        messages.error(request, 'You can not post an empty thought')
        return redirect('/thoughts')

    if len(request.POST['thought']) < 5:
        messages.error(
            request, 'The thought must be at least 5 characters long')
        return redirect('/thoughts')

    post = Post.objects.create(
        created_by=request.user, message=request.POST['thought'])

    return redirect('/thoughts')


@login_required(login_url='/')
def delete_thought(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')

    post = Post.objects.get(id=request.POST['post_id'])

    if post.created_by != request.user:
        return redirect('/auth/logout')

    post.delete()

    return redirect('/thoughts')


@login_required(login_url='/')
def thought(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
        'likes': post.liked_by.all().exclude(id=post.created_by.id),
    }
    if not context['post']:
        return redirect('/thoughts')
    return render(request, 'thought.html', context)


@login_required(login_url='/')
def like_post(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')

    post = Post.objects.get(id=request.POST['post_id'])

    post.liked_by.add(request.user)
    return redirect(f"/thoughts/{request.POST['post_id']}")


@login_required(login_url='/')
def unlike_post(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')

    post = Post.objects.get(id=request.POST['post_id'])

    post.liked_by.remove(request.user)
    return redirect(f"/thoughts/{request.POST['post_id']}")
