FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
