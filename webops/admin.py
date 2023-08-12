from django.contrib import admin
from webops.models import ops_application, ops_task
from webops.toolfuncs import adminsite_action_publish_tasks

# 修改站点信息
admin.site.site_title = '运维管理系统'
admin.site.site_header = 'WebOps System'
admin.site.index_title = '管理后台'

# 添加动作信息
adminsite_action_publish_tasks.short_description = "触发"


# 注册
@admin.register(ops_application)
class ops_application_Admin(admin.ModelAdmin):
    # 分页
    list_per_page = 10

    # 动作执行属性
    actions_on_top = False    # 默认为True
    actions_on_bottom = True  # 默认为False

    list_display = ['app_name', 'app_platform', 'app_webhook']     # 显示列属性
    list_filter = ['app_platform']                                 # 过滤器
    search_fields = ['app_name']                                   # 搜索框

    fieldsets = (
        ('基础信息', {'fields': ['app_name', 'app_platform', 'app_webhook']}),
        ('高级选项', {
            'fields': ['app_token'],
            'classes': ('collapse',)                               # 设置是否折叠显示
        })
    )


# 注册
@admin.register(ops_task)
class ops_task_Admin(admin.ModelAdmin):
    # 分页
    list_per_page = 10

    # 动作执行属性
    actions_on_top = False    # 默认为True
    actions_on_bottom = True  # 默认为False

    # 显示列属性
    list_display = ['application', 'ops_parameters', 'ops_date', 'ops_status']   # 显示列属性
    list_filter = ['application']                                                # 过滤器
    search_fields = ['application']                                              # 搜索框

    fieldsets = (
        ('基础信息', {'fields': ['application', 'ops_parameters']}),
    )

    # 添加动作
    actions = [adminsite_action_publish_tasks]
