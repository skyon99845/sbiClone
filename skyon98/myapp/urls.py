from django.urls import path
from myapp import views

urlpatterns = [

    path('', views.home, name="homepage"),
    path('submituserinfo', views.submituserinfo),
    path('loginreg', views.loginreg),#for login 
    path('logincheck', views.loginauth),#for checking login
    path('userreg', views.userreg),
    path('dashboard', views.dashboard),
    path('home', views.home),
    path('userlogout', views.userlogout),
    path('addmoney', views.addmoney),
    path('complaint', views.complaint),
    path('updateaddmoney', views.updateaddmoney),
    path('transfermoney', views.transfermoney),
    path('updatetransfermoney', views.updatetransfermoney),
    path('blank', views.blank),
    path('withdrawmoney', views.withdrawmoney),
    path('updatewithdrawmoney', views.updatewithdrawmoney),
    path('updatepasswordform', views.updatepasswordform),
    path('updatepassword', views.updatepassword),
    path('complaint', views.complaint),
    path('updatecomplaint', views.updatecomplaint),
    path('generateotp', views.generateotp),
    path('verify_otp', views.verify_otp),

]
