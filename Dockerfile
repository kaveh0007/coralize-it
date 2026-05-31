FROM python:3.10-slim

WORKDIR /app

RUN curl -fsSL https://withcoral.com/install.sh | sh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
