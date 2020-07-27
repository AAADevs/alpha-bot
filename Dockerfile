FROM python:3.8
COPY requirements.txt /app/
RUN pip install --no-cache-dir -U -r /app/requirements.txt

