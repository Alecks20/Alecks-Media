FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /app/uploads

EXPOSE 80

CMD ["python3","app.py"]