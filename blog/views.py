from django.shortcuts import render , get_object_or_404 , redirect
from django.http import Http404 , HttpResponse
from blog.models import *
from blog.forms import *
from django.views.decorators.http import require_POST
#from django.core.paginator import Paginator,EmptyPage ,  PageNotAnInteger
from django.views.generic import ListView , DetailView
from django.db.models import Sum

def index(request):
    rt = Post.published.aggregate(Sum('reading_time'))['reading_time__sum']
    lp=Post.published.order_by('publish')[:5]
    context = {
        'rt':rt,
        'lp':lp
    }
    return render(request,'blog/index.html',context=context)



#def post_list(request):
 #   posts=Post.published.all()
  #  paginator=Paginator(posts,2)
   # page_number=request.GET.get('page',1)
    #try:
     #   posts=paginator.page(page_number)
    #except EmptyPage:
     #   posts=paginator.page(paginator.num_pages)
    #except PageNotAnInteger:
     #   posts=paginator.page(1)
    #contex={
     #   'posts':posts
    #}
   # return render(request,"blog/list.html",contex)


def post_detail(request,id):
    post=get_object_or_404(Post,id=id,status=Post.Status.Published)
    comments=post.comments.filter(active=True)

    form = CommentForm()
    context={
       'post':post,
       'form':form,
       'comments':comments,

    }
    return render(request,'blog/detail.html',context)



class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 4
    template_name = 'blog/list.html'
    context_object_name = 'posts'

#class PostDetailView(DetailView):
#    model = Post
#    template_name = 'blog/detail.html'

def ticket(request):

    if request.method =='POST':
        form=TicketForm(request.POST)
        if  form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'],name=cd['name'],email=cd['email'],
                                               phone=cd['phone'],subject=cd['subject'])
            return redirect('blog:index')

    else :
        form = TicketForm()
    return render(request,'forms/ticket.html',{'form': form})


@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.Published)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
    context ={
        'post':post,
        'form':form,
        'comment':comment
    }
    return render(request,'forms/comment.html',context)
