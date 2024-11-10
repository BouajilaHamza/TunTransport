FROM python:3.11-slim
ARG SCRAPING_URL
ARG MONGO_URI

ENV SCRAPING_URL=${SCRAPING_URL}
ENV MONGO_URI=${MONGO_URI}
WORKDIR /Dashboard
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


CMD ["streamlit", "run", "main.py"]
