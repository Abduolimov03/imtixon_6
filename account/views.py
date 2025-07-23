from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from account.forms import ChangePassForm, ResetPassForm
from category.models import Product
from .utils import generate_code, send_to_mail
from datetime import datetime, timedelta
from account.forms import SignUpForms
from account.forms import LoginForms
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required







def logout_view(request):
    logout(request)
    messages.success(request, 'Siz dasturdan chiqdingiz')
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu username orqali oldin royxatdan otilgan')
                return redirect('signup')
            form.save()
            messages.success(request, 'Siz muvaffaqiyatli royxatdan otdingiz')
            return redirect('login')
        else:
            messages.error(request, 'Nimadur xato ketdi')
    else:
        form = SignUpForms()
    return render(request, 'account/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForms(request=request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz muvaffaqiyatli tizimga kirdingiz')
            return redirect('home')
        else:
            messages.error(request, 'Login yoki parol xato')
    else:
        form = LoginForms()
    return render(request, 'account/login.html', {'form':form})

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/profile.html', {'user':user})

@login_required
def change_pass_view(request):
    if request.method == 'GET':
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request, 'Emailingizga tasdiqlash kodi yuborildi.')
        form = ChangePassForm()
        return render(request, 'account/change_pass.html', {'form': form})
    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            confirm_pass = form.cleaned_data['confirm_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')

            if not request.user.check_password(old_pass):
                messages.error(request, 'Eski parol xato')
                return render(request, 'account/change_pass.html', {'form':form})

            if new_pass != confirm_pass:
                messages.error(request, 'Parollar mos emas')
                return render(request, 'account/change_pass.html', {'form':form})

            if session_code != code:
                messages.error(request, 'Tasdiqlah kodi notogri')
                return render(request, 'account/change_pass.html', {'form':form})

            user = request.user
            user.set_password(new_pass)
            user.save()

            messages.success(request, 'Parolingiz muvaffaqiyatli ozgartirildi')
            update_session_auth_hash(request, user)
            del request.session['verification_code']
            return redirect('login')
        else:
            return render(request, 'account/change_pass.html', {'form': form})


def reset_pass(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            code = generate_code()
            request.session['reset_code'] = code
            request.session['username'] = username
            request.session['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            send_to_mail(user.email, code)
            return redirect('reset2')
        except User.DoesNotExist:
            return render(request, 'account/reset_pass1.html')

    return render(request, 'account/reset_pass1.html')

def reset_pass2(request):
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            code = form.cleaned_data['code']
            session_code = request.session.get('reset_code')
            username = request.session.get('username')
            created_at_ = request.session.get('created_at')
            created_at = datetime.strptime(created_at_, '%Y-%m-%d %H:%M:%S')

            if datetime.now() - created_at > timedelta(minutes=1):
                messages.info(request, 'Emailga yuborilgan kod eskirgan ')
                return redirect('reset2')

            if session_code != code:
                messages.error(request, 'Tasdiqlash kodingiz xato')
                return redirect('reset2')

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'Parolingiz ozgartirildi')
            del request.session['reset_code']
            del request.session['username']
            return redirect('login')
    else:
        form = ResetPassForm()

    return render(request, 'account/reset_pass2.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'account/profile_update.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# @login_required(login_url='login')
# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'category_list.html', {'products':products})
#





