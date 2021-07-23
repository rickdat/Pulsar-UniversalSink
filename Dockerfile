FROM python:3
ADD start_sink.py /
ADD auth.py /
ADD schema.py /
RUN pip install pulsar
RUN pip install requests
CMD [ "python", "./start_sink.py" ]
