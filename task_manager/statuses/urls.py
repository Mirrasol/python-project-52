"""
URL configuration for statuses app.

"""
from django.urls import path
from task_manager.statuses.views import (
    IndexView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='statuses_index'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]
