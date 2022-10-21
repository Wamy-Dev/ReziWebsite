FROM python:3.9-slim
COPY . .
RUN pip install -r requirements.txt
ENV CRONMONITORING=healthchecksurl
ENV SEARCHCLIENT=meiliclient
ENV SEARCHCLIENTKEY=meiliclientapikey
CMD ["python", "main.py"]
