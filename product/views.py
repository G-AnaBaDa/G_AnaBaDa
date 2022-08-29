from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .models import Product

# 마이 페이지
class myPage(APIView):
    def get(self, request):
        name = request.session.get('name')
        myItem = Product.objects.filter(writer_id=request.session.get('id'))
        # 내 세션(나의 id)id값이 product DB에 저장된 writer_id와 일치하는것만 가져오기
        return render(request, 'mypage.html', {'myItem': myItem})

# 상품 업로드
class UploadProduct(APIView):
    def get(self, request):
        return render(request, template_name='product_upload.html')

    def post(self, request):
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        # writer = request.POST.get('writer')
        location = request.POST.get('location')
        hashtag = request.POST.get('hashtag')
        Product.objects.create(title=title, category=category, content=content, location=location, hashtag=hashtag)
        return render(request, 'main.html')

# 상품 게시판
class productList(ListView):
    model = Product
    template_name = 'product_list.html'

# 상품 상세보기
class productDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
