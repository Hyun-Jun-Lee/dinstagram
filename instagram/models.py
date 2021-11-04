from django.conf import settings
from django.db import models
import re

# Create your models here.
from django.urls import reverse



class Post(models.Model):
    # user.mypost_set : 해당 user가 작성한 포스팅 / user.like_user_set : 해당 유저가 좋아요한 포스팅
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mypost_set')
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag',blank=True)
    location = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_post_set')


    def __str__(self):
        return self.caption

    # 정규표현식으로 cpation에서 tag 찾아내기
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])
    # 좋아요를 누른 유저인지 반환
    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()
    # 최신글이 timeline 제일 먼저 오게
    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['-id']
