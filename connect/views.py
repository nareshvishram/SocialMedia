from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from SocialMedia.task import *
# Create your views here.
def Login(request):
    # if u r already logged in then no need see this page again n again

    if request.user.is_authenticated:
        return redirect("userProfile", request.user.username)
    error_wrong_user = False
    form = AddUser_Form()
    if request.method == "POST":
        data = request.POST
        un = data["un"]
        ps = data["ps"]
        usr = authenticate(request, username=un, password=ps)
        # print("username", un, usr.username)
        if usr != None:
            login(request, usr)
            username = usr.username
            return redirect("userProfile", username)

        error_wrong_user = True
    dict = {"error_wrong_user": error_wrong_user, "form": form}
    return render(request, "login_register.html", dict)


def Register(request):
    error_username_exist=False
    form = AddUser_Form()
    if request.method == "POST":
        form = AddUser_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            un = request.POST["un"]
            ps = request.POST["ps"]
            email = data.email
            already_existed=User.objects.filter(username=un)
            if not already_existed:
                   usr = User.objects.create_user(un, email, ps)
                   if usr:
                       data.usr = usr
                       data.save()
                       return redirect("login")
            error_username_exist = True

    dict = {"form": form,"error_username_exist":error_username_exist}
    return render(request, "login_register.html", dict)

def Logout(request):
    logout(request)
    return redirect("login")


def UserProfile(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    same_user_or_not = False
    is_there_company = False
    user = User.objects.filter(username=Username)

    '''
      1. condtion
      if there is no logged-in user with this name in our UserDatabase then redirect tp
      Currently logged in user that can be get from request.user.username
    '''

    if not user:
        return redirect("userProfile", request.user.username)

    '''
      If there is a user present in our UserDB with this username then
      extract that user details and then return that username so that we can see that users profile
    '''
    '''Follow - Request coding start '''
    connections = None
    if request.user.username != Username:
        username1 = request.user.username
        username2 = Username
        usr1 = User.objects.get(username=username1)
        usr2 = User.objects.get(username=username2)
        user1 = UserDataBase.objects.get(usr=usr1)
        user2 = UserDataBase.objects.get(usr=usr2)
        connections = Connections.objects.filter(Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1))
        # print(connections)
        if connections:
            connections = connections[0]
    ''' Follow - Request coding End '''

    Usr = user[0]  # getting username that is 0th position
    print(Usr)
    connection_in_userdb = UserDataBase.objects.get(usr=Usr)

    if Username == request.user.username:
        same_user_or_not = True

    ##### this user have company or not ? #######
    data = Comapny_Model.objects.filter(usr=request.user)
    if data:
        is_there_company = True

    ############## Blog Stuffs ###############
    blogs_data = Blogs_Model.objects.filter(usr=User.objects.get(username=Username))

    ###########  Like the blog stuffs #######

    liked_by_me_ids = []  ## --> Total ids of the blogs that this logged in user has liked
    liked = Like_Blogs.objects.filter(usr=request.user)
    for i in liked:
        liked_by_me_ids.append(i.blog.id)
    print(liked_by_me_ids)

    ################ Comment Form ###########
    comment_form = Comment_Blog_Form()

    ##### Comments Data ##############
    comments_data=Comment_Blogs.objects.all().order_by("-date")

    ########## Follow - Following  #########
    logged_in_user = request.user.username
    me_usr = User.objects.get(username=logged_in_user)
    me = UserDataBase.objects.get(usr=me_usr)
    connection = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend"))
    follower = ""
    User_Data = []
    for i in connection:
        UserData = UserDataBase.objects.get(id=i.sender.id)
        if UserData.id != me.id:
            User_Data.append(UserData)

        UserData = UserDataBase.objects.get(id=i.receiver.id)
        if UserData.id != me.id:
            User_Data.append(UserData)
    follower = User_Data
    print(len(User_Data))
    total_follower = len(User_Data)

    dict = {
        "profile": connection_in_userdb, "same_user_or_not": same_user_or_not,
        "connections": connections,
         "is_there_company": is_there_company,
        "blogs_data": blogs_data,
        "liked_by_me_ids": liked_by_me_ids,
        "comment_form":comment_form,
        "comments_data":comments_data,
        "follower":follower,
        "total_follower":total_follower

    }
    return render(request, 'user_details.html', dict)


