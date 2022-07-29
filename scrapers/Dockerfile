# Specify a base image

FROM python:3.9

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /scrapers

COPY . .


#EXPOSE 5000
CMD ["python3", "scrapers/asset_mint.py"]