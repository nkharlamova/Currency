from accounts import views

from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.ActivateUser.as_view(), name='activate-user'),
]
