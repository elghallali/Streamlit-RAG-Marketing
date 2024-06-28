FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ARG GDRIVE_CREDENTIALS_DATA
ARG BASE_URL

ENV GDRIVE_CREDENTIALS=$GDRIVE_CREDENTIALS_DATA
ENV BASE_URL=$BASE_URL

COPY . /app

RUN echo "BASE_URL=$BASE_URL" > /app/.env
RUN mkdir -p /root/.config/gdrive && echo $GDRIVE_CREDENTIALS > /root/.config/gdrive/credentials.json
RUN dvc pull data

ENTRYPOINT ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]


