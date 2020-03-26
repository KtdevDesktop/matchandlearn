from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import SignUpForm, CommentForm, AdditionalForm, Editprofileform,profilepicture
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django import db
from django.db import close_old_connections
# Create your views here.

@login_required
def home(request):
    return render(request, 'tinder/home.html')

def test_redirect(request):
    return HttpResponseRedirect("/")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.bio = form.cleaned_data.get('bio')
            newuser = Userinfo.objects.create(name=user.username, school=user.profile.college,schoolkey=stringforschool(user.profile.college), age=user.profile.age, fullname=user.profile.first_name,lastname=user.profile.last_name,bio =user.profile.bio)
            Profilepic.objects.create(user=newuser,images='default.png')
            newuser.save()
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please verify your email address.'
            message = render_to_string('tinder/acc_active_email.html', {
                                        'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user), })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            db.connection.close()
            return render(request,'tinder/email_sent.html')

    else:
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request,'tinder/Activation_success.html')
    else:
        return HttpResponse('''Activation link is invalid! <META HTTP-EQUIV="Refresh" CONTENT="5;URL=/login">''')

def your_subject_page(request,user_id):
    User = Userinfo.objects.get(name=request.user.username)
    comments = Comment.objects.filter(post=request.user.id)
    pic = Profilepic.objects.get(user=User)
    if request.POST.get('subject_good'):
        subject = Subject.objects.create(subject_name=request.POST['subject_good'],subject_keep=stringforsearch(request.POST['subject_good']))
        U1=Userinfo.objects.get(name=request.user.username)
        U1.good_subject.add(subject)
        U1.save()
        return render(request, 'tinder/your_subject.html', {'comments': comments,'pic':pic,'name': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(name=request.user.username).good_subject.all()})
    return render(request,'tinder/your_subject.html', {'comments': comments,'pic':pic,'name': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(name=request.user.username).good_subject.all(),'test':Userinfo.objects.get(name=request.user.username).match.all()})
def successlogin(request):
    if request.POST.get('login'):
        return render(request, 'tinder/home.html', {'name': request.user.username })
def another_profile(request,user_id):
    pic = Profilepic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    modelget = get_object_or_404(Userinfo,id=user_id)
    Username = Userinfo.objects.get(name=request.user.username)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name,match_guy.name]
    Url_list_sort=sorted(Url_list)
    Url_chat =Url_list_sort[0]+"_"+Url_list_sort[1]
    if request.POST.get('comment_input'):
        comment_text = Comment.objects.create(comment=request.POST['comment_input'])
        if not Comment.objects.filter(whocomment = Username, commentto= match_guy):
            a1 = Comment.objects.create(comment_value = comment_text, whocomment = Username, commentto= match_guy)
            a1.save()
        else:
            a1 = Comment.objects.get(whocomment = Username, commentto= match_guy)
            a1.comment_value = comment_text
            a1.save()
    if request.POST.get('star_input'):
        star_score = Comment.objects.create(comment=request.POST['star_input'])
        if not Comment.objects.filter(whocomment = Username, commentto= match_guy):
            a1 = Comment.objects.create(comment_value = star_score, whocomment = Username, commentto= match_guy)
            a1.save()
        else:
            a1 = Comment.objects.get(whocomment = Username, commentto= match_guy)
            a1.comment_value = star_score
            a1.save()
    if match_guy.request.filter(request_list=Username.name).exists():
        return render(request, 'tinder/profile.html', {'comments': comments,'pic':pic,'name': Userinfo.objects.get(name=request.user.username),
                                                       'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                       'test': Userinfo.objects.get(
                                                           name=request.user.username).match.all(),
                                                       'profile': Userinfo.objects.get(id=user_id),'check':1,"chat_room_name":Url_chat})
    return render(request,'tinder/profile.html',{'comments': comments,'pic':pic,'profile': modelget,'subject':modelget.good_subject.all(),'name': Userinfo.objects.get(name =request.user.username),"chat_room_name":Url_chat})


