from django.http import HttpResponse
from django.views import View
from webops.toolfuncs import querydict_to_dict
from webops.toolfuncs import add_task
from webops.toolfuncs import trigger_gitlab_pipeline
from webops.toolfuncs import dingtalk_msg_sign_auth
from webops.toolfuncs import dingtalk_request_parameter_acquisition
from webops.toolfuncs import send_message_to_dingtalk
from webops.toolfuncs import ops_logger

logger = ops_logger()


# Post请求触发流水线视图
class post_trigger_gitlab_pipeline_view(View):
    def get(self, request):
        return HttpResponse('no get request method, call post request!')

    def post(self, request):
        try:  # 获取请求参数
            app, params, refname = querydict_to_dict(request.POST)
        except Exception:
            logger.error('[Post trigger] gets the request parameter error!')
            return HttpResponse('gets the request parameter error!')

        try:  # 触发流水线
            trigger_gitlab_pipeline(appname=app, post_params=params, refname=refname)
        except Exception:
            logger.error('[Post trigger] trigger pipeline error!')
            return HttpResponse('trigger pipeline error!')

        try:  # 添加任务到表
            add_task(appname=app, post_params=params, refname=refname)
            send_message_to_dingtalk(app=app, refname=refname)
            logger.info('[Post trigger] {} application triggering succeeded.'.format(app))
            return HttpResponse('add task success.')
        except Exception:
            logger.error('[Post trigger] add a task to database ops_task table error!')
            return HttpResponse('add a task to database ops_task table error!')


# Chat请求触发流水线视图
class chat_trigger_gitlab_pipeline_view(View):
    def get(self, request):
        return HttpResponse('no get request method, call post request!')

    def post(self, request):
        # 钉钉消息合法性认证
        if not dingtalk_msg_sign_auth(request) is True:
            logger.error('[Chat trigger] the request from dingtalk is illegal!')
            return HttpResponse('the request from dingtalk is illegal!')

        try:  # 获取请求参数
            app, params, refname = dingtalk_request_parameter_acquisition(request)
        except Exception:
            logger.error('[Chat trigger] gets the request parameter error!')
            return HttpResponse('gets the request parameter error')

        try:  # 触发流水线
            trigger_gitlab_pipeline(appname=app, post_params=params, refname=refname)
        except Exception:
            logger.error('[Chat trigger] trigger pipeline error!')
            return HttpResponse('trigger pipeline error!')

        try:  # 添加任务到表
            add_task(appname=app, post_params=params, refname=refname)
            send_message_to_dingtalk(app=app, refname=refname)
            logger.info('[Chat trigger] {} application triggering succeeded.'.format(app))
            return HttpResponse('add task success.')
        except Exception:
            logger.error('[Chat trigger] add a task to database ops_task table error!')
            return HttpResponse('add a task to database ops_task table error!')
