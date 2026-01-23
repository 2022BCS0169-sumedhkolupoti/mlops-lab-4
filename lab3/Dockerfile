# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Upgrade pip to handle downloads better
RUN pip install --upgrade pip

# Install heavy dependencies individually to improve reliability and debuggability
RUN pip install --no-cache-dir --default-timeout=1000 numpy pandas
RUN pip install --no-cache-dir --default-timeout=1000 scikit-learn
RUN pip install --no-cache-dir --default-timeout=1000 fastapi uvicorn joblib pydantic

# Copy the application code and the model
COPY main.py .
COPY model.pkl .

# Expose the API port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
