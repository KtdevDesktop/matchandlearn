from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import SignUpForm
from .models import Userinfo, Subject,match_class,request_class ,Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.

@login_required
def home(request):
    return render(request, 'tinder/home.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            Userinfo.objects.create(name=user.username, school=user.profile.college, age=user.profile.age, fullname=user.profile.first_name,lastname=user.profile.last_name)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tinderforeduapp/login')
    else:
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})
def your_subject_page(request,user_id):
    if request.POST.get('subject_good'):
        subject = Subject.objects.create(subject_name=request.POST['subject_good'])
        U1=Userinfo.objects.get(name=request.user.username)
        U1.good_subject.add(subject)
        U1.save()
        return render(request, 'tinder/your_subject.html', {'name': Userinfo.objects.get(name=request.user.username),'subject': Userinfo.objects.get(name=request.user.username).good_subject.all()})
    return render(request,'tinder/your_subject.html', {'name': Userinfo.objects.get(name=request.user.username),'subject': Userinfo.objects.get(name=request.user.username).good_subject.all(),'test':Userinfo.objects.get(name=request.user.username).match.all()})
def successlogin(request):
    if request.POST.get('login'):
        return render(request, 'tinder/home.html', {'name': request.user.username })
def another_profile(request,user_id):
    modelget = get_object_or_404(Userinfo,id=user_id)
    Username = Userinfo.objects.get(name=request.user.username)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name,match_guy.name]
    Url_list_sort=sorted(Url_list)
    Url_chat =Url_list_sort[0]+"_"+Url_list_sort[1]
    if match_guy.request.filter(request_list=Username.name).exists():
        return render(request, 'tinder/profile.html', {'name': Userinfo.objects.get(name=request.user.username),
                                                       'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                       'test': Userinfo.objects.get(
                                                           name=request.user.username).match.all(),
                                                       'profile': Userinfo.objects.get(id=user_id),'check':1,"chat_room_name":Url_chat})
    return render(request,'tinder/profile.html',{'profile': modelget,'subject':modelget.good_subject.all(),'name': Userinfo.objects.get(name =request.user.username),"chat_room_name":Url_chat})
def home_page(request):
    if request.POST.get('subject_find'):
        select_sub = Userinfo.objects.filter(good_subject__subject_name=request.POST['subject_find'])
        what_sub = request.POST['subject_find']
        return render(request, 'tinder/home.html', {'name':Userinfo.objects.get(name=request.user.username),"search_result": select_sub, "what_sub": what_sub})
    return render(request,'tinder/home.html',{'name':Userinfo.objects.get(name=request.user.username),'test':Userinfo.objects.get(name=request.user.username).request.all()})
def select_delete(request,user_id):
    User1 = Userinfo.objects.get(id=user_id)
    modelget = get_object_or_404(Userinfo, id=user_id)
    num = request.POST.getlist("subject_list")
    if len(num) == 0:
        pass
    else :
        for i in num:
            select = modelget.good_subject.get(pk=i)
            select.delete()

    return HttpResponseRedirect(reverse('tinder:your_subject', args=(User1.id,)))
def match_request(request,user_id):
    match_list_id  = Userinfo.objects.get(name=request.user.username).request.all()
    list_match = []
    for i in match_list_id:
        list_match.append(Userinfo.objects.get(name=i.request_list))
    return render(request,'tinder/match_request.html',{'name':Userinfo.objects.get(name=request.user.username),'match_request':Userinfo.objects.get(name=request.user.username).request.all(),'list_match':list_match})
def match(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('match'):
        user_name = request_class.objects.create(request_list=Username.name)
        match_guy.request.add(user_name)
        return render(request,'tinder/profile.html', {'name': Userinfo.objects.get(name=request.user.username),'subject': Userinfo.objects.get(id=user_id).good_subject.all(),'test':Userinfo.objects.get(name=request.user.username).match.all(),'check':1,'profile':Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
def Unmatched(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('Unmatched'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        remove_match = match_guy.request.get(request_list=Username.name)
        match_guy.request.remove(remove_match)
        return render(request, 'tinder/profile.html', {'name': Userinfo.objects.get(name=request.user.username),
                                                       'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                       'test': Userinfo.objects.get(
                                                           name=request.user.username).match.all(),
                                                       'profile': Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
    return render(request, 'tinder/profile.html', {'name': Userinfo.objects.get(name=request.user.username),
                                                   'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                   'test': Userinfo.objects.get(name=request.user.username).match.all(),
                                                    'profile': Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
def profile_accept(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    chat_room_name = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('accept'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        match_obj = match_class.objects.create(match=match_guy.name)
        Username.match.add(match_obj)
        request_obj = Username.request.get(request_list=match_guy.name)
        Username.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))
    if request.POST.get('decline'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        request_obj = Username.request.get(request_list=match_guy.name)
        Username.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))
    return render(request,'tinder/profile_accept.html',{'chat_room_name':chat_room_name,'name':Userinfo.objects.get(name=request.user.username),'profile': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(id=user_id).good_subject.all()})
def students_list(request,user_id):
    match_list_id = Userinfo.objects.get(name=request.user.username).match.all()
    list_match = {}
    for i in match_list_id:
        list_sort = []
        key = Userinfo.objects.get(name=i.match)
        list_sort = sorted([Userinfo.objects.get(name=request.user.username).name,Userinfo.objects.get(name=i.match).name])
        value = list_sort[0]+"_"+list_sort[1]
        list_match[key]=value
    return render(request,'tinder/students_list.html',{"name":Userinfo.objects.get(name=request.user.username),'tutor_list':Userinfo.objects.get(id=user_id).match.all(),'list_match':list_match})
def watch_profile(request,user_id):
    if request.POST.get('unmatch'):
        Username=Userinfo.objects.get(name=request.user.username)
        match_guy=Userinfo.objects.get(id=user_id)
        unmatch_obj= Username.match.get(match=match_guy.name)
        Username.match.remove(unmatch_obj)
        return HttpResponseRedirect(reverse('tinder:tutor_list', args=(Username.id,)))
    return render(request,'tinder/watch_profile.html',{'profile':Userinfo.objects.get(id=user_id)})