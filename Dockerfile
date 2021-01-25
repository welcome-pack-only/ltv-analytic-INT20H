FROM python:3.8-slim

COPY . /home/root
WORKDIR /home/root

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]