
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from .models import Userinfo, Subject
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


def your_subject_page(request,user_id):
    if request.POST.get('subject_good'):
        subject = Subject.objects.create(subject_name=request.POST['subject_good'])
        U1=Userinfo.objects.get(id=user_id)
        U1.good_subject.add(subject)
        U1.save()
        return render(request, 'tinder/your_subject.html', {'name': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(id=user_id).good_subject.all()})
    return render(request,'tinder/your_subject.html', {'name': Userinfo.objects.get(id=user_id),'subject': Userinfo.objects.get(id=user_id).good_subject.all()})
def home_page(request):
    if not Userinfo.objects.filter(name="watcharawut").exists():
        Userinfo.objects.create(name="watcharawut")
    if request.POST.get('subject_find'):
        select_sub = Userinfo.objects.filter(good_subject__subject_name=request.POST['subject_find'])
        what_sub = request.POST['subject_find']
        return render(request, 'tinder/home.html', {'search_result': select_sub, "what_sub": what_sub})
    return render(request, 'tinder/home.html', {'name': Userinfo.objects.get(name="watcharawut") })