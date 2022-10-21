from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .models import Board, Comment
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

        return redirect('/board/list/')


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
        return redirect('/board/list/')
    return render(request,'community_edit.html',{'board':edit_board})

def BoardDeleteView(request,pk):
    delete_board = Board.objects.get(id=pk)
    delete_board.delete()
    return redirect('/board/list/')

def create_comment(request,pk):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.content = request.POST.get('content')
        comment.board = Board.objects.get(id=pk)
        comment.save()

        return redirect('/board/list')
    return render(request,'community_list.html')


@csrf_exempt
def board_search(request):
    search_content = request.POST.get('search')
    board = Board.objects.all()
    return render(request,'community_search.html',{'search_content':search_content,'board':board})

