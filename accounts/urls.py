from django.urls import path
from .views import loginview, profileview, user_register, EditUserView, edit_user
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns=[
    #path('login/',loginview,name='login'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',profileview,name='profile'),
    path('password-change/',PasswordChangeView.as_view(),name='password_change'),
    path('password-change-done/',PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password-reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password-reset-done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='comfirm'),
    path('password-reset-complate/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('signup/', user_register,name='signup'),
    #path('edit/',edit_user,name='edit'),
    path('edit/',EditUserView.as_view(),name='edit'),
]