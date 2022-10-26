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
from account.views import MainView

import mimetypes
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    #G_AnaBaDa에서 관리해야하는것들
    path('', MainView.as_view()),
    path('account/',include('account.urls')),
    path('product/',include('product.urls',namespace='product')),
    path('board/',include('board.urls')),

    #Board에서 관리할것들
    # path('board/',BoardListView.as_view()),
    # path('board_upload/',BoardUploadView.as_view()),
    # path('board/<int:pk>/',BoardDetailView.as_view()),
    # path('board/edit/<int:pk>/', bviews.BoardEditView),
    # path('board/delete/<int:pk>/', bviews.BoardDeleteView),
    # path('notice/',NoticeListView.as_view()),
    # path('notice/<int:pk>', NoticeDetailView.as_view())
]

# DEBUG Toolbar
# if settings.DEBUG:
#     mimetypes.add_type("application/javascript", ".js", True)
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
