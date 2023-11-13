FROM python:3.11.6-slim-bookworm
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY NOIRS-DOVE.py NOIRS-DOVE.py
CMD ["python3", "NOIRS-DOVE.py"]