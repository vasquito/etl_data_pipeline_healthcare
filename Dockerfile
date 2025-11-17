FROM python:3.11-slim

# Solo Graphviz como dependencia del sistema
RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto Panel
EXPOSE 5006

CMD ["panel", "serve", "app/dashboards/run.py", "--address", "0.0.0.0", "--port", "5006"]
