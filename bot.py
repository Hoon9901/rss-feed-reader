from nextcord.ext.commands import Bot, Context
from nextcord import Intents, TextChannel
from contextlib import ExitStack
from json_db import JSON_DB
from updater import start


intents = Intents.default()
intents.messages = True

class RSSBot(Bot):
    time = 5*60 # defalt 5 minutes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_scheduled = False
    
    def updateTime(self, time):
        self.time = time
        print(f"Updated time to {time} seconds.")

    def getTime(self):
        return self.time


client = RSSBot(intents=intents, command_prefix="rss!")


@client.listen()
async def on_ready():
    if not client.updates_scheduled:
        print(f"Starting the feed update loop {client.getTime()} seconds")
        start(client.getTime(), client.loop, db, client)

    print("We're alive!!!")

@client.command(name="추가")
async def add(ctx: Context, feed_url: str):
    guilds = db.get("feeds", default={})
    feeds = guilds.get(str(ctx.guild.id), [])

    feeds.append(feed_url)

    guilds[str(ctx.guild.id)] = feeds
    db.set("feeds", guilds)

    await ctx.send(f"[{ctx.guild.name}] 피드 목록에  `{feed_url}` 추가됨! ")


@client.command(name="삭제")
async def remove(ctx: Context, feed_url: str):
    guilds = db.get("feeds", default={})
    feeds = guilds.get(str(ctx.guild.id), [])

    try:
        feeds.remove(feed_url)
    except ValueError:
        await ctx.send(f"[{ctx.guild.name}] `{feed_url}` 피드 목록에서 이미 삭제된 URL.")
    else:
        guilds[str(ctx.guild.id)] = feeds
        db.set("feeds", guilds)

        await ctx.send(f"[{ctx.guild.name}] `{feed_url}` 삭제됨. ")


@client.command(name="목록")
async def list_command(ctx: Context):
    guilds = db.get("feeds", default={})
    feeds = guilds.get(str(ctx.guild.id), [])
    feed_list = "\n".join(feeds) if feeds else "*피드 찾을 수 없음!*"
    await ctx.send(f"**피드 목록**\n{feed_list}")


@client.command(name="채널설정")
async def setup(ctx: Context, channel: TextChannel):
    guilds = db.get("guilds", default={})
    guilds[str(channel.guild.id)] = channel.id
    db.set("guilds", guilds)
    await ctx.send(f"[{ctx.guild.name}] {channel.mention} RSS 피드 채널로 성공적으로 설정되었습니다.")


@client.command(name="채널정보")
async def info(ctx: Context):
    channel_id = db.get("guilds", default={}).get(str(ctx.guild.id), None)
    channel = ctx.guild.get_channel(channel_id).mention if channel_id is not None else "*Not Set*"
    await ctx.send(f"[{ctx.guild.name}] RSS 피드 채널은 이곳 -> {channel} ")

@client.command(name="갱신정보")
async def info(ctx: Context):
    await ctx.send(f"[{ctx.guild.name}] RSS 피드 갱신 주기 : {client.getTime()}초")


@client.command(name="갱신설정")
async def info(ctx: Context, time: int):
    old_time = client.getTime()
    client.updateTime(time)
    await ctx.send(f"[{ctx.guild.name}] RSS 피드 갱신 주기 변경! -> {old_time}초 에서 {client.getTime()}초")

@client.command(name="봇정보")
async def info(ctx: Context):
    channel_id = db.get("guilds", default={}).get(str(ctx.guild.id), None)
    channel = ctx.guild.get_channel(channel_id).mention if channel_id is not None else "*Not Set*"
    await ctx.send(f"**RSS 피드 Reader 봇 정보입니다.**\n"
    + "RSS 피드 채널 : " + channel + "\n"
    + "RSS 갱신 주기 : " + client.getTime() + "초\n"
    + "created by @hoon9901")


@client.command(name="명령어")
async def info(ctx: Context):
    await ctx.send(f"**RSS 피드 Reader 봇 명령어 목록입니다.**\n"
    + "rss!추가 <피드 URL> - 피드를 추가합니다.\n" 
    + "rss!삭제 <피드 URL> - 피드를 삭제합니다.\n" 
    + "rss!목록 - 피드 목록을 보여줍니다.\n" 
    + "rss!채널설정 <채널> - RSS 피드 채널을 설정합니다.\n" 
    + "rss!채널정보 - RSS 피드 채널 정보를 보여줍니다.\n" 
    + "rss!갱신정보 - RSS 피드 갱신 주기를 보여줍니다.\n"
    + "rss!갱신설정 <초단위> - RSS 피드 갱신 주기를 설정합니다.\n"
    + "rss!봇정보 - 봇 정보를 보여줍니다.\n"
    + "rss!명령어 - 명령어를 보여줍니다.")


with ExitStack() as stack:
    stack.enter_context(token_file := open("token.secret"))
    stack.enter_context(db := JSON_DB(__file__))
    client.run(token_file.read().strip())
