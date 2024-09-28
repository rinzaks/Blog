from django.shortcuts import render,redirect
from adminpanel.models import Profile,Blog_Table,User,Comment_Table
from .forms import Registration_Form,ProfileForm,Login_Form
from django.contrib import messages
from django.contrib.auth import authenticate,login


def registration(request):
    if request.method == 'POST':
        form = Registration_Form(request.POST)
        form2 = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "user registered  added ")
            return redirect('user_login')
    else:
        form = Registration_Form()
        form2 = ProfileForm()
    return render(request,'sitevisitor/registration.html',{'form':form, 'form2': form2})

def unauthorized_access(request):
    return render(request,'sitevisitor/404.html')

def home(request):
    blogs = Blog_Table.objects.all()
    return render(request,'sitevisitor/home.html',{'blogs': blogs})

def user_login(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_home')                
            else:
                messages.error(request, 'Invalid username or password')
    form = Login_Form()
    return render(request, 'sitevisitor/login.html', {'form': form})