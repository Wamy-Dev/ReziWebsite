FROM python:3.9-slim
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y chromium x11-utils gnumeric xvfb
ENV CRONMONITORING=healthchecksurl
ENV SEARCHCLIENT=meiliclient
ENV SEARCHCLIENTKEY=meiliclientapikey
CMD ["python", "main.py"]
