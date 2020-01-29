from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import SignUpForm
from .models import Userinfo, Subject
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
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})
def your_subject_page(request,user_id):
    if request.POST.get('subject_good'):
        subject = Subject.objects.create(subject_name=request.POST['subject_good'])
        U1=Userinfo.objects.get(name="pakkapure")
        U1.good_subject.add(subject)
        U1.save()
        return render(request, 'tinder/your_subject.html', {'name': Userinfo.objects.get(name="pakkapure"),'subject': Userinfo.objects.get(name="pakkapure").good_subject.all()})
    return render(request,'tinder/your_subject.html', {'name': Userinfo.objects.get(name="pakkapure"),'subject': Userinfo.objects.get(name="pakkapure").good_subject.all()})
def home_page(request):
    if not Userinfo.objects.filter(name="pakkapure").exists():
        Userinfo.objects.create(name="pakkapure",age="18",school="king mongkut's university of technology north bangkok")
    if request.POST.get('subject_find'):
        select_sub = Userinfo.objects.filter(good_subject__subject_name=request.POST['subject_find'])
        what_sub = request.POST['subject_find']
        return render(request, 'tinder/home.html', {'search_result': select_sub, "what_sub": what_sub})
    print(list)
    return render(request, 'tinder/home.html', {'name': Userinfo.objects.get(name="pakkapure") })
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
