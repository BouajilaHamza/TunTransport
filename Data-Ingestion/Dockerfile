FROM python:3.11 

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt\
&& cat /usr/local/lib/python3.11/site-packages/scrapyd/default_scrapyd.conf\
&& sed -i '/^bind_address/s/127.0.0.1/0.0.0.0/' /usr/local/lib/python3.11/site-packages/scrapyd/default_scrapyd.conf 

CMD ["scrapyd"]