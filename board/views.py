from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .models import Board
from .models import notice

class BoardListView(ListView):
    model = Board
    template_name = 'community_list.html'

class BoardUploadView(APIView):
    def get(self,request):
        return render(request,template_name="community_upload.html")

    def post(self,request):

        title = request.POST.get('title')
        content = request.POST.get('summernote')
        user_id = request.user
        Board.objects.create(title=title,content=content,user_id=user_id)


        return render(request,'main.html')

class NoticeListView(ListView):
    model = notice
    template_name = 'notice_list.html'

class NoticeDetailView(DetailView):
    model = notice
    template_name = 'notice_detail.html'
