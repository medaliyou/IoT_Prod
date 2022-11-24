FROM python:3.10

WORKDIR /MU

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /MU/requirements.txt
COPY . /MU/
RUN ls -laht /MU
ENV PYTHONPATH "${PYTHONPATH}:/MU"

EXPOSE 8003
CMD python3 /MU/core/MU.py