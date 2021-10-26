from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            next_url = request.GET.get('next', '/')
            form.save()
            messages.success(request, "회원가입을 환영합니다")
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form' : form,
    })