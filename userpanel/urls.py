from django.urls import path
from .views import  (edit_myblog, user_logout,viewmy_profile, edit_profile, my_blogs,view_blog,user_home,confirm_delete_blog,
                     delete_comment,view_mysingleblog,create_blog,delmy_blogs,password_change,password_change_done)

urlpatterns = [
    path('viewmy_profile/', viewmy_profile, name='viewmy_profile'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('edit_myblog/<int:blog_id>/', edit_myblog, name='edit_myblog'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('user_home/',user_home,name='user_home'),
    path('create_blog/',create_blog,name='create_blog'),
    path('delmy_blogs/<int:blog_id>/',delmy_blogs,name='delmy_blogs'),
    path('delete_comment/<int:comment_id>/',delete_comment, name='delete_comment'),
    path('password-change/',password_change, name='password_change'),
    path('password-change-done/',password_change_done, name='password_change_done'),
    path('view_blog/<int:blog_id>/',view_blog,name='view_blog'),
    path('view_mysingleblog/<int:blog_id>/',view_mysingleblog,name='view_mysingleblog'),
    path('confirm_delete_blog/<int:blog_id>/',confirm_delete_blog,name='confirm_delete_blog'),
    path('user_logout/',user_logout,name='user_logout'),

]
