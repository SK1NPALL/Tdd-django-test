FROM python:3.12-slim

# 1. เพิ่ม python3-dev เพื่อให้คอมไพล์ psycopg2 ได้ราบรื่น
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv  
ENV PATH="/venv/bin:$PATH"  

RUN pip install --upgrade pip

# 2. แนะนำให้ใช้ --no-cache-dir เพื่อประหยัดขนาด Image
COPY requirements.txt /tmp/requirements.txt  
RUN pip install --no-cache-dir -r /tmp/requirements.txt 

# 3. เตรียม Folder สำหรับ Static และ Media files
# (Render Disk หรือ Cloud Storage จะมาเก็บที่นี่)
WORKDIR /src
COPY src /src

# 4. จัดการสิทธิ์ให้ nonroot
RUN adduser --uid 1234 nonroot  
RUN chown -R nonroot:nonroot /src /venv
USER nonroot  

# 5. การรัน Migrate และ Gunicorn
# ระบุชื่อ app ให้ตรง (ในที่นี้คือ superlists)
# Render จะส่งค่า $PORT มาให้เองอัตโนมัติ
CMD python manage.py migrate --noinput && \
    gunicorn --bind 0.0.0.0:$PORT superlists.wsgi:application