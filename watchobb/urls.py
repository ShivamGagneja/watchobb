from django.urls import path
from watchobb import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base-page'),
    path('companies/<slug:industry>', views.companies, name='companies'),
    path('companies/', views.Allcompanies),
    path('companies/details/<slug>', views.compDetails, name='comp_details'),
    path('login/', views.Login, name="login"),
    path('login_user', views.LoginUser, name="login_user"),
    path('logout/', views.LogoutUser, name="logout"),
    path('register/<slug:user_type>/', views.SignupUser, name="signup"),
    path('detailsubmit', views.detailsubmit, name="detailsubmit"),
    path('details/<slug:firstname><slug:lastname>', views.userinfo, name="details"),
    path('success/', views.Success, name="success"),
    path('login_recruiter', views.LoginRecruiter, name="login_recruiter"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name="activate"),

]
