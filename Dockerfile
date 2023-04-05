FROM python:3.9-alpine
WORKDIR /app					
ADD . .					

RUN pip install poetry

CMD ["poetry", "run", "python", "bot.py"]
