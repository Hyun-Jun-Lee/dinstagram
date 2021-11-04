from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from instagram.forms import PostForm, CommentForm
from instagram.models import Tag, Post

@login_required
def index(request):
    # author가 현재 user의 following_set에 포함된 경우만 조회, or 연산위해 Q 사용
    post_list = Post.objects.all()\
        .filter(
        Q(author__in=request.user.following_set.all()) |
        Q(author=request.user)
    )

    comment_form = CommentForm()
    # 현재 로그인한 user 제외하고 받기
    suggest_user_list = get_user_model().objects.all().exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all()) # follow하고나면 추천목록에서 사라지게
    return render(request, "instagram/index.html",{
        "post_list":post_list,
        "suggest_user_list":suggest_user_list,
        "comment_form": comment_form,
    })

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "포스팅을 완료하였습니다.")
            return redirect(post)
    else:
        form = PostForm
    return render(request, "instagram/post_form.html", {
        "form":form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, "instagram/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })

def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    if request.user.is_authenticated:
        # following_set에 page_user의 pk가 포함되어 있는지 확인
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    post_list = Post.objects.filter(author=page_user)
    post_count = post_list.count() # DB에 count 쿼리 수행/ len()은 메모리에 올려서 수행
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_count":post_count,
        "is_follow":is_follow,
    })

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 좋아요를누르면 현재 user의 like_user_set에 추가
    post.like_user_set.add(request.user)
    messages.success(request, '좋아요')
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, '좋아요 취소')
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {
        "form" : form,
    })
