FROM python:3.10

WORKDIR /HGW

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /HGW/requirements.txt
COPY . /HGW/
RUN ls -laht /HGW
ENV PYTHONPATH "${PYTHONPATH}:/HGW"

EXPOSE 8001
EXPOSE 30001

CMD bash start.sh