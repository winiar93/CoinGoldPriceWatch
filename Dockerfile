# Specify a base image

FROM python:3.9

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY /app /app


EXPOSE 5000
CMD ["python", "asset_mint.py"]

