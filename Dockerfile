FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mv .env.example .env && echo "Renamed file"
CMD ["python3", "discord_main.py"]
