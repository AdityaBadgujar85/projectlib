from django.urls import path
from django.contrib.auth import views as auth_views
import students.views as views

urlpatterns = [

    path('', views.HomePage, name='HomePage'),
    path('About/', views.AboutPage, name='About'),
    path('Login/', views.loginPage, name='Login'),
    path('Register/', views.registerPage, name='Register'),
    path('logout/', views.logout_page, name='logout'),
    path('Upload/', views.UploadPage, name='Upload'),
    path('Repository/', views.RepositoryPage, name='Repository'),
    path('Video/<studid>', views.video_page, name='Video'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('Video/<int:studid>/like/', views.video_like, name='video_like'),



]
