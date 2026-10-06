from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
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
    
class TaskListAPIView(APIView):

    def get(self, request):
        tasks = Task.objects.filter(owner=request.user)

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    

class TaskDetailAPIView(APIView):
    
    def get_task(self, pk, user):
        return get_object_or_404(
            Task,
            id=pk,
            owner=user
        )
        
    def get(self, request, pk):
        task = self.get_task(pk, request.user)
        
        serializer = TaskSerializer(task)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_task(pk, request.user)
        
        serializer = TaskSerializer(
            task,
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=400
        )
        
    def patch(self, request, pk):
        task = self.get_task(pk, request.user)
        
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=400
        )
        
    def delete(self, request, pk):
        task = self.get_task(pk, request.user)
        
        task.delete()
        
        return Response(status=204)
    
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        ]
    filterset_fields = ['completed']
    
    search_fields = [
        'title',
        'description',
        ]
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        