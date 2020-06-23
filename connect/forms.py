from django import forms
from .models import *


# form that we'll use during registration time
class AddUser_Form(forms.ModelForm):
    class Meta:
        model = UserDataBase
        exclude = ("usr","dob","location","degree","website","company","experience" ,"tweeter","linkedin","facebook","instagram","profile_title")
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control", }),
            "email":forms.EmailInput(attrs={"class":"form-control", }),
            "number":forms.NumberInput(attrs={"class":"form-control", }),
            "image":forms.FileInput(attrs={"class":"form-control","onchange":"loadFile(event)" }),
            "about":forms.Textarea(attrs={"class":"form-control", "rows":"5"}),

        }


class Edit_User_Details_form(forms.ModelForm):
    class Meta:
        model=UserDataBase
        exclude = ("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", }),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "number": forms.NumberInput(attrs={"class": "form-control", }),
            "image": forms.FileInput(attrs={"class": "form-control", "onchange": "loadFile(event)"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "dob":forms.DateInput(attrs={"class":"form-control",}),
            "location": forms.TextInput(attrs={"class": "form-control", }),
            "degree": forms.TextInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "experience": forms.TextInput(attrs={"class": "form-control", }),
            "company": forms.TextInput(attrs={"class": "form-control", }),
            "profile_title": forms.TextInput(attrs={"class": "form-control", }),
            "tweeter": forms.URLInput(attrs={"class": "form-control", }),
            "linkedin": forms.URLInput(attrs={"class": "form-control", }),
            "facebook": forms.URLInput(attrs={"class": "form-control", }),
            "instagram": forms.URLInput(attrs={"class": "form-control", }),


        }


class Company_Form(forms.ModelForm):
    class Meta:
        model=Comapny_Model
        exclude=("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", }),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "number": forms.NumberInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "logo": forms.FileInput(attrs={"class": "form-control", "onchange": "loadFile(event)"}),
            "address": forms.TextInput(attrs={"class": "form-control", }),
            "title": forms.TextInput(attrs={"class": "form-control", }),
            "map_embad": forms.Textarea(attrs={"class": "form-control", }),
            "total_emp": forms.NumberInput(attrs={"class": "form_control", }),
            "operating_time": forms.TextInput(attrs={"class": "form-control", }),
            "profile_title": forms.TextInput(attrs={"class": "form-control", }),
            "tweeter": forms.URLInput(attrs={"class": "form-control", }),
            "linkedin": forms.URLInput(attrs={"class": "form-control", }),
            "facebook": forms.URLInput(attrs={"class": "form-control", }),
            "instagram": forms.URLInput(attrs={"class": "form-control", }),
            "about": forms.Textarea(attrs={"class": "form-control", }),
            "bg_img": forms.FileInput(attrs={"class": "form-control",}),

        }


class Blogs_Form(forms.ModelForm):
    class Meta:
        model=Blogs_Model
        exclude=("usr",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", }),
            "blogs":forms.Textarea(attrs={"class": "form-control", }),
            "date": forms.DateInput(attrs={"class": "form-control", }),
            "youtube_embad": forms.Textarea(attrs={"class": "form-control", }),


        }


class Comment_Blog_Form(forms.ModelForm):
    class Meta:
        model=Comment_Blogs
        exclude=("usr","blog",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", }),
            "date": forms.DateInput(attrs={"class": "form-control", }),
            "youtube_embad": forms.Textarea(attrs={"class": "form-control", }),
            "content": forms.Textarea(attrs={"class": "form-control", }),
            "image":forms.FileInput(attrs={"class": "form-control", }),
        }