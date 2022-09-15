from cgitb import html

from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from rest_framework.views import APIView
from .models import Product,Comment
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
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
        summernote = request.POST.get('summernote')
        user_id = request.user
        location = request.POST.get('location')
        hashtag = request.POST.get('hashtag')
        Product.objects.create(title=title, category=category, content=summernote, location=location, hashtag=hashtag,writer=user_id)
        return redirect('/product/list/')

def editproduct(request,pk):
    edit_product = Product.objects.get(id=pk)
    if request.method == 'POST':
        edit_product.title = request.POST['title']
        edit_product.category = request.POST['category']
        edit_product.content = request.POST['summernote']
        edit_product.location = request.POST['location']
        edit_product.hashtag = request.POST['hashtag']
        edit_product.save()
        return redirect('/product/list/')
    return render(request,'product_edit.html',{'product': edit_product})

def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return redirect('/product/list/')

# 상품 게시판
class productList(ListView):
    model = Product
    template_name = 'product_list.html'

# 상품 상세보기 + 조회수 기능 추가 
def productDetail(request,pk):
    product = get_object_or_404(Product, id=pk)
    template_name = 'product_detail.html'
    response = render(request, 'product_detail.html', {'product':product })
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0,minute=0,second=0,microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('countcookie','')

    if f'{pk}' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('countcookie', value=cookie_value, max_age=max_age,httponly=True)
        product.count += 1
        product.save()
    return response



@login_required
def create_comment(request,pk):
    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('content')
        comment.user = request.user
        comment.product = Product.objects.get(id=pk)
        comment.save()

        return redirect('/product/list/')
    return render(request,'product_list.html')


