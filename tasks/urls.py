from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from .views import(
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskViewSet,
)


app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),

    path('create/', TaskCreateView.as_view(), name='task_create'),

    path('<int:pk>/edit/',TaskUpdateView.as_view(), name='task_update'),

    path('<int:pk>/delete/',TaskDeleteView.as_view(), name='task_delete'),
    
    path('api/tasks/', TaskListAPIView.as_view(), name='api_task_list'),
    
    path('api/tasks/<int:pk>/',
         TaskDetailAPIView.as_view(),
         name='api_task_detail'
         ),
]

router = DefaultRouter()

router.register(
    'api/viewset/tasks',
    TaskViewSet,
    basename='task'
    )

urlpatterns += router.urls