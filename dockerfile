FROM python:3.9-slim
COPY . .
RUN pip install -r requirements.txt
ENV CRONMONITORING=healthchecksurl
ENV SEARCHCLIENT=meiliclient
ENV SEARCHCLIENTKEY=meiliclientapikey
ENV DISCORDWEBHOOK=discordwebhookurl
ENV GAMEBOUNTY_API_KEY=gamebountyapikey
CMD ["python", "main.py"]
