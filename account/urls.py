from django.urls import path
from .views import signup_view, login_view, logout_view, profile, change_pass_view, reset_pass, reset_pass2,  update_profile

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name= 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('profile/', profile, name='profile'),
    path('change-pass/', change_pass_view, name='change-pass'),
    path('reset/', reset_pass, name='reset'),
    path('reset2/', reset_pass2, name='reset2'),
    path('profile/update/', update_profile, name='update_profile'),

]