FROM python:3.12-slim

WORKDIR /app

COPY . /app/code

RUN pip install --no-cache-dir --upgrade -r /app/code/requirements.txt

EXPOSE 80

CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "80"]