from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Userinfo, Subject

# Create your views here.
@login_required
def home(request):
    return render(request, 'tinder/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home.html')
    else:
        form = UserCreationForm()
    return render(request, 'tinder/signup.html', {'form': form})
def your_subject_page(request,user_id):
    if request.POST.get('subject_good'):
        subject = Subject.objects.create(subject_name=request.POST['subject_good'])
        U1=Userinfo.objects.get(name="watcharawut")
        U1.good_subject.add(subject)
        U1.save()
        return render(request, 'tinder/your_subject.html', {'name': Userinfo.objects.get(name="watcharawut"),'subject': Userinfo.objects.get(name="watcharawut").good_subject.all()})
    return render(request,'tinder/your_subject.html', {'name': Userinfo.objects.get(name="watcharawut"),'subject': Userinfo.objects.get(name="watcharawut").good_subject.all()})
def home_page(request):
    if not Userinfo.objects.filter(name="watcharawut").exists():
        Userinfo.objects.create(name="watcharawut")
    return render(request, 'tinder/home.html',{'User': Userinfo.objects.filter(name="watcharawut")})

