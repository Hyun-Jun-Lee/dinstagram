from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import User
from django import forms

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs): # super()로 오버라이딩받아서 수정
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True # 필수값으로 설정
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','first_name','last_name']

    # email 중복 막기
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 Email입니다")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name','last_name', 'website_url', 'bio', 'phone_number', 'gender']

class Password_Change_Form(PasswordChangeForm): # 기존 Form 상속받아서 수정
    def clean_new_password2(self): # 이전 PW와 바꾼 PW 같으면 안되게 만들어주는 옵션
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError("기존 PW와 다르게 변경해 주세요")
        return new_password2
