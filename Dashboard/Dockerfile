FROM python:3.11
ARG SCRAPING_URL
ARG MONGO_URI

ENV SCRAPING_URL=${SCRAPING_URL}
ENV MONGO_URI=${MONGO_URI}
WORKDIR /dashboard
COPY . .


RUN pip install -r requirements.txt
CMD ["streamlit", "run", "main.py"]
