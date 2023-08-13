## 简介
Python 自动化运维工具，基于 apifox, web 和 dingtalk chat。



## 数据库信息

基于 SQLite3 嵌入式的关系型数据库管理系统来存储系统数据，它是一个轻量级、服务器无关、零配置的数据库引擎。与传统的客户端服务器模式的数据库不同，SQLite3 数据库引擎以库的形式嵌入到应用程序中，不需要独立的服务器进程。



**ops_application:** 

| 字段         | 类型                        | 说明                      |
| ------------ | --------------------------- | ------------------------- |
| app_name     | CharField（max_length=50）  | 应用名称                  |
| app_platform | CharField（max_length=50）  | 所属平台                  |
| app_token    | CharField（max_length=500） | gitlab or jenkins token   |
| app_webhook  | CharField（max_length=500） | gitlab or jenkins webhook |
| app_date     | DateTimeField               | 创建时间                  |



**ops_task:** 

| 字段           | 类型                        | 说明                        |
| -------------- | --------------------------- | --------------------------- |
| ops_parameters | CharField（max_length=500） | 参数选项                    |
| ops_date       | DateTimeField               | 创建时间                    |
| ops_status     | BooleanField                | 任务状态                    |
| application    | ForeignKey                  | 外键关联 ops_application 表 |



## 业务的部署

构建镜像：

```bash
$ docker build -t py-automateops:1.0 .
```



业务部署：

```bash
"create docker volume"
$ docker volume create automateops_config
$ docker volume create automateops_data
$ docker volume create automateops_logs

"deployment automateops app"
$ docker run -d --name automateops -p 8000:8000 \
-v automateops_config:/opt/PyAutomateOps/config \
-v automateops_data:/opt/PyAutomateOps/data \
-v automateops_logs:/opt/PyAutomateOps/logs \
py-automateops:1.0

"create django superuser"
$ docker exec -it automateops /bin/sh
/opt/PyAutomateOps # python manage.py createsuperuser
用户名 (leave blank to use 'root'): admin
电子邮件地址: admin@outlook.com
Password: 
Password (again): 
密码跟 用户名 太相似了。
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
/opt/PyAutomateOps # exit
```



更改配置：需要在钉钉开放平台 - 企业内部开发 - 发布自定义机器人（出口 IP、[消息接受地址](http://IP:8000/webops/chat_trigger_gitlab_pipeline/)）

```bash
"edit automateops app config"
$ vim /var/lib/docker/volumes/automateops_config/_data/config.ini
[webops]
dingtalk_robot_token = ******
dingtalk_robot_secret = ******

"restart automateops app"
$ docker restart automateops
```

