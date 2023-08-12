from django.apps import AppConfig
from django.dispatch import Signal

# 定义信号
task_data_added = Signal()


class WebopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webops'
    verbose_name = '运维管理'
