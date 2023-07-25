from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from app.forms import *
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
           
            send_mail('Registration',
                      'Registraction is Success check in admin',
                      'chanigallateja@gmail.com',
                      [NSUFO.email],
                      fail_silently=False)
            return HttpResponse('Registration is Succeffully check in admin')
         else:
             return HttpResponse('TRY AGAIN')

    return render(request,'register.html',d)

def Home(request):
    if request.session.get('username'):
        username=request.session.get('username')#collecting username of login user 
        d={'username':username}
        return render(request,'Home.html',d)

    return render(request,'Home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        #authenticate is a function to check for authentication(checking) and authorization(allowing permission)
        if AUO:
            if AUO.is_active:#checking whether the user is active or not
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('Home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))


@login_required
def display_details(request):
    username=request.session.get['username']
    UO=User.objects.get(username=username)
    PO=profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'display_details.html',d)



def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('reset password is done')
        else:
            return HttpResponse('invalid username')



    return render(request,' reset_password.html')
