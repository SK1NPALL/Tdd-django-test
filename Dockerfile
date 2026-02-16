FROM python:3.14-slim

RUN python -m venv /venv  
ENV PATH="/venv/bin:$PATH"  

COPY requirements.txt /tmp/requirements.txt  
RUN pip install -r /tmp/requirements.txt 

COPY src /src

WORKDIR /src

RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1

RUN adduser --uid 1234 nonroot  
RUN chown -R nonroot:nonroot /src
USER nonroot  

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8888 superlists.wsgi:application"]