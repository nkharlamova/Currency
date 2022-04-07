from accounts import views

from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
]
