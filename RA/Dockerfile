FROM python:3.10

WORKDIR /RA

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /RA/requirements.txt
COPY . /RA/
RUN ls -laht /RA
ENV PYTHONPATH "${PYTHONPATH}:/RA"

EXPOSE 8000
EXPOSE 30000

CMD bash start.sh