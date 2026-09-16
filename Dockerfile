FROM python:3.11-slim

RUN echo "app:x:1001:1001::/home/code:/sbin/nologin" >> /etc/passwd && \
    echo "app:x:1001:" >> /etc/group && \
    mkdir -p /home/code

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app

RUN chown -R 1001:1001 /app /home/code

USER 1001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]