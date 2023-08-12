FROM registry.cn-hangzhou.aliyuncs.com/zyyhubs/python-alpine:3.9

# Workdir
WORKDIR /opt/

# Download dependency
RUN pip install django==4.2.4 requests==2.31.0 -i https://pypi.tuna.tsinghua.edu.cn/simple && django-admin startproject PyAutomateOps && cd PyAutomateOps && python manage.py startapp webops && mkdir logs data static templates config

# Workdir
WORKDIR /opt/PyAutomateOps/

# Copy code
ADD config/* config/
ADD PyAutomateOps/* PyAutomateOps/
ADD manage.py ./
ADD webops/* /opt/PyAutomateOps/webops/

# Generate migration file
RUN python manage.py makemigrations && python manage.py migrate

# Exposed port 8000
EXPOSE 8000

# Run program
ENTRYPOINT python manage.py runserver 0.0.0.0:8000
