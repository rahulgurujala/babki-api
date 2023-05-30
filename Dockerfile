FROM python:3.11.2

WORKDIR /denarii

COPY requirements.txt .
RUN pip install --no-cache-dir -r /denarii/requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
