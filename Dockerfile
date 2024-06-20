FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

# Update pip to the latest version
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]

CMD ["App.py"]
