from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
    name = "Yusuf"
    
    tasks = [ 
             "learn Django",
             "Build a REST API",
             "Learn PostgreSQL",
    ]
    
    return render(
        request,
        'tasks/home.html',
        {
            'name': name,
            'tasks': tasks
        }
    )

def about(request):
    return HttpResponse("This is my Task Manager About pagr.")

def tasks(request):
    return HttpResponse("This is my Tasks page.")

def task_detail(request, id):
    return HttpResponse(f"Task ID: {id}")

def product_detail(request, id):
    return HttpResponse(f"Product ID: {id}")

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = '/tasks/'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        response = super().form_valid(form)
    
        messages.success(
            self.request,
            "Task created successfully!"
        )
        
        return response
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = '/tasks/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            "Task updated successfully!"
        )
        
        return response
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = '/tasks/'
    
    def form_valid(self, form):
        response =super().form_valid(form)
        
        messages.success(
            self.request,
            "Task deleted successfully!"
        )
        
        return response
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


@login_required  
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            
            
            return redirect('tasks:task_list')
        
    else:
        form = TaskForm()
        
    return render(
        request,
        'tasks/task_form.html',
        {'form': form}
    )
    
@login_required
def task_update(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        owner=request.user
    )
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
        
    else:
        form = TaskForm(instance=task)
        
    
    return render(
        request,
        'tasks/task_form.html',
        {'form': form}
    )

@login_required
def task_delete(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        owner=request.user
    )
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    
    return render(
        request,
        'tasks/task_confirm_delete.html',
        {'task': task}
    )
    
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    
    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks}
    )