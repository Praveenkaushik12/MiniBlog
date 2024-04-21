from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Blog
from django.contrib.auth.models import Group
# Create your views here.
def home_page(request):
    blogs=Blog.objects.all()
    return render(request,'blog_app/home.html',{'blogs':blogs})

def about_page(request):
    return render(request,'blog_app/about.html')

def contact_page(request):
    return render(request,'blog_app/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        blogs=Blog.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        ip=request.session.get('ip',0)
        return render(request,'blog_app/dashboard.html',{'blogs':blogs,'full_name':full_name,'groups':gps,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')
    

#signUp Page
def user_signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request,'Congratulations!You have become an Author.')
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog_app/signup.html',{'form':form})


#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()
        return render(request,'blog_app/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
        


#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add_post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=BlogForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                post=Blog(title=title,desc=desc)
                post.save()
                messages.success(request,'Blog added successfully!')
                form=BlogForm()
        else:
            form=BlogForm()   
        return render(request,'blog_app/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#update_post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Blog.objects.get(pk=id)
            form=BlogForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Updated successfully!')
        else:
            pi=Blog.objects.get(pk=id)
            form=BlogForm(instance=pi)   
        return render(request,'blog_app/update.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#delete_post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Blog.objects.get(pk=id)
            pi.delete()
            messages.success(request,'Deleted Successfully!')
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')