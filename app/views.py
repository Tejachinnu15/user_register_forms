from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
# Create your views here.
def register(request):
    USFO=UserForm()
    PFO=ProfileForm()
    d={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
         USFD=UserForm(request.POST)
         PFD=ProfileForm(request.POST,request.FILES)
         if USFD.is_valid() and PFD.is_valid():
            NSUFO=USFD.save(commit=False)
            submitpassword=USFD.cleaned_data['password']
            NSUFO.set_password(submitpassword)
            NSUFO.save()
            NSPO=PFD.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()
         return HttpResponse('data is submited to database')

    return render(request,'register.html',d)