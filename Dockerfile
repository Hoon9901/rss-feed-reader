FROM python:3.10-slim
WORKDIR /usr/src/app

ADD ./ ./

RUN pip3 install poetry
RUN poetry install

CMD ["poetry", "run", "python", "bot.py"]
