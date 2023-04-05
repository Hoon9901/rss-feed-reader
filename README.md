# [Discord Bot] RSS Feed Reader 

This is a simple bot that monitors RSS feeds and announces when new items show up in the feeds.

## prerequisites

```
Python >= 3.9
Poetry
```

## Installation & Run

`token.secret` 이름의 파일을 생성하고 Discord Bot 토큰을 기입하세요.
그리고 다음 명령어를 차례대로 실행합니다.

```shell
pip install poetry
poetry install
poetry run python bot.py
```

## Commands
`rss!추가 <피드 URL>` 
피드를 추가합니다.

`rss!삭제 <피드 URL>`
피드를 삭제합니다.

`rss!목록`
피드 목록을 보여줍니다.

`rss!채널설정 <채널>`
RSS 피드 채널을 설정합니다.

`rss!정보`
RSS 피드 채널 정보를 보여줍니다.

`rss!명령어`
명령어를 보여줍니다.

# 참고 