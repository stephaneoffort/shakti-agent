FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Télécharge le modèle de détection de voix (VAD) au build
RUN python -m livekit.plugins.silero download

COPY . .

CMD ["python", "agent.py", "start"]
