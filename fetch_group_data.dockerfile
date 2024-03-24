FROM python:3.9

RUN apt-get update; apt-get install -y dnsutils

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /var/vps_status
RUN touch /var/vps_status/status.db

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"

COPY . .

CMD ["python", "./src/vps_status_fetch_group/main.py"]