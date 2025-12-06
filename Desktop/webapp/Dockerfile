# 1. START: Start with a standard, clean Python box (The base layer)
FROM python:3.11-slim

# 2. SETUP: Set the working folder inside the box to /app
WORKDIR /app

# 3. COPY: Copy the Store's supply list and code into the box
COPY requirements.txt .
COPY app.py .

# 4. INSTALL SUPPLIES: Use the supply list to install Flask
RUN pip install --no-cache-dir -r requirements.txt

# 5. OPEN DOOR: Tell the box to open the store's internal door (8000)
EXPOSE 8000

# 6. RUN: This is the command to open the store when the box starts running
CMD ["python", "app.py"]