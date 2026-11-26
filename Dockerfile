FROM python:3.12-slim-bookworm

ARG GODOT_VERSION=4.7.1
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl unzip \
       libasound2 libfontconfig1 libgl1 libpulse0 libxcursor1 libxi6 libxinerama1 libxrandr2 \
    && curl -fL --retry 2 "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip" -o /tmp/godot.zip \
    && unzip -q /tmp/godot.zip -d /tmp/godot \
    && mv "/tmp/godot/Godot_v${GODOT_VERSION}-stable_linux.x86_64" /usr/local/bin/godot \
    && chmod +x /usr/local/bin/godot \
    && rm -rf /tmp/godot /tmp/godot.zip /var/lib/apt/lists/*

WORKDIR /app
COPY server.py game.pck.gz /app/
RUN python -c "import gzip, shutil; source=gzip.open('game.pck.gz', 'rb'); target=open('game.pck', 'wb'); shutil.copyfileobj(source, target); source.close(); target.close()" \
    && rm game.pck.gz
ENV PYTHONUNBUFFERED=1 DATA_DIR=/data PORT=8080 GAME_PORT=9000
EXPOSE 8080
CMD ["python", "server.py"]