def Edit_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    # if passed username is not as our logged-in username then simply jump to userProfile
    current_user = request.user.username

    if current_user != Username:
        return redirect("userProfile", current_user)

    usr = User.objects.filter(username=Username)
    Usr = usr[0]
    user_details = UserDataBase.objects.get(usr=Usr)
    # now how to edit our form

    form = Edit_User_Details_form(request.POST or None, request.FILES or None, instance=user_details)
    if form.is_valid():
        form.save()
        return redirect("userProfile", request.user.username)
    dict = {
        "profile": user_details, "form": form
    }
    return render(request, 'edit_user_details_form.html', dict)


def Professionals(request, what):
    if not request.user.is_authenticated:
        return redirect("login")

    logged_in_user = request.user.username
    me_usr = User.objects.get(username=logged_in_user)

    me = UserDataBase.objects.get(usr=me_usr)

    sabhi = Connections.objects.all()
    all_users_till_now=UserDataBase.objects.all()
    data = ""
    #print("me",me)
    #print("sabhi log",UserDataBase.objects.all())
    if what == "all":
        data = UserDataBase.objects.all()

    elif what == 'request':
        connections = Connections.objects.filter(receiver=me, status="send_request")
        User_Data = []
        # print(connections)
        for i in connections:
            ud = UserDataBase.objects.get(id=i.sender.id)
            User_Data.append(ud)
        data = User_Data
    elif what == "pending":
        connections = Connections.objects.filter(sender=me, status="send_request")
        User_Data = []
        for i in connections:
            ud = UserDataBase.objects.get(id=i.receiver.id)
            User_Data.append(ud)
        data = User_Data

    elif what == "friends":
        connection = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend"))
        User_Data = []
        for i in connection:
            UserData = UserDataBase.objects.get(id=i.sender.id)
            if UserData.id != me.id:
                User_Data.append(UserData)

            UserData = UserDataBase.objects.get(id=i.receiver.id)
            if UserData.id != me.id:
                User_Data.append(UserData)
        data = User_Data

    # print("what", what)
    # print("dataaa", data)
    # print("meee", me)
    ################# Coutning ###############
    con_all = Connections.objects.all()
    con_request = Connections.objects.filter(receiver=me, status="send_request")
    con_pending = Connections.objects.filter(sender=me, status="send_request")
    con_friend = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend"))

    dict = {"data": data, "what": what, "con_request": con_request, "con_pending": con_pending,
            "con_friend": con_friend, "con_all": con_all,"all_user_till_now":all_users_till_now}
    return render(request, "professionals.html", dict)


def Manage_connections(request, action, u_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if action == "send_request" or action == "unsent":
        sender_user = User.objects.get(username=request.user.username)
        # sender is Database of sender user (logged in user)
        # receiver is Database of receiver user (whom logged in user sent request )
        sender = UserDataBase.objects.get(usr=sender_user)
        receiver = UserDataBase.objects.get(id=u_id)
        if action == "send_request":
            Connections.objects.create(sender=sender, receiver=receiver)
            return redirect("userProfile", receiver.usr.username)
        if action == "unsent":
            data = Connections.objects.filter(sender=sender, receiver=receiver)
            # print("unsent -data", data)
            if data:
                for c in data:
                    c.status = "unsent"
                    c.save()
                return redirect("professionals", "all")

        return redirect("userProfile", receiver.usr.username)
        # return HttpResponse("request is " + str(action) + "to user id " + str(u_id))

    if action == "accept_request" or action == "reject_request":
        ReceiverUser = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=ReceiverUser)
        sender = UserDataBase.objects.get(id=u_id)
        connection = Connections.objects.filter(sender=sender, receiver=receiver)
        if connection:
            for c in connection:
                if action == "accept_request":
                    c.status = "friend"
                    c.save()
                if action == "reject_request":
                    c.status = "rejected"
                    c.save()

        return redirect("professionals", "all")

    # return render(request,"user_details.html")


def Add_Company(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = Company_Form()
    if request.method == "POST":
        form = Company_Form(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            data = form.save(commit=False)
            data.usr = request.user
            Map = data.map_embad
            if 'width="600"' in Map:
                Map = Map.split('width="600"')
                Map.insert(1, 'width="100%"')
                Map = " ".join(Map)
                data.map_embad = Map
            data.save()
            return redirect("companies_detail")

    dict = {"form": form}
    return render(request, "add_company_form.html", dict)


def Companies_Detail(request):
    if not request.user:
        return redirect("login")
    data = Comapny_Model.objects.filter(usr=request.user)
    form = Blogs_Form()
    blogs_data = Blogs_Model.objects.filter(usr=request.user).order_by("-date")
    print("data", data.first())
    ########## Follow - Following  #########
    logged_in_user = request.user.username
    me_usr = User.objects.get(username=logged_in_user)
    me = UserDataBase.objects.get(usr=me_usr)
    connection = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend"))
    follower = ""
    User_Data = []
    for i in connection:
        UserData = UserDataBase.objects.get(id=i.sender.id)
        if UserData.id != me.id:
            User_Data.append(UserData)

        UserData = UserDataBase.objects.get(id=i.receiver.id)
        if UserData.id != me.id:
            User_Data.append(UserData)
    follower = User_Data
    print(len(User_Data))
    total_follower = len(User_Data)
    dict = {"data": data, "form": form, "blogs_data": blogs_data, "follower": follower,
            "total_follower": total_follower}
    return render(request, "companies_detail.html", dict)


def Company_Blogs(request):
    if request.method=="POST":
        form = Blogs_Form(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.usr = request.user
            data.save()
    return redirect("login")


def Likes(request, b_id, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    blog = Blogs_Model.objects.get(id=b_id)
    ##### Sending Email #######
    user=User.objects.get(username=blog.usr.username)
    userdb=UserDataBase.objects.get(usr=user)
    name=userdb.name.split()[0]
    email=userdb.email
    title=blog.title
    total_likes=len(Like_Blogs.objects.filter(blog=blog))
    msg="You got one liked on {blog} by {name} . Total likes is : {count}.".format(blog=title,name=name,count=total_likes)
    SendEmail.delay(email,msg)
    #Like_Blogs.objects.create(usr=request.user, blog=blog)
    return redirect("userProfile", Username)



def Comments(request,b_id,Username):
    if not request.user.is_authenticated:
        return redirect("login")
    form=Comment_Blog_Form()
    print(form)
    if request.method=="POST":
        form=Comment_Blog_Form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.usr=User.objects.get(username=Username)
            data.blog=Blogs_Model.objects.get(id=b_id)
            data.save()
            print("cheeje",data)
            return redirect("userProfile",Username)


    return render("userProfile",Username)


def SendEmailOld(email,msg):
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        html = get_template("mail.html").render({"msg":msg})
        sub = "TechBlog - New Like"
        send_mail(sub,msg, from_email, to_email, html_message=html)


def See_Comments(request,b_id,Username):
    blog=Blogs_Model.objects.get(id=b_id)
    comments_data=Comment_Blogs.objects.filter(blog=blog)
    print("blog",blog)
    return redirect("userProfile",Username)

def Base_Data(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user=request.user.username
    usr=User.objects.filter(username=user)
    usr=usr[0]
    data=UserDataBase.objects.get(usr=usr)
    dict={"data":data}
    print("data",data)
    return render(request,"base.html",dict)


