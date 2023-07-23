from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .models import Post, Response, User
from django.urls import reverse_lazy, reverse
from .forms import PostForm, ResponseForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
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

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, Form):
        Form.instance.author = User.objects.get(username=self.request.user)
        return super().form_valid(Form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('board')


class ResponsePost (LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'
    context_object_name = 'response'

    def form_valid(self, Form):
        Form.instance.resp_post = Post.objects.get(id=self.kwargs['pk'])
        Form.instance.resp_author = self.request.user
        return super().form_valid(Form)


class ResponseList (LoginRequiredMixin, ListView):
    model = Post
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user).all()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *arg,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses')


@login_required
def response_accept(request, pk):
    resp_context = Response.objects.get(id=pk)
    if resp_context.status == False:
        resp_context.status = True
        resp_context.save(update_fields=['status'])
        message = "Вы ответили на отклик:"
    else:
        message = "Вы уже ответили на этот отклик!"
    return render(request, 'saveresp.html', {'response': resp_context, 'message': message})