def adddata(request):
    if request.method == "POST":
        form = AdditionalForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data.get('school')
            adddata = Userinfo.objects.get(name=request.user.username)
            adddata.school = school
            adddata.schoolkey = stringforschool(school)
            adddata.save()
            return HttpResponseRedirect('/')
    else:
        form = AdditionalForm()
    return render(request, 'tinder/adddata.html', {'form': form})

def home_page(request):
    """search here"""
    select_sub = []
    sendPOST = 0
    if (Userinfo.objects.filter(name=request.user.username).count() == 0):
        return HttpResponseRedirect('/login')
    if Userinfo.objects.get(name=request.user.username).school == '':
        return HttpResponseRedirect('/adddata')
    if request.POST.get('subject_find'):
        sendPOST = 1
        infoma = {}
        what_sub = stringforsearch(request.POST['subject_find'])
        if request.POST['filter'] != "" and request.POST['location_school'] !=" ":
            select_sub = Userinfo.objects.filter(good_subject__subject_keep=what_sub,schoolkey=stringforschool(request.POST['location_school']),bio=request.POST['filter'])
            for key in select_sub:
                infoma[key] = Profilepic.objects.get(user=key)
        elif request.POST['filter'] != "":
            select_sub = Userinfo.objects.filter(good_subject__subject_keep=what_sub,bio=request.POST['filter'])
            for key in select_sub:
                infoma[key] = Profilepic.objects.get(user=key)
        elif request.POST['location_school'] != "":
            select_sub = Userinfo.objects.filter(good_subject__subject_keep=what_sub,
                                                     schoolkey=stringforschool(request.POST['location_school']))
            for key in select_sub:
                infoma[key] = Profilepic.objects.get(user=key)
        else:
            select_sub = Userinfo.objects.filter(good_subject__subject_keep=what_sub)
            for key in select_sub:
                infoma[key] = Profilepic.objects.get(user=key)
        return render(request, 'tinder/home.html', {'infoma':infoma,'name':Userinfo.objects.get(name=request.user.username),"search_result": select_sub, "search_size": len(select_sub),'sendPOST' : sendPOST, "what_sub": request.POST['subject_find']})
    close_old_connections()
    db.connection.close()
    return render(request,'tinder/home.html',{ 'name':Userinfo.objects.get(name=request.user.username), "search_size": len(select_sub),'sendPOST':sendPOST,'test':Userinfo.objects.get(name=request.user.username).request.all()})
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
    usernaem=Userinfo.objects.get(name=request.user.username)
    usernaem.read()
    usernaem.save()
    for i in match_list_id:
        list_match.append(Userinfo.objects.get(name=i.request_list))
    return render(request,'tinder/match_request.html',{'name':Userinfo.objects.get(name=request.user.username),'match_request':Userinfo.objects.get(name=request.user.username).request.all(),'list_match':list_match})
def match(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    pic = Profilepic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    already_match = 0
    if request.method == "POST":
        if match_guy.request.filter(request_list=Username.name,whorecive=match_guy.name) or Username.request.filter(request_list=match_guy.name,whorecive=Username.name) :
            already_match=1
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': comments, 'pic': pic,
                           'name': Userinfo.objects.get(name=request.user.username),
                           'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                           'test': Userinfo.objects.get(name=request.user.username).match.all(), 'check': 1,
                           'profile': Userinfo.objects.get(id=user_id), 'chat_room_name': Url_chat})
        else:
            user_name = request_class.objects.create(request_list=Username.name,request_message=request.POST['text_request'],whorecive=match_guy.name)
            match_guy.request.add(user_name)
            Userinfo.objects.get(id=user_id).notify()
            Userinfo.objects.get(id=user_id).save()
            return render(request,'tinder/profile.html', {'already_match':already_match,'comments': comments,'pic': pic,'name': Userinfo.objects.get(name=request.user.username),'subject': Userinfo.objects.get(id=user_id).good_subject.all(),'test':Userinfo.objects.get(name=request.user.username).match.all(),'check':1,'profile':Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
def Unmatched(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    pic = Profilepic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    Url_chat = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('Unmatched'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        remove_match = match_guy.request.get(request_list=Username.name,whorecive=match_guy.name)
        match_guy.request.remove(remove_match)
        Userinfo.objects.get(id=user_id).denotify()
        Userinfo.objects.get(id=user_id).save()
        return render(request, 'tinder/profile.html', {'comments': comments,'pic': pic,'name': Userinfo.objects.get(name=request.user.username),
                                                       'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                       'test': Userinfo.objects.get(
                                                           name=request.user.username).match.all(),
                                                       'profile': Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
    return render(request, 'tinder/profile.html', {'comments': comments,'pic': pic,'name': Userinfo.objects.get(name=request.user.username),
                                                   'subject': Userinfo.objects.get(id=user_id).good_subject.all(),
                                                   'test': Userinfo.objects.get(name=request.user.username).match.all(),
                                                    'profile': Userinfo.objects.get(id=user_id),'chat_room_name':Url_chat})
def profile_accept(request,user_id):
    Username = Userinfo.objects.get(name=request.user.username)
    pic = Profilepic.objects.get(user=user_id)
    match_guy = Userinfo.objects.get(id=user_id)
    Url_list = [Username.name, match_guy.name]
    Url_list_sort = sorted(Url_list)
    comments = Comment.objects.filter(post=user_id)
    chat_room_name = Url_list_sort[0] + "_"+Url_list_sort[1]
    if request.POST.get('accept'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        match_obj = match_class.objects.create(match=match_guy.name,youself=Username.name)
        Username.match.add(match_obj)
        request_obj = Username.request.get(request_list=match_guy.name,whorecive=Username.name)
        Username.request.remove(request_obj)
        match_obj2 = match_class.objects.create(match=Username.name,youself=match_guy.name)
        match_guy.match.add(match_obj2)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))
    if request.POST.get('decline'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        request_obj = Username.request.get(request_list=match_guy.name,whorecive=Username.name)
        Username.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(Username.id,)))
    return render(request,'tinder/profile_accept.html',{'comments':comments,'pic':pic,'name': Userinfo.objects.get(name=request.user.username),'chat_room_name':chat_room_name,'name':Userinfo.objects.get(name=request.user.username),'profile': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(id=user_id).good_subject.all(),'request': Username.request.get(request_list=match_guy.name)})
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
    match_guy = Userinfo.objects.get(id=user_id)
    post = get_object_or_404(Userinfo, name=match_guy.name)
    pic = Profilepic.objects.get(user=user_id)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.name = request.user.username
            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()
    if request.POST.get('unmatch'):
        Username = Userinfo.objects.get(name=request.user.username)
        match_guy = Userinfo.objects.get(id=user_id)
        unmatch_obj= Username.match.get(match=match_guy.name,youself=Username.name)
        Username.match.remove(unmatch_obj)
        unmatch_obj2= match_guy.match.get(match=Username.name,youself=match_guy.name)
        match_guy.match.remove(unmatch_obj2)
        return HttpResponseRedirect(reverse('tinder:students_list', args=(Username.id,)))
    return render(request,'tinder/watch_profile.html',{'pic':pic,'name':Userinfo.objects.get(name=request.user.username),'profile':Userinfo.objects.get(id=user_id),'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

def edit_profile(request,user_id):
    User = Userinfo.objects.get(name=request.user.username)
    Pic = Profilepic.objects.get(user= User)
    if request.method == "POST":
        form = Editprofileform(request.POST,instance=User)
        formpic = profilepicture(request.POST,request.FILES,instance=Pic)
        if form.is_valid() and formpic.is_valid():
            form.save()
            formpic.save()
            return HttpResponseRedirect(reverse('tinder:your_subject', args=(user_id,)))

    else:
        form = Editprofileform(instance=User)
        formpic = profilepicture(instance=Pic)
    return render(request,'tinder/edit_profile.html',{"pic":Pic,'form':form,'formpic':formpic})
def stringforsearch(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(' ', '')
    return keyword
def stringforschool(keyword):
    keyword = keyword.upper()
    keyword = keyword.replace(' ','')
    return keyword