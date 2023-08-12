# -*- coding : utf-8 -*-
# Time       : 2023/8/10 13:56
# Auth       : Yangyang Zhang(张洋洋)
# File       : toolfuncs.py
# Explain    : 业务功能函数封装

import datetime
from webops.models import ops_application, ops_task
from urllib.parse import urlencode
from pathlib import Path
from urllib.parse import parse_qs
import configparser
import requests
import time
import hmac
import base64
import hashlib
import json
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

configfile = Path(__file__).resolve().parent.parent / Path('config/config.ini')

# 创建cfg实例对象
cfg = configparser.ConfigParser()
# 解析cfg配置文件
cfg.read(configfile)

dingtalk_robot_token  = cfg.get('webops', 'dingtalk_robot_token')
dingtalk_robot_secret = cfg.get('webops', 'dingtalk_robot_secret')

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}'.format(Path(__file__).resolve().parent.parent / 'logs/automate-ops.log'),
            'when': 'midnight',         # 每天切割
            'interval': 1,              # 间隔一天
            'backupCount': 7,           # 保留七天
            'formatter': 'standard',
        },
    },
    'loggers': {
        'automate-ops': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}


def ops_logger():
    """
    Log function Function encapsulation.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('automate-ops')
    return logger


def querydict_to_dict(querydict):
    """
    Django querydict object to python dict object.
    """
    result_dict = {}
    for key in querydict.keys():
        if key == 'app' or key == 'ref':
            continue
        result_dict[key] = querydict[key]

    return querydict['app'], result_dict, querydict['ref']


def add_task(appname, post_params, refname):
    """
    Add task to database ops_task table.
    """
    post_params.pop('token')
    post_params['ref'] = refname
    ops_task.objects.create(
        ops_parameters="&".join(["{}={}".format(k, v) for k, v in post_params.items()]),
        ops_date=datetime.datetime.now(),
        ops_status=True,
        application=ops_application.objects.get(app_name=appname),
    )


def adminsite_action_publish_tasks(modeladmin, request, queryset):
    """
    The Admin site triggers the pipeline.
    """
    logger = ops_logger()

    try:
        for task in queryset:
            target = []
            refname = ""

            query_dict = parse_qs(task.ops_parameters)
            for k, v in query_dict.items():
                if k == 'ref':
                    refname = v[0]
                else:
                    target.append('{}={}'.format(k, v[0]))

            target.append("token={}".format(ops_application.objects.get(app_name=str(task)).app_token))
            url = "{}?{}".format(ops_application.objects.get(app_name=str(task)).app_webhook.replace('REF_NAME', refname), "&".join(target))

            requests.post(url, headers=headers)
            send_message_to_dingtalk(app=str(task), refname=refname)
            logger.info('[Web trigger] {} application triggering succeeded.'.format(str(task)))

        # 部署完成将选定任务设置部署状态
        queryset.update(ops_status=True)
    except Exception:
        logger.error('[Web trigger] add a task to database ops_task table error!')


def trigger_gitlab_pipeline(appname, post_params, refname):
    """
    The Post request triggers the pipeline.
    """
    post_params['token'] = ops_application.objects.get(app_name=appname).app_token
    url = "{}?{}".format(ops_application.objects.get(app_name=appname).app_webhook.replace('REF_NAME', refname), urlencode(post_params))

    requests.post(url, headers=headers)


def dingtalk_msg_sign_auth(request):
    """
    Use sign and timestamp to determine whether it is a legitimate request from Dingpin.
    """
    # 当前系统的时间戳
    curt_timestamp = int(time.time() * 1000)
    # 客户端请求时间戳
    http_timestamp = int(request.META.get("HTTP_TIMESTAMP"))

    # 计算当前的签名
    app_secret = dingtalk_robot_secret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(str(http_timestamp), app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    curt_sign = base64.b64encode(hmac_code).decode('utf-8')
    # 客户端请求签名
    http_sign = request.META.get("HTTP_SIGN")

    if abs(curt_timestamp - http_timestamp) < 3600000 and curt_sign == http_sign:
        return True
    else:
        return False


def dingtalk_request_parameter_acquisition(request):
    """
    Gets the parameters of the dingtalk request.
    """
    request_data = json.loads(json.loads(request.body).get('text').get('content').strip())
    params = {}
    appname = ""
    refname = ""
    for k, v in request_data.items():
        if k == 'app':
            appname = v
            continue
        if k == 'ref':
            refname = v
            continue
        params[k] = v

    return appname, params, refname


def send_message_to_dingtalk(app, refname):
    """
    Send a message to dingtalk.
    """
    json_data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'Pipeline',
            'text': '### Gitlab 流水线触发成功!\n --- \n - 项目：{}\n - 分支：{}\n - 状态：<font color= green>{}</font>\n'.format(
                app, refname, 'Successful!'),
        },
    }
    params = {'access_token': dingtalk_robot_token}
    requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
