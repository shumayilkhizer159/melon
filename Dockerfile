FROM python:3.7.5-slim

RUN apt update
RUN apt install -y python3-dev gcc

ADD requirements.txt requirements.txt
ADD Melanoma95.h5 Melanoma95.h5
ADD app.py app.py

# Install required libraries
RUN pip install -r requirements.txt

# Run it once to trigger resnet download
RUN python app.py

EXPOSE 8008

# Start the server
CMD ["python", "app.py", "serve"]