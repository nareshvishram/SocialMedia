from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserDataBase(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    dob=models.DateField(null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    degree=models.CharField(max_length=100,null=True,blank=True)
    website=models.URLField(null=True,blank=True)
    experience=models.CharField(max_length=20,null=True,blank=True)
    company=models.CharField(max_length=200,null=True,blank=True)
    profile_title=models.CharField(max_length=200,null=True,blank=True)
    tweeter=models.URLField(null=True,blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    instagram=models.URLField(null=True, blank=True)


    def __str__(self):
        return self.name


class Connections(models.Model):
    sender=models.ForeignKey(UserDataBase,on_delete=models.CASCADE,related_name="sender",null=True,blank=True)
    receiver = models.ForeignKey(UserDataBase, on_delete=models.CASCADE,related_name="receiver", null=True, blank=True)
    status=models.CharField(max_length=100,null=True,blank=True,default='send_request')

    def __str__(self):
        return self.receiver.name




class Skills(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    percent=models.IntegerField(null=True,blank=True)


class Comapny_Model(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    map_embad=models.TextField( null=True, blank=True)
    total_emp = models.IntegerField(null=True, blank=True)
    about=models.TextField(null=True,blank=True)
    operating_time = models.CharField(max_length=100, null=True, blank=True)
    tweeter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    bg_img=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class Blogs_Model(models.Model):
    usr=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=True,blank=True)
    blogs=models.TextField(null=True,blank=True)
    youtube_embad=models.TextField(null=True,blank=True)
    date=models.DateField(null=True,blank=True)


    def __str__(self):
        return self.title


class Like_Blogs(models.Model):
    # if u delete user then like should'nt be deleted
    # But if u have deleted blog then like table should be deleted
    usr=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    blog=models.ForeignKey(Blogs_Model,on_delete=models.CASCADE,null=True,blank=True)

class Comment_Blogs(models.Model):
    usr=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    blog = models.ForeignKey(Blogs_Model, on_delete=models.CASCADE, null=True, blank=True)
    content=models.TextField(null=True,blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    youtube_embad = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.usr.username


#class Services(models.Model):
 #   title=models.TextField(max_length=100,null=True)
  #  content=models.TextField