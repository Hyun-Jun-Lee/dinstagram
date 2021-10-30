from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from instagram.forms import PostForm
from instagram.models import Tag


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
            return redirect('/') # 향후 get_absolute_url 활용
    else:
        form = PostForm
    return render(request, "instagram/post_form.html", {
        "form":form,
    })