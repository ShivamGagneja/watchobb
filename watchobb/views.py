from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse 
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from .models import Company

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator
from .forms import UserCreationForm
from Watchob import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from . tokens import generate_token
import time

def show_user(request):
  user = request.user
  if user.is_authenticated:
    fname = user.profile.firstname
    return fname
  else:
    return


def home(request):
  return render(request, "home.html", {'fname':show_user(request)})  


def Success(request):
  return render(request, "success.html", {'fname':show_user(request)})

# def signupform(request):
#   form = UserCreationForm()
#   return render(request, 'signupform.html', {'form': form})
  

# signup for new user and storing data into mysql database
def SignupUser(request,user_type):
  # USER = get_user_model()
  # if request.method == "POST":
  #   fname = request.POST['fname']
  #   lname = request.POST['lname']
  #   dob   = request.POST['dob'  ]
  #   gender= request.POST['gender']
  #   email = request.POST['email']
  #   mobile= request.POST['mobile']
  #   psw   = request.POST['psw'  ]


  #   # match = USER.objects.get(email=email)

  #   myuser = USER.objects.create_user(email, psw)
  #   myuser.profile.user_id = myuser.id
  #   myuser.profile.firstname = fname
  #   myuser.profile.lastname = lname
  #   myuser.profile.date_of_birth = dob
  #   myuser.profile.gender = gender  
  #   myuser.profile.phone = mobile


  #   myuser.save()
  #   myuser.refresh_from_db()
    
  #   messages.success(request, "Account has been successfully created.")
  #   return render(request, 'success.html')
    
  # return redirect('home')
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.profile.firstname = form.cleaned_data.get('firstname')
      user.profile.lastname = form.cleaned_data.get('lastname')
      user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
      user.profile.gender = form.cleaned_data.get('gender')
      user.profile.phone = form.cleaned_data.get('phone')
      user.is_active = False
      user.save()
      user.email = form.cleaned_data.get('email')


      #Welcome Email
      subject = "Welcome to watchobb!!"
      message = "Hello " + user.profile.firstname + "\n\nWelcome to the watchobb family.\n\n At watchobb, we make sure that your dream job should not just be a dream anymore.\n\nLet us help you get to the next level in your career progression and land you a job you would love to go to!\n\nAn email verification link has been sent to your email, please verify your email in order to activate your account.\n\nThanking You\nShivam Gagneja"
      from_email = settings.EMAIL_HOST_USER
      to_list = [user.email]
      send_mail(subject, message, from_email, to_list, fail_silently = True)

      #Verification Email
      current_site = get_current_site(request)
      email_subject = "Activate your Watchobb Account !!"
      message2 = loader.render_to_string('email_verify.html', {
        'name': user.profile.firstname,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
      })
      email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [user.email]
      )
      email.fail_silently = True
      email.send()

      crtn_msg = "Account has been successfully created."
      return render(request, 'success.html',{'crtn_msg':crtn_msg})
  form = UserCreationForm(request.POST)
  return render(request, 'signup.html', {'form': form})

def base(request):
  form = UserCreationForm(request.POST)
  return render(request, "base.html", {'fname':show_user(request), 'form': form})

# def company(request):
#   return render(request, "company.html", {'fname':show_user(request)})

@login_required(login_url='login_user')
def userinfo(request):
  return render(request,"userinfo.html", {'fname':show_user(request)})  

def Login(request, user):
  if request.user.is_authenticated:
    return render(request, "success.html")
  else:
    messages.info(request, "Please login to access this page.")
    return redirect("/")

def LoginUser(request):
  if request.method == "POST":
    email = request.POST['email']
    password   = request.POST['psw']
    is_recruiter = False
    myuser= authenticate(request, email = email, password = password)
    if myuser != None and myuser.is_recruiter == False and myuser.is_staff == False:
      login(request, myuser)
      messages.success(request, "Successfully Logged In.")
      return redirect('home')

    else:
      messages.error(request, "Enter correct Username/Password.")
      return render(request, 'sorry.html')

def LogoutUser(request):
  logout(request)
  request.user = None
  msg = "Logged out successfully."
  return render(request, 'success.html',{"auth_msgs":msg})

def detailsubmit(request):
  if request.method == "POST":
    hsname   = request.POST['hsname' ]
    hsyear   = request.POST['hsyear' ]
    hsmarks  = request.POST['hsmarks']
    intname  = request.POST['intname']
    intyear  = request.POST['intyear']
    intmarks = request.POST['intmarks']
    exp      = request.POST['exp'    ]
    jprofile = request.POST['jprofile']
    project  = request.POST['project']
    comp     = request.POST['comp'   ]
    salary   = request.POST['salary' ]
    salex    = request.POST['salex']
    resume   = request.POST['resume' ]

    user = request.user
    if user.is_authenticated:
      user.profile.high_school  = hsname
      user.profile.hs_year      = hsyear
      user.profile.hs_marks     = hsmarks
      user.profile.inter        = intname
      user.profile.inter_year   = intyear
      user.profile.inter_marks  = intmarks
      user.profile.exp_years    = exp
      user.profile.job_profile  = jprofile
      user.profile.projects     = project
      user.profile.curr_company = comp
      user.profile.curr_salary  = salary
      user.profile.expect_salary= salex
      user.profile.resume       = resume

      user.save()

      messages.success(request, "Details have been submitted successfully.")

    return redirect('home')


def LoginRecruiter(request):
  if request.method == "POST":
    email = request.POST['email']
    password   = request.POST['psw']
    myuser= authenticate(request, email = email, password = password)
    if myuser != None and myuser.is_recruiter == True and myuser.is_staff == False:
      login(request, myuser)
      messages.success(request, "Successfully Logged In.")
      return redirect('home')

    else:
      messages.error(request, "Enter correct Username/Password.")
      return render(request, 'sorry.html')

def activate(request, uidb64, token):
  USER = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = USER.objects.get(pk = uid)
  except(TypeError, ValueError, OverflowError, USER.DoesNotExist):
    user = None

  if user is not None and generate_token.check_token(user, token):
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('details/{}{}'.format(user.profile.firstname,user.profile.lastname))
  else:
    return render(request, 'sorry.html')

def companies(request, industry):
  comp_list = []
  comp_dict = {'product_based':'Product Based', 'service_based':'Service Based', 'startup':'Startup','ecom':'E-Commerce', 'all':''}
  if(industry == "all"):
    comp_list = Company.objects.all().order_by('comp_name')
  else:
    comp_list = Company.objects.filter(comp_type__icontains=comp_dict[industry]).order_by('comp_name')
    # paginator = Paginator(comp_list, 20)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
  keywords = ['abc','xyz','bhf','sjs']
  context = {
      'companies': comp_list,
      'fname':show_user(request),
      'keywords': keywords,
      'results': len(comp_list),
      'industry': comp_dict[industry]
  }
  return render(request, 'company.html', context)

def Allcompanies(request):
  return redirect('/companies/all')

# def compDetails(request, id):
#   keywords = ['abc','xyz','bhf','sjs']
#   company = Company.objects.filter(id__icontains=id)
#   return render(request, 'compDetails.html', {'company':company,'keywords':keywords})

def compDetails(request, slug):
  keywords = ['abc','xyz','bhf','sjs']
  company = Company.objects.filter(slug__icontains=slug)
  return render(request, 'compDetails.html', {'company':company,'keywords':keywords})