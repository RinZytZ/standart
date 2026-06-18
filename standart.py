import discord
from discord.ext import commands
import asyncio
import random
import os

TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = 991057181677850694

PREFIX = "всодд-"

# Гифки для команды "огонь"
FIRE_GIFS = [
    "https://tenor.com/view/soviet-gas-mask-assault-military-gif-22381336",
    "https://tenor.com/view/soviet-union-tanks-ussr-cccp-russia-gif-9739824583956641130"
]

# Гифки для команды "парад"
PARADE_GIFS = [
    "https://tenor.com/view/east-germany-national-people%27s-army-ddr-germany-gdr-gif-19915374299296063",
    "https://tenor.com/view/east-germany-national-people%27s-army-ddr-germany-gdr-gif-7980861786812559513"
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def is_admin(ctx):
    return ctx.author.id == ADMIN_ID

@bot.event
async def on_ready():
    print(f"⭐ {bot.user} — Генерал ВС ОДД готов!")

@bot.command(name="огонь")
async def fire(ctx):
    if not is_admin(ctx):
        return
    gif = random.choice(FIRE_GIFS)
    await ctx.send(f"@everyone {gif}")

@bot.command(name="ликвидировать")
async def liquidate(ctx, member: discord.Member):
    if not is_admin(ctx):
        return
    try:
        await member.kick(reason="Ликвидация по приказу командования")
        await ctx.send(f"⭐ {member.mention} ликвидирован.")
    except:
        await ctx.send("⭐ Ошибка. Проверь права.")

@bot.command(name="зачистка")
async def purge(ctx, amount: int):
    if not is_admin(ctx):
        return
    if amount < 1 or amount > 100:
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"⭐ Зачистка завершена. Удалено {len(deleted)-1} сообщений.")

@bot.command(name="парад")
async def parade(ctx):
    if not is_admin(ctx):
        return
    
    gif = random.choice(PARADE_GIFS)
    
    await ctx.send(gif)
    await asyncio.sleep(1)
    await ctx.send(gif)
    await asyncio.sleep(1)
    await ctx.send(gif)

@bot.command(name="отбой")
async def standdown(ctx):
    if not is_admin(ctx):
        return
    await ctx.send("⭐ **ОТБОЙ.** Всем отдыхать.")

@bot.command(name="позывной")
async def callsign(ctx):
    if not is_admin(ctx):
        return
    await ctx.send("⭐ Генерал ВС ОДД на связи.")

async def main():
    while True:
        try:
            async with bot:
                await bot.start(TOKEN)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
