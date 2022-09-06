from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .models import Board
from .models import notice
import datetime
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

class BoardDetailView(DetailView):
    model = Board
    template_name = 'community_detail.html'

def BoardEditView(request,pk):
    edit_board = Board.objects.get(id=pk)
    if request.method == 'POST':
        edit_board.title = request.POST['title']
        edit_board.content = request.POST['summernote']
        edit_board.save()
    return render(request,'community_edit.html',{'board':edit_board})

def BoardDeleteView(request,pk):
    delete_board = Board.objects.get(id=pk)
    delete_board.delete()
    return redirect('/board/')