import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

# 🔹 Flask 웹서버 (Replit 슬립 방지용)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ Discord Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================================
# 🔹 디스코드 봇 설정
# ================================
TOKEN = os.environ["DISCORD_TOKEN"]  # Replit Secrets에 넣기
TARGET_USER_ID = 1076109410130219109  # 닉 바꿀 유저 ID
GUILD_ID = 1375837621636567142        # 봇이 돌아갈 서버 ID
counter = 458  # 시작 숫자 (예: D-259부터 시작)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")
    await wait_until_midnight()
    daily_rename.start()

# 🔹 자정까지 기다린 뒤 루프 시작
async def wait_until_midnight():
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    await asyncio.sleep((tomorrow - now).total_seconds())

@tasks.loop(hours=24)
async def daily_rename():
    global counter
    guild = bot.get_guild(GUILD_ID)  # 서버 ID로 특정 서버 가져오기
    member = guild.get_member(TARGET_USER_ID)

    if member:
        new_nick = f"D-{counter}"
        try:
            await member.edit(nick=new_nick)
            print(f"닉네임 변경 완료 → {new_nick}")
        except discord.Forbidden:
            print("⚠️ 권한 부족: 봇에 Manage Nicknames 권한 필요")
        counter -= 1
    else:
        print("⚠️ 해당 유저를 찾을 수 없음")

# ================================
# 실행
# ================================
keep_alive()
bot.run(TOKEN)


# 테스트용
