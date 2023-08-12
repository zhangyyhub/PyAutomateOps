# PyAutomateOps/webops/urls.py

from django.urls import path
from webops import views

urlpatterns = [
    # Post请求触发Gitlab流水线
    path('post_trigger_gitlab_pipeline/', views.post_trigger_gitlab_pipeline_view.as_view(), name='post_trigger_gitlab_pipeline'),

    # Chat请求触发Gitlab流水线
    path('chat_trigger_gitlab_pipeline/', views.chat_trigger_gitlab_pipeline_view.as_view(), name='chat_trigger_gitlab_pipeline'),
]
