FROM python:3.11

WORKDIR /app
COPY . /app
RUN pip install -i "https://mirrors.aliyun.com/pypi/simple/" -r requirements.txt
ENV ENV=prod

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
