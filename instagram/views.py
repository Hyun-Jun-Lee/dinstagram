from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from instagram.forms import PostForm
from instagram.models import Tag, Post

@login_required
def index(request):
    # author가 현재 user의 following_set에 포함된 경우만 조회, or 연산위해 Q 사용
    post_list = Post.objects.all()\
        .filter(
        Q(author__in=request.user.following_set.all()) |
        Q(author=request.user) #작성자가 자신인 경우
    )

    # 현재 로그인한 user 제외하고 받기
    suggest_user_list = get_user_model().objects.all().exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all()) # follow하고나면 추천목록에서 사라지게
    return render(request, "instagram/index.html",{
        "post_list":post_list,
        "suggest_user_list":suggest_user_list,
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
    return render(request, "instagram/post_detail.html", {
        "post":post,
    })

def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_count = post_list.count() # DB에 count 쿼리 수행/ len()은 메모리에 올려서 수행
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_count":post_count,
    })