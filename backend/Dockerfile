FROM python
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
RUN mkdir src/db
RUN python src/manage.py collectstatic --noinput
CMD python src/manage.py migrate && cd src && gunicorn --bind 0.0.0.0:8000 ispu.wsgi
