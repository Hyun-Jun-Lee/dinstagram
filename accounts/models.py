from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    # 성별 남,여 선택할 수 있게 설정
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male" # DB에 저장되는 값, 실제 값
        FEMAle = "F", "Female"
    website_url = models.URLField(blank=True) # 없어도 됨
    bio = models.TextField(blank=True)
    # 정규표현식 사용해서 휴대폰 번호 양식 지정 -?[1-9]\d{3}-?\d{4}$
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r"^010-?([0-9]{3,4})-?([0-9]{4})$")])
    gender = models.CharField(max_length=2, blank=True, choices=GenderChoices.choices)
    # profile 이미지 업로드 전에 1. form에서 enctype="multipart/form-data" 확인 2. view에서 request.FILES 확인
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%y%m%d") # 파일 업로드한 연/월/일 별로 폴더만들어서 저장