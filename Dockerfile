FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Assume model.pkl is present after training in the pipeline
# Or pulled from an artifact

CMD ["python", "app/app.py"]
