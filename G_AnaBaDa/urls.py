"""G_AnaBaDa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from account.views import MainView, Logout, Login, Register, FindId
from django.contrib.auth import views as auth_views

from board.views import BoardListView, BoardUploadView
from product.views import UploadProduct, productList, productDetail, myPage
from product import views

import mimetypes
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', MainView.as_view()),

    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('signup/', Register.as_view()),

# 아이디찾기
    path('findId/', FindId.as_view()),
    # 비번찾기
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),  # 리셋 초기 화면 (이메일 입력폼)
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),   # 이메일로 전송 완료 화면
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),  # 메일 링크눌렀을떄
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # 초기화 완료 화면

    path('upload/', UploadProduct.as_view()),
    path('list/', productList.as_view()),
    path('list/<int:pk>', views.productDetail),
    path('myPage/', myPage.as_view()),

    #자유게시판
    path('board/',BoardListView.as_view()),
    path('board_upload/',BoardUploadView.as_view()),
    path('edit/<int:pk>/',views.editproduct),
    path('delete/<int:pk>/',views.deleteproduct),
]

# DEBUG Toolbar
if settings.DEBUG:
    mimetypes.add_type("application/javascript", ".js", True)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
