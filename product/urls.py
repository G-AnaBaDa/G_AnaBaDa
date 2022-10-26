from django.urls import path

from product.views import UploadProduct, productList, myPage, create_comment, product_search, create_sendbird_group_channel,Chat
from product import views as pviews, views
app_name = 'product'
urlpatterns= [
    path('upload/', UploadProduct.as_view()),
    path('list/', productList.as_view()),
    path('search/', views.product_search),
    path('list/<int:pk>', pviews.productDetail),
    path('edit/<int:pk>/', pviews.editproduct),
    path('delete/<int:pk>/', pviews.deleteproduct),
    path('myPage/', myPage.as_view()),
    path('comment/<int:pk>/',pviews.create_comment),
    path('like/', views.product_like, name= 'product_like'),
    path('create_chat/<int:pk>/', create_sendbird_group_channel),
    path('send_message/', Chat.as_view())
]