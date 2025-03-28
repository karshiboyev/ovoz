# Python muhitini o‘rnatish
FROM python:3.9

# Ishchi katalogni yaratish
WORKDIR /bot

# Kerakli fayllarni ko‘chirish
COPY . /bot

# Talab qilinadigan kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "main.py"]
