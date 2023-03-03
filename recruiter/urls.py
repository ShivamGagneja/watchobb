from django.urls import path
from recruiter import views

urlpatterns = [
    path('', views.recruiterHome, name='rhome'),
]
