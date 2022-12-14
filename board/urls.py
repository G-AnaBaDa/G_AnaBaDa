from django.urls import path

from board.views import NoticeDetailView, NoticeListView, BoardDetailView, BoardUploadView, BoardListView
from board import views as bviews, views

urlpatterns=[
    #자유게시판
    path('list/',BoardListView.as_view()),
    path('upload/',BoardUploadView.as_view()),
    path('list/<int:pk>/',BoardDetailView.as_view()),
    path('edit/<int:pk>/', bviews.BoardEditView),
    path('delete/<int:pk>/', bviews.BoardDeleteView),
    path('search/',views.board_search),
    #공지사항
    path('notice/',NoticeListView.as_view()),
    path('notice/<int:pk>', NoticeDetailView.as_view()),
    path('comment/<int:pk>/',bviews.create_comment)
]