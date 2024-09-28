from django import forms
from adminpanel.models import Blog_Table,Comment_Table

class Comment_Form(forms.ModelForm):
    comment = forms.CharField(label='Comment',
                              max_length=500,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = Comment_Table
        fields = ['comment']

class Createblog_Form(forms.ModelForm):
    title = forms.CharField(
         label='Title',
         max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    content = forms.CharField(
         label='Description',
         max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control'})
        )
    blog_image = forms.ImageField(
        label='Blog Image',
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    class Meta:
            model = Blog_Table
            fields = ['title','content','blog_image']
