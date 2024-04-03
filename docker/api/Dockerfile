FROM python:3.10

WORKDIR /usr/src
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y default-jdk
ADD requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]