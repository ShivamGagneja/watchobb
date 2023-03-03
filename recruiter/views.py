from django.shortcuts import render

# Create your views here.
def show_user(request):
  user = request.user
  if user.is_authenticated:
    fname = user.profile.firstname
    return fname
  else:
    return


def recruiterHome(request):
  return render(request, "rhome.html", {'fname':show_user(request)})  

def SignupRecruiter(request):
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