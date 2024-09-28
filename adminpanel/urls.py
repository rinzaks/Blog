from django.urls import path
from .views import  (activate_user,adminpassword_changed,admin_home,blog_view,user_list,deactivate_user,view_user,
                     admin_logout,admin_resetpassword,hide_comment,userblog_view,admin_loginpage)
urlpatterns = [
    path('user_list/',user_list,name='user_list'),
    path('view_user/<int:user_id>/',view_user,name='view_user'),
    path('admin_home/',admin_home,name='admin_home'),
    path('admin_logout/',admin_logout,name='admin_logout'),
    path('admin_resetpassword/',admin_resetpassword,name='admin_resetpassword'),
    path('blog_view/<int:blog_id>/',blog_view, name='blog_view'),
    path('hide_comment/<int:comment_id>/',hide_comment,name='hide_comment'),
    path('userblog_view/<int:user_id>/', userblog_view, name='userblog_view'),
    path('admin_loginpage/',admin_loginpage,name='admin_loginpage'),
    path('admin_password_changed',adminpassword_changed,name='adminpassword_changed'),
    path('deactivate_user/<int:user_id>/', deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),

]
