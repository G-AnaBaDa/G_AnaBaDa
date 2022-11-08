from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .models import Board, Comment
from .models import notice

#커뮤니티 리스트 출력
class BoardListView(ListView):
    model = Board
    template_name = 'community_list.html'
#커뮤니티 게시글 업로드
class BoardUploadView(APIView):
    def get(self,request):
        return render(request,template_name="community_upload.html")

    def post(self,request):

        title = request.POST.get('title')
        content = request.POST.get('summernote')
        user_id = request.user
        Board.objects.create(title=title,content=content,user_id=user_id)

        return redirect('/board/list/')
#공지사항 리스트 출력
class NoticeListView(ListView):
    model = notice
    template_name = 'notice_list.html'
#공지사항 게시글 상세보기
class NoticeDetailView(DetailView):
    model = notice
    template_name = 'notice_detail.html'
#커뮤니티 게시글 상세보기
class BoardDetailView(DetailView):
    model = Board
    template_name = 'community_detail.html'
#커뮤니티 게시글 수정하기
def BoardEditView(request,pk):
    edit_board = Board.objects.get(id=pk)
    if request.method == 'POST':
        edit_board.title = request.POST['title']
        edit_board.content = request.POST['summernote']
        edit_board.save()
        return redirect('/board/list/')
    return render(request,'community_edit.html',{'board':edit_board})
#커뮤니티 게시글 삭제하기
def BoardDeleteView(request,pk):
    delete_board = Board.objects.get(id=pk)
    delete_board.delete()
    return redirect('/board/list/')

#게시글에 댓글 작성하기
def create_comment(request,pk):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.content = request.POST.get('content')
        comment.board = Board.objects.get(id=pk)
        comment.save()

        return redirect('/board/list')
    return render(request,'community_list.html')

#게시글 검색하기
@csrf_exempt
def board_search(request):
    search_content = request.POST.get('search')
    board = Board.objects.all()
    return render(request,'community_search.html',{'search_content':search_content,'board':board})

