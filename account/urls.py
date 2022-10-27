from django.urls import path

from account.views import Login, Logout, Register, FindId
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',Login.as_view()),
    path('logout/', Logout.as_view()),
    path('signup/', Register.as_view()),
    # 아이디찾기
    path('findId/', FindId.as_view()),

    # 비번찾기
# 비번찾기 위한 이메일 입력할 첫 화면
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
# 이메일로 전송 완료 화면
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
# 메일 링크눌렀을때 들어가면 비밀번호 재설정 화면나옴
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
#비밀번호 변경 완료
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]