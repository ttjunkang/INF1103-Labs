FROM python:3.11-slim

WORKDIR /app

COPY *.py ./
COPY inventory.json products.csv ./
COPY tests/ ./tests/

CMD ["python", "inventory_system.py"]