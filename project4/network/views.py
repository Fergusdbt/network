import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follower


def index(request):
    id = request.user.id

    if request.method == "POST":
        user = User.objects.get(id=id)
        content = request.POST["content"]
        post = Post(user=user, content=content)
        post.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        posts = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        likes = Like.objects.filter(user=id)
        liked_posts = []

        for like in likes:
            if like.user.id == id:
                liked_posts.append(like.post)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "liked_posts": liked_posts
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    user = User.objects.get(username=username)

    if request.method == "POST":
        follower = request.user
        button = request.POST["button"]

        if button == "Follow":
            following = Follower(user=user, follower=follower)
            following.save()
            return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

        else:
            following = Follower.objects.get(user=user, follower=follower)
            following.delete()
            return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

    else:
        posts = Post.objects.filter(user=user).order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_following = user.followers.filter(follower=request.user.id).exists()

        return render(request, "network/profile.html", {
            "user": user,
            "page_obj": page_obj,
            "is_following": is_following
        })


def following(request):
    user = request.user
    followings = Follower.objects.filter(follower=user)
    followed_users = [following.user for following in followings]
    followed_posts = Post.objects.filter(user__in=followed_users).order_by("-timestamp")
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


def edit(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_content = data.get("content")

        post = Post.objects.get(id=id)
        post.content = new_content
        post.save()
        return JsonResponse(post.serialize())

    else:
        post = Post.objects.get(id=id)
        return JsonResponse(post.serialize())


def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    like = Like.objects.filter(user=user, post=post)

    if like.exists():
        like.delete()
        message = "unliked"

    else:
        like = Like(user=user, post=post)
        like.save()
        message = "liked"

    like_count = Like.objects.filter(post=post).count()
    return JsonResponse({
        'message': message,
        'like_count': like_count
    })

