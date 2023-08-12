from django.db import models


# 应用表
class ops_application(models.Model):
    app_name = models.CharField(verbose_name=' 应用名称', max_length=50)
    app_platform = models.CharField(verbose_name='所属平台', max_length=50)
    app_token = models.CharField(verbose_name='Token', max_length=500)
    app_webhook = models.CharField(verbose_name='Webhook', max_length=500)
    app_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ops_application'
        verbose_name = '应用'
        verbose_name_plural = verbose_name  # 不显示复数形式

    def __str__(self):
        target = '{}'.format(self.app_name)
        return target


# 任务表
class ops_task(models.Model):
    ops_parameters = models.CharField(verbose_name='参数选项', max_length=500)
    ops_date = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    ops_status = models.BooleanField(default=False, verbose_name='任务状态')
    application = models.ForeignKey(ops_application, on_delete=models.CASCADE, verbose_name='应用名称')  # 外键关联

    class Meta:
        db_table = 'ops_task'
        verbose_name = '任务'
        verbose_name_plural = verbose_name  # 不显示复数形式

    def __str__(self):
        target = '{}'.format(self.application)
        return target
