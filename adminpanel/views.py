from django.shortcuts import render,redirect,get_object_or_404
from .models import Blog_Table,Profile,Comment_Table
from django.contrib.auth import authenticate,logout,login
from .forms import Login_Form
from userpanel.forms import Comment_Form
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sitevisitor.forms import PasswordChangeForm,Login_Form

def admin_loginpage(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_home')
    else:
        form = Login_Form()
    return render(request, 'adminpanel/admin_loginpage.html',{'form':form})

@login_required(login_url='/404/')
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'User {user.first_name} has been deactivated successfully.')
        return redirect('user_list') 

    return render(request, 'adminpanel/deactivate_user.html', {'user': user})

@login_required(login_url='/404/')
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.success(request, f'User {user.first_name} has been activated successfully.')
        return redirect('user_list') 

    return render(request, 'adminpanel/activate_user.html', {'user': user})

@login_required(login_url='/404/')
def blog_view(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    comments = Comment_Table.objects.filter(blog=blog)
    count = comments.count()
    context = {
        'blog': blog,
        'comments': comments,
        'count': count,
    }
    return render(request, 'adminpanel/blog_view.html', context)

@login_required
def hide_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment_Table, id=comment_id)
        blog = comment.blog 
        comment.status = 'hide' 
        count = Comment_Table.objects.filter(blog=blog).exclude(status='hide').count()
        comment.save()  # Save changes to the database
        messages.success(request, 'Comment has been hidden')
    return redirect('blog_view',blog_id=blog.id,count=count)

@login_required
def userblog_view(request,user_id):
    user = get_object_or_404(User, id=user_id)  # Get the user by user_id
    blogs = Blog_Table.objects.filter(author=user)  # Get blogs by that user
    return render(request, 'adminpanel/userblog_view.html', {'blogs': blogs})

# @login_required(login_url='/404/')
def admin_home(request):
    if request.user.is_staff:
        total_blogs = Blog_Table.objects.count()
        blogs = Blog_Table.objects.all()
        total_comments = Comment_Table.objects.count()
        total_profile = Profile.objects.count()
        context = {'total_profile':total_profile,
                   'total_blogs': total_blogs,
                   'total_comments':total_comments,
                   'blogs':blogs

        }
        return render(request, 'adminpanel/admin_home.html',context)
        
@login_required(login_url='/404/')
def user_list(request):
    if request.user.is_staff:
        profiles = Profile.objects.all()
        users = User.objects.exclude(is_staff= True)
    return render(request,'adminpanel/user_list.html',{'profiles': profiles,'users':users})

@login_required(login_url='/404/')
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)  # Get the profile based on the user
    return render(request, 'adminpanel/view_user.html', {'profile': profile,'user':user}) 

@login_required(login_url='/404/')
def admin_logout(request):
    if request.user.is_staff:
        logout(request)
        return redirect('home')

@login_required(login_url='/404/')
def admin_resetpassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'adminpanel/admin_resetpassword.html', {'form': form})

@login_required(login_url='/404/')
def adminpassword_changed(request):
    return render(request,'adminpanel/adminpassword_changed.html')
