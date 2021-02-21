from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from notice.models import Notice, Board
from notice.forms import WriteForm
from django.urls import reverse
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q

def main(request):  # 메인페이지
    Notice_List = Notice.objects.order_by('-id')[0:5] # 공지사항 최신순 5개
    Board_List = Board.objects.order_by('-id')[0:5] # 게시글 최신순 5개

    return render(request, 'notice/main.html', {'NoticeList': Notice_List, 'BoardList': Board_List})

class BoardListView(ListView): # 게시글
    model = Board
    paginate_by = 10 # 페이지당 게시글 수
    template_name = 'notice/board.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'board_list'        #DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        board_list = Board.objects.order_by('-id') 

        if search_keyword :
            if len(search_keyword) > 0 :    # 1글자 이상 검색 (변경시 get_context_data의 len(search_keyword)도 같이 변경)
                if search_type == 'all':
                    search_board_list = board_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (author__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_board_list = board_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_board_list = board_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_board_list = board_list.filter(content__icontains=search_keyword)    
                elif search_type == 'author':
                    search_board_list = board_list.filter(author__icontains=search_keyword)

                return search_board_list

        return board_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # 페이징 ex)[1, 2, 3, 4, 5] 
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 0 :
            context['q'] = search_keyword
        context['type'] = search_type

        return context

def boadet(request, pk):
    board = get_object_or_404(Board, id=pk)
    board.hits += 1
    board.save()

    return render(request, 'notice/boadet.html', {'board':board})

def boadel(request, pk):
    if request.method == 'POST':
        board = get_object_or_404(Board, id=pk)
        if board.password == request.POST['password']:
            board.delete()
            return HttpResponseRedirect(reverse('notice:board'))
        else:
            return render(request, 'notice/boadet.html', {'board':board, 'error_message': "비밀번호 오류"})
    
    elif request.method == 'GET':
        return HttpResponseRedirect(reverse('notice:boadet', args = (pk,)))


class NoticeListView(ListView): # 공지사항
    model = Notice
    paginate_by = 10
    template_name = 'notice/notice.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'notice_list'        #DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = Notice.objects.order_by('-id') 

        if search_keyword :
            if len(search_keyword) > 0 :
                if search_type == 'all':
                    search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_notice_list = notice_list.filter(content__icontains=search_keyword)    
                return search_notice_list

        return notice_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 0 :
            context['q'] = search_keyword
        context['type'] = search_type

        return context

def notdet(request, pk):
    notice = get_object_or_404(Notice, id=pk)
    notice.hits += 1
    notice.save()

    return render(request, 'notice/notdet.html', {'notice':notice})

def write(request): # 글 쓰기
    if request.method == 'GET':
        form = WriteForm()

        return render(request, 'notice/write.html', {'form': form})
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        content = request.POST['content']
        image = request.FILES.get('image')
        password = request.POST['password']
        
        new_post = Board.objects.create(
            title = title,
            author = author,
            content = content,
            image = image,
            password = password
        )
        new_post.save()
            
        return HttpResponseRedirect(reverse('notice:board'))
