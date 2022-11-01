from datetime import timedelta, datetime
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .models import User
from django.conf import settings
import json
import requests
from .models import SendBirdSessionToken
from product.models import Product

application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN

# 회원가입
class Register(APIView):
    def get(self, request):
        template_name = 'signup.html'
        return render(request, template_name)

    def post(self, request):
        account_id = request.data.get('account_id', "")
        email = request.data.get('email', "")
        nickname = request.data.get('nickname', "")
        name = request.data.get('name', "")
        phone_number = request.data.get('phone_number', "")
        password = request.data.get('password', "")

        if User.objects.filter(account_id=account_id).exists():
            return render(request, 'signup_exist.html', {'account_id': account_id})

        User.objects.create_user(account_id=account_id, password=password, name=name, email=email, nickname=nickname,
                                 phone_number=phone_number)

        # 회원가입시 sendbird에 유저를 동시에 같은 ID로 생성시킴
        def create_sendbird_user(user_id, nickname, profile_url=""):
            url = f"https://api-{application_id}.sendbird.com/v3/users"
            api_headers = {"Api-Token": sendbird_api_token}
            data = {
                "user_id": user_id,
                "nickname": nickname,
                "profile_url": profile_url,
            }
            res = requests.post(url, data=json.dumps(data), headers=api_headers)
            res_data = json.loads(res._content.decode("utf-8"))
            return json.dumps(res_data)

        create_sendbird_user(account_id, nickname, profile_url="")
        return render(request, 'signup_ok.html', {'account_id': account_id})

# 로그인
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        account_id = request.POST.get('account_id')
        password = request.POST.get('password')
        user = authenticate(request, username=account_id, password=password)

        # 로그인과 동시에 채팅을 위해 필요한 샌드버드 user token을 발급받음
        def create_sendbird_user_session_token(user_id):
            url = f"https://api-{application_id}.sendbird.com/v3/users"
            api_headers = {"Api-Token": sendbird_api_token}
            get_user_res = requests.get(
                f"{url}/{user_id}", headers=api_headers
            )
            if get_user_res.status_code == 200:
                now = datetime.now()
                four_weeks_later = now + timedelta(weeks=4)
                expireds_time = int(round(time.mktime(four_weeks_later.timetuple()) * 1000))
                url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}/token"
                api_headers = {"Api-Token": sendbird_api_token}
                # expire_date = datetime.now() + timedelta(days=365)
                # invert_expire_date = f"{invert_timestamp(expire_date)}000"
                data = {
                    "expires_at": expireds_time
                }
                res = requests.post(url, headers=api_headers, data=json.dumps(data))
                res_data = json.loads(res._content.decode("utf-8"))
                print(res_data)
                SendBirdSessionToken.objects.create(
                    user_id=user,
                    sessionToken=res_data["token"],
                )
                return print(res_data)
            return "sendbird에 유저가 없습니다."

        if user is not None:  # 올바른 로그인 정보 입력시.
            request.session['id'] = account_id  # 여기서 세션값에 멤버id와 이름이 넘어감
            request.session['name'] = request.POST.get('name')
            auth.login(request, user)
            create_sendbird_user_session_token(account_id)
            return redirect('/')  # 위에서 로그인해서 세션값 가지고 redirect됨
        else:  # 들어온값이 db없으면.
            return render(request, "login.html", {'error': 'Username or Password is incorrect', })

#로그아웃
class Logout(APIView):
    def get(self, request):
        auth.logout(request)
        return redirect('/')  #세션 X상태이기때문에 main가면 base_page.html찾아감

#홈화면
class MainView(APIView):
# main페이지는 두가지로 나뉨. 세션값 가지고 들어가는 main.html과 세션값 없는 base_page.html
# main.html에는 context ={}를 통해 나중에 회원정보 하나하나 넘겨줄수있음
    def get(self, request):
        account_id = request.session.get('id')
        products = Product.objects.all().order_by('-count')
        _context = {'check': False}

        # G_아나바다 계정로그인된 경우
        if account_id:
            return render(request, 'main.html', {'products': products})

        # 카톡 계정 로그인 됐을때(아래 access_token이 카톡 토큰임)
        elif request.session.get('access_token'):
            _context['check'] = True
            context = {'products': products, '_context': _context}
            return render(request, 'main.html', {'context': context})
        # 아무 계정도 로그인 안됐을때
        else:
            return render(request, 'Base_page.html', {'products': products})

#아이디 찾기
class FindId(APIView):
    def get(self, request):
        return render(request, 'find_Id.html')
    def post(self, request):
        email = request.data.get('email')
        E = User.objects.filter(email=email)
        # E가 있는객체인지, 빈 객체인지는  결과 템플릿에서 if문에 나눠서 출력할것임
        return render(request, 'find_Id_result.html', {'E': E})


# 카카오 로그인


def kakaoLoginLogic(request):
    # 입력필요
    _restApiKey = '223ec240f24b6c90a9f568470a777b7f'
    _redirectUrl = 'http://127.0.0.1:8000/account/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)


def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '223ec240f24b6c90a9f568470a777b7f'  # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/account/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    products = Product.objects.all()
    request.session.get('access_token')
    _context = {'check': True}
    context = {'products': products, '_context': _context}
    return render(request, 'main.html',{'context':context})


def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
        'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    products = Product.objects.all()

    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'Base_page.html',{'products':products})


