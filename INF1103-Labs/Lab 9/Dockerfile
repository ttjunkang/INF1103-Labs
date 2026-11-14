FROM python:3.11-slim

WORKDIR /app

COPY *.py ./
COPY inventory.json products.csv ./

CMD ["python", "inventory_system.py"]