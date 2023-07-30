FROM python:3.9-slim
COPY . .
RUN pip install -r requirements.txt
ENV CRONMONITORING=healthchecksurl
ENV SEARCHCLIENT=meiliclient
ENV SEARCHCLIENTKEY=meiliclientapikey
ENV DISCORDWEBHOOK=discordwebhookurl
CMD ["python", "main.py"]
