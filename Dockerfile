FROM python:3.9.1

ADD ./requirements.txt ./

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

RUN pip install -r ./requirements.txt

RUN pip install -U flask-cors

RUN pip install opencv-python
