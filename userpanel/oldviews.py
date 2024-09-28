from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Profile, Blog_Table, Comment_Table
from django.contrib.auth.models import User
from .forms import Comment_Form,Createblog_Form
from sitevisitor.forms import ProfileForm,Registration_Form
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from sitevisitor.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required



@login_required(login_url='/404/')
def user_logout(request):
    logout(request)   
    return redirect('home')  
 


@login_required(login_url='/404/')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userpanel/password_change.html', {'form': form})

@login_required(login_url='/404/')
def password_change_done(request):
    return render(request, 'userpanel/password_changed.html')

@login_required(login_url='/404/')
def edit_profile(request,user_id):
    logged_user = request.user
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
            profile_form  = ProfileForm(request.POST,request.FILES,instance=profile)
            register_form  = Registration_Form(request.POST,request.FILES,instance=user)

            if profile_form.is_valid() and register_form.is_valid():
                return redirect('viewmy_prrofile')
    else:
        profile_form  = ProfileForm(request.POST,request.FILES,instance=profile)
        register_form  = Registration_Form(request.POST,request.FILES,instance=user)

    return render(request,'userpanel/edit_profile.html',{'profile_form':profile_form,'register_form': register_form,'logged_user':logged_user})






    return render(request,'userpanel/edit_profile.html')

#view to see own blogs
@login_required(login_url='/404/')
def my_blogs(request):
    logged_user = request.user
    blogs = Blog_Table.objects.filter(author=logged_user)
    
    # Check if there are no blogs
    if not blogs.exists():
        no_blogs_message = "No blogs to display."
        return render(request, 'userpanel/my_blogs.html', {'logged_user': logged_user, 'no_blogs_message': no_blogs_message})

    comments = Comment_Table.objects.filter(blog__in=blogs)
    count = comments.count()

    return render(request, 'userpanel/my_blogs.html', {
        'blogs': blogs,
        'logged_user': logged_user,
        'count': count,
        'comments': comments
    })

@login_required(login_url='/404/')
def view_mysingleblog(request,blog_id):
    logged_user=request.user
    blog = get_object_or_404(Blog_Table, id=blog_id)
    comments = Comment_Table.objects.filter(blog=blog)
    count = comments.count()
    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = logged_user
            comment.created_at = timezone.now()
            comment.blog = blog
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('view_mysingleblog', blog_id=blog_id)
    else:
        form = Comment_Form()

    context = {
        'blog': blog,
        'comments': comments,
        'count': count,
        'form': form,
        'logged_user': logged_user,
    }
    return render(request, 'userpanel/view_mysingleblog.html', context)

#to view my profile
@login_required(login_url='/404/')
def viewmy_profile(request):
    logged_user = request.user
    profile = get_object_or_404(Profile,user = logged_user)
    return render(request,'userpanel/viewmy_profile.html', {'profile': profile, 'logged_user':logged_user})
 
#to delete own blogs
@login_required(login_url='/404/')
def delmy_blogs(request,blog_id):
    logged_user = request.user
    blog = get_object_or_404(Blog_Table,id = blog_id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request,'Blog deleted')
        return redirect('my_blogs')
    return render(request,'userpanel/del_myblogs.html',{'blog':blog,'logged_user':logged_user})
 
#edit my blogs
@login_required(login_url='/404/')
def edit_myblog(request,blog_id):
    logged_user = request.user
    blog = get_object_or_404(Blog_Table,id = blog_id)
    if request.method == 'POST':
        blog_Form  = Createblog_Form(request.POST,request.FILES,instance=blog)
        if blog_Form.is_valid():
            blog_form.save() 
            return redirect('my_blogs')
    else:
        blog_form = Createblog_Form(instance=blog)
    return render(request,'userpanel/edit_myblog.html',{'blog_Form':blog_Form,'blogs': blog,'logged_user':logged_user})

@login_required(login_url='/404/')
def create_blog(request):
    logged_user = request.user
    if request.method == 'POST':
        form = Createblog_Form(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request,'Blog created Succesfully')
            return redirect('my_blogs')
    else:
        form = Createblog_Form()
    return render(request, 'userpanel/create_blog.html', {'form': form,'logged_user':logged_user})

@login_required(login_url='/404/')
def user_home(request):
    blogs = Blog_Table.objects.all()  
    logged_user = request.user
    return render(request, 'userpanel/user_home.html', {'logged_user': logged_user,'blogs':blogs})

@login_required 
def view_blog(request, blog_id):
    logged_user = request.user
    blog = get_object_or_404(Blog_Table, id=blog_id)
    comments = Comment_Table.objects.filter(blog=blog)
    count = comments.count()
    
    # Handle comment posting
    if request.method == 'POST':
        form = Comment_Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = logged_user
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
        'count': count,
        'form': form,
        'logged_user': logged_user,
    }
    return render(request, 'userpanel/view_blog.html', context)

@login_required 
def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment_Table,id = comment_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('view_blog',comment.id)
    return render(request,'userpanel/user_home.html',{'comment': comment})
