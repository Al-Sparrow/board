from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Response, User, Category
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from .forms import PostForm, ResponseForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from datetime import datetime


class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'board.html'
    context_object_name = 'board'
    paginate_by = 5



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'search.html'
    context_object_name = 'Search'
    paginate_by = 5



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'post {self.kwargs["pk"]}', None)
    #
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post_{self.kwargs["pk"]}', obj)
    #     return obj

    def get_context_data(self, *args, **kwargs):
        context_detail = super().get_context_data(**kwargs)
        context_detail['is_author'] = Post.objects.filter(author=self.request.user) #self.request.user.username.get(username=Post.author.username).exists()
        return context_detail


class PostCreate(LoginRequiredMixin, CreateView):
    # permission_required = ('news.add_post',)
    # raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, Form):
        # authorUser = self.request.user.objects.get(id=int(self.kwargs['pk']))
        Form.instance.author = User.objects.get(username=self.request.user)
        return super().form_valid(Form)



class PostUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ResponsePost (LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'


    def form_valid(self, Form):
        Form.instance.resp_post = Post.objects.get(id=int(self.kwargs['pk'])).id
        Form.instance.resp_author = self.request.user.id
        return super().form_valid(Form)


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribe.all()
        context['category'] = self.category
        return context