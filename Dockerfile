FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY src/Components/dist_analysis.jsx ./src/Components/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code + CSV
COPY . .

# Expose backend port
EXPOSE 5000

CMD ["python", "app.py"]
