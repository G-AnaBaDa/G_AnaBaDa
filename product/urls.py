from django.urls import path

from product.views import UploadProduct, productList, myPage,create_comment
from product import views as pviews

urlpatterns= [
    path('upload/', UploadProduct.as_view()),
    path('list/', productList.as_view()),
    path('list/<int:pk>', pviews.productDetail),
    path('edit/<int:pk>/', pviews.editproduct),
    path('delete/<int:pk>/', pviews.deleteproduct),
    path('myPage/', myPage.as_view()),
    path('comment/<int:pk>/',pviews.create_comment)
]