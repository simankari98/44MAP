FROM python:3.12-slim-bookworm

ARG GODOT_VERSION=4.7.1
ARG PCK_FILE_ID=1Hx0SGPIhOfE07aU_YR4s7jh2_wMNwnyP

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl unzip gzip \
       libasound2 libfontconfig1 libgl1 libpulse0 libxcursor1 libxi6 libxinerama1 libxrandr2 \
    && curl -fL --retry 2 "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip" -o /tmp/godot.zip \
    && unzip -q /tmp/godot.zip -d /tmp/godot \
    && mv "/tmp/godot/Godot_v${GODOT_VERSION}-stable_linux.x86_64" /usr/local/bin/godot \
    && chmod +x /usr/local/bin/godot \
    && rm -rf /tmp/godot /tmp/godot.zip /var/lib/apt/lists/*

WORKDIR /app

# ---- دانلود game.pck.gz از Google Drive ----
RUN curl -c /tmp/cookies.txt -s -L "https://drive.google.com/uc?export=download&id=${PCK_FILE_ID}" -o /tmp/gd_page.html \
    && CONFIRM=$(grep -o 'confirm=[^&"]*' /tmp/gd_page.html | head -1 | sed 's/confirm=//') \
    && if [ -n "$CONFIRM" ]; then \
         curl -L -b /tmp/cookies.txt "https://drive.google.com/uc?export=download&confirm=${CONFIRM}&id=${PCK_FILE_ID}" -o /app/game.pck.gz; \
       else \
         cp /tmp/gd_page.html /app/game.pck.gz; \
       fi \
    && rm -f /tmp/cookies.txt /tmp/gd_page.html

# ---- بررسی اینکه فایل واقعاً gzip است، سپس استخراج ----
RUN python -c "import gzip, shutil; source=gzip.open('game.pck.gz', 'rb'); target=open('game.pck', 'wb'); shutil.copyfileobj(source, target); source.close(); target.close()" \
    && rm game.pck.gz

COPY server.py /app/

ENV PYTHONUNBUFFERED=1 DATA_DIR=/data PORT=8080 GAME_PORT=9000
EXPOSE 8080
CMD ["python", "server.py"]