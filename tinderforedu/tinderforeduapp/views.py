from django.shortcuts import render, redirect

# Create your views here.
from .models import Userinfo, Subject
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
