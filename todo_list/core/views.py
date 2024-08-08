from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    fields = "__all__"
    redirect_authenticated_url = True  # for check user who was login

    # def get_success_url(self):
    #     return reverse_lazy("tasks")

class RegisterView(FormView):
    template_name = 'core/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')  # reverse_lazy is important here.

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):  # it searches for task_list.html
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)  # when we need to use info about whom that login at site
        context['count'] = context['tasks'].filter(complete=False).count()
        filter_value = self.request.GET.get('filterBy') or ''

        if filter_value:
            context['tasks'] = context['tasks'].filter(title__icontains=filter_value)

        context['filter_value'] = filter_value

        return context

class TaskDetail(LoginRequiredMixin, DetailView):  # it searches for task_detail.html
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):  # it searches for task_form.html
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  # revers lazy forward our page to our mention urls in('name=....')

    def form_valid(self, form):
        form.instance.user = self.request.user  # it gives to us the user info & we don't need the user field in form
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):  # it searches for task_form.html
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
