from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .models import User


# id, account_id, password, email, nickname, name, phone_number

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

        context = {}

        if User.objects.filter(account_id=account_id).exists():
            return render(request, 'idexist.html', {'account_id': account_id})

        User.objects.create_user(account_id=account_id, password=password, name=name, email=email, nickname=nickname,
                              phone_number=phone_number)

        return render(request, 'signup_ok.html', {'account_id': account_id})

#로그인
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        account_id = request.POST.get('account_id')
        password = request.POST.get('password')
        user = authenticate(request, username=account_id, password=password)
        if user is not None: # 올바른 로그인 정보 입력시.
            request.session['id'] = account_id  # 여기서 세션값에 멤버id와 이름이 넘어감
            request.session['name'] = request.POST.get('name')
            auth.login(request, user)
            return redirect('/') #위에서 로그인해서 세션값 가지고 redirect됨
        else:  # 들어온값이 db없으면.
            return render(request, "login.html", {'error':'Username or Password is incorrect',})

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
        if account_id:
            return render(request, 'main.html')
        return render(request, 'base_page.html')

#아이디 찾기
class FindId(APIView):
    def get(self,request):
        return render(request, 'find_account.html')
    def post(self,request):
        email = request.data.get('email')
        E = User.objects.filter(email=email)
#E가 있는객체인지, 빈 객체인지는  결과 템플릿에서 if문에 나눠서 출력할것임
        return render(request, 'find_accountOK.html', {'E':E})
