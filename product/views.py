import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework.views import APIView
from .models import Product, Comment
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN


# 마이 페이지
class myPage(APIView):
    def get(self, request):
        myItem = Product.objects.filter(writer_id=request.session.get('id'))
        # 내 세션(나의 id)id값이 product DB에 저장된 writer_id와 일치하는것만 가져오기
        products = Product.objects.filter(like_user=request.session.get('id'))
        #찜한 상품 가져오는 products
        return render(request, 'Mypage.html', {'myItem': myItem,'products':products})


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
        photo1 = request.FILES.get('photo1')
        photo2 = request.FILES.get('photo2')
        photo3 = request.FILES.get('photo3')
        Product.objects.create(title=title, category=category, content=summernote, location=location, hashtag=hashtag,writer=user_id,photo1=photo1,photo2=photo2,photo3=photo3)
        return redirect('/product/list/')

#채팅하기
class Chat(APIView):
    def get(self, request):
        return render(request, template_name='chat_room.html')
    def post(self, request):
        message = request.POST.get('message')
        url = f"https://api-{application_id}.sendbird.com/v3/group_channels"
        api_headers = {"Api-Token": sendbird_api_token}
        now_user = str(request.session.get('id'))
        global arr
        chat_user = arr[-1]
        data = {
            "inviter_id": now_user,
            "user_ids": [now_user, chat_user],
            "is_distinct": True,
        }
        res = requests.post(url, headers=api_headers, data=json.dumps(data))
        res_data = json.loads(res._content.decode("utf-8"))
        chanel_url = res_data.get('channel_url')
        # print(chanel_url)
        message_url = f"https://api-{application_id}.sendbird.com/v3/group_channels/{chanel_url}/messages"
        data = {
            'message_type': 'MESG',
            'user_id': now_user,
            'message': message
        }
        message_res = requests.post(message_url, headers=api_headers, data=json.dumps(data))
        message_data = json.loads(message_res._content.decode("utf-8"))
        message_ts = message_data['created_at']
        # print(message_ts)
        message_list_url = f'https://api-{application_id}.sendbird.com/v3/group_channels/{chanel_url}/messages?message_ts={message_ts}&prev_limit=200'
        message_list = requests.get(message_list_url, headers=api_headers)
        message_list_res = json.loads((message_list._content.decode("utf-8")))
        return render(request, 'chat_room.html', {'message_list2': message_list_res})

# 상품 수정하기
def editproduct(request, pk):
    edit_product = Product.objects.get(id=pk)
    if request.method == 'POST':
        edit_product.title = request.POST['title']
        edit_product.category = request.POST['category']
        edit_product.content = request.POST['summernote']
        edit_product.location = request.POST['location']
        edit_product.hashtag = request.POST['hashtag']
        edit_product.photo1 = request.FILES.get('photo1')
        edit_product.photo2 = request.FILES.get('photo2')
        edit_product.photo3 = request.FILES.get('photo3')
        edit_product.save()
        return redirect('/product/list/')
    return render(request,'product_edit.html',{'product': edit_product})

#상품 삭제하기
def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/product/list/')

# 상품 리스트 출력
class productList(ListView):
    model = Product
    template_name = 'product_list.html'

# 상품 상세보기 + 조회수 기능 추가
def productDetail(request, pk):
    product = get_object_or_404(Product, id=pk)
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

arr = []

#샌드버드 채팅 api
@login_required
def create_sendbird_group_channel(request, pk):
    try:
        url = f"https://api-{application_id}.sendbird.com/v3/group_channels"
        api_headers = {"Api-Token": sendbird_api_token}
        now_user = request.session.get('id')
        chat_user = str(Product.objects.get(id=pk))
        # print(chat_user)
        global arr
        arr.append(chat_user)
        data = {
            "inviter_id": now_user,
            "user_ids": [now_user, chat_user],
            "is_distinct": True,
        }
        res = requests.post(url, headers=api_headers, data=json.dumps(data))
        res_data = json.loads(res._content.decode("utf-8"))
        channel_url = res_data.get('channel_url')
        message_ts = res_data['created_at']
        message_list_url = f"https://api-{application_id}.sendbird.com/v3/group_channels/{channel_url}/messages?message_ts={message_ts}&prev_limit=200"
        message_list = requests.get(message_list_url, headers=api_headers)
        # print(arr)
        message_list_res = json.loads(message_list._content.decode("utf-8"))
    except AttributeError:
        pass
    return render(request, 'chat_room.html', {'message_list1': message_list_res})

# 상품 게시글 댓글 작성
@login_required
def create_comment(request, pk):
    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST.get('content')
        comment.user = request.user
        comment.product = Product.objects.get(id=pk)
        comment.save()
        return redirect('/product/list/')
    return render(request,'product_list.html')


#상품 좋아요 기능
@login_required
@require_POST
def product_like(request):
    pk = request.POST.get('pk', None)
    product = get_object_or_404(Product, pk=pk)
    user = request.user

    if product.like_user.filter(account_id=user).exists():
        product.like_user.remove(user)
        message = '좋아요 취소'
    else:
        product.like_user.add(user)
        message = '좋아요'

    context = {'like_count': product.count_like_user(), 'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")

#상품 검색하기
@csrf_exempt
def product_search(request):
    search_content = request.POST.get('search')
    products = Product.objects.all()
    return render(request,'product_search.html',{'search_content':search_content,'products':products})