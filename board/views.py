from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework.views import APIView

from account.models import User
from board.models import Board

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
