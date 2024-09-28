from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f'Profile of {self.user.username}'
    
class Blog_Table(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Comment_Table(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog_Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
    

    
# from django.db import models
# from  django.contrib.auth.models import User


# # Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone=models.CharField(max_length=20)
#     profile_image=models.ImageField(upload_to='profile_image/')
#     id_proof=models.ImageField(upload_to='id_proof/')

#     def __str__(self):
#         return self.name

# class Blog_Table(models.Model):
#     title= models.CharField(max_length=200)
#     content=models.TextField(max_length=1000)
#     blog_image=models.ImageField(upload_to='blog_content/')
#     author=models.ForeignKey(User,on_delete=models.CASCADE)
#     created_at=models.DateField(auto_now_add=True)
#     updated_at=models.DateField(auto_now_add=True)
#     status=models.CharField(max_length=20)
#     def __str__(self):
#         return self.name

# class Comment_Table(models.Model):
#     comment= models.TextField()
#     author=models.ForeignKey(User,on_delete=models.CASCADE)
#     blog=models.ForeignKey(Blog_Table,on_delete=models.CASCADE)
#     created_at=models.DateField(auto_now_add=True)
#     updated_at=models.DateField(auto_now_add=True)
#     status=models.CharField(max_length=20)


#     def __str__(self):
#         return f'Comment by {self.author.username} on {self.blog.title}'
    
# class Profile(models.Model):
#     name = models.CharField(max_length=200)
#     username=models.CharField(max_length=200,unique=True)
#     password=models.EmailField(max_length=200,unique=True)
#     email=models.CharField(max_length=200)
#     phone=models.CharField(max_length=20)
#     profile_image=models.ImageField(upload_to='profile_image/')
#     id_proof=models.ImageField(upload_to='id_proof/')

#     def __str__(self):
#         return self.name