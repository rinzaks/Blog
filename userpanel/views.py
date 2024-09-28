from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Profile, Blog_Table, Comment_Table
from django.contrib.auth.models import User
from .forms import Comment_Form, Createblog_Form
from sitevisitor.forms import ProfileForm, Registration_Form, PasswordChangeForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/404/')
def edit_myblog(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    if request.method == 'POST':
        blog_form = Createblog_Form(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            blog_form.save()
            messages.success(request, 'Blog updated successfully.')
            return redirect('my_blogs')
    else:
        blog_form = Createblog_Form(instance=blog)

    return render(request, 'userpanel/edit_myblog.html', {
        'blog_form': blog_form,
        'blog': blog,
    })

# Profile Edit
@login_required(login_url='/404/')
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        register_form = Registration_Form(request.POST, request.FILES, instance=user)

        if profile_form.is_valid() and register_form.is_valid():
            profile_form.save()
            register_form.save()
            return redirect('viewmy_profile')

    else:
        profile_form = ProfileForm(instance=profile)
        register_form = Registration_Form(instance=user)

    context = {
        'profile_form': profile_form,
        'register_form': register_form,
        'logged_user': request.user
    }
    return render(request, 'userpanel/edit_profile.html', context)

@login_required(login_url='/404/')
def viewmy_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'userpanel/viewmy_profile.html', {
        'profile': profile,
        'logged_user': request.user
    })

# Password change
@login_required(login_url='/404/')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'userpanel/password_change.html', {'form': form})

@login_required(login_url='/404/')
def password_change_done(request):
    return render(request, 'userpanel/password_changed.html')

# Blog personal
@login_required(login_url='/404/')
def my_blogs(request):
    blogs = Blog_Table.objects.filter(author=request.user)
    comments = Comment_Table.objects.filter(blog__in=blogs)
    
    context = {
        'blogs': blogs,
        'comments': comments,
        'count': comments.count(),
        'logged_user': request.user,
        'no_blogs_message': "No blogs to display." if not blogs.exists() else None
    }
    return render(request, 'userpanel/my_blogs.html', context)

@login_required(login_url='/404/')
def view_mysingleblog(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    comments = Comment_Table.objects.filter(blog=blog)

    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog = blog
            comment.created_at = timezone.now()
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('view_mysingleblog', blog_id=blog_id)
    else:
        form = Comment_Form()

    context = {
        'blog': blog,
        'comments': comments,
        'count': comments.count(),
        'form': form,
        'logged_user': request.user,
    }
    return render(request, 'userpanel/view_mysingleblog.html', context)

@login_required(login_url='/404/')
def delmy_blogs(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    return render(request, 'userpanel/del_myblogs.html', {'blog': blog, 'logged_user': request.user})

@login_required(login_url='/404/')
def confirm_delete_blog(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully.')
        return redirect('my_blogs')  # Redirect to the list of blogs after deletion

    return render(request, 'userpanel/del_myblogs.html', {
        'blog': blog,
        'logged_user': request.user
    })

@login_required(login_url='/404/')
def create_blog(request):
    if request.method == 'POST':
        form = Createblog_Form(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully.')
            return redirect('my_blogs')
    else:
        form = Createblog_Form()

    return render(request, 'userpanel/create_blog.html', {
        'form': form,
        'logged_user': request.user
    })

@login_required(login_url='/404/')
def user_home(request):
    blogs = Blog_Table.objects.all()
    return render(request, 'userpanel/user_home.html', {
        'logged_user': request.user,
        'blogs': blogs
    })

@login_required(login_url='/404/')
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog_Table, id=blog_id)
    comments = Comment_Table.objects.filter(blog=blog)

    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.created_at = timezone.now()
            comment.blog = blog
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('view_blog', blog_id=blog_id)
    else:
        form = Comment_Form()

    context = {
        'blog': blog,
        'comments': comments,
        'count': comments.count(),
        'form': form,
        'logged_user': request.user,
    }
    return render(request, 'userpanel/view_blog.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment_Table, id=comment_id)
    blog_id = comment.blog.id

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('view_blog', blog_id=blog_id)

    return render(request, 'userpanel/delete_comment.html', {'comment': comment})

@login_required(login_url='/404/')
def user_logout(request):
    logout(request)
    return redirect('home')
