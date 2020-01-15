from django.shortcuts import render, redirect, get_object_or_404

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
    if request.POST.get('subject_find'):
        select_sub = Userinfo.objects.filter(good_subject__subject_name=request.POST['subject_find'])
        what_sub = request.POST['subject_find']
        return render(request, 'tinder/home.html', {'search_result': select_sub, "what_sub": what_sub})
    print(list)
    return render(request, 'tinder/home.html', {'name': Userinfo.objects.get(name="watcharawut") })
def select_delete(request,user_id):
    deletemodel = get_object_or_404(Userinfo, pk=user_id)
    for i in deletemodel:
        deletemodel.objects.filter(deletemodel)