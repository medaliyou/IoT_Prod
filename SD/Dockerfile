FROM python:3.10

WORKDIR /SD

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /SD/requirements.txt
COPY . /SD/
RUN ls -laht /SD
ENV PYTHONPATH "${PYTHONPATH}:/SD"

EXPOSE 8002
EXPOSE 30002

CMD bash start.sh