import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime, timedelta

TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = 991057181677850694

PREFIX = "трейн-"
WARNS_FILE = "warns.json"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def is_commander(ctx):
    return ctx.author.id == ADMIN_ID

# ===== ВАРНЫ =====
def load_warns():
    if os.path.exists(WARNS_FILE):
        with open(WARNS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_warns(warns):
    with open(WARNS_FILE, "w", encoding="utf-8") as f:
        json.dump(warns, f, ensure_ascii=False, indent=2)

warns = load_warns()
isolation_mode = {}

@bot.event
async def on_ready():
    print(f"💨 {bot.user} — A-Train в деле!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.guild is None:
        return
    
    if isolation_mode.get(str(message.guild.id), False):
        if message.author.id != ADMIN_ID:
            try:
                await message.delete()
            except:
                pass
            return
    
    await bot.process_commands(message)

# ===== КОМАНДЫ =====
@bot.command(name="отзовись")
async def respond(ctx):
    if not is_commander(ctx):
        return
    await ctx.send("A-Train на месте.")

@bot.command(name="очистить")
async def clear(ctx, amount: int):
    if not is_commander(ctx):
        return
    if amount < 1 or amount > 100:
        return
    deleted = await ctx.channel.purge(limit=amount + 1)

@bot.command(name="изоляция")
async def isolation(ctx):
    if not is_commander(ctx):
        return
    guild_id = str(ctx.guild.id)
    isolation_mode[guild_id] = True
    await ctx.send("Изоляция включена.")

@bot.command(name="отбой")
async def off_isolation(ctx):
    if not is_commander(ctx):
        return
    guild_id = str(ctx.guild.id)
    isolation_mode[guild_id] = False
    await ctx.send("Изоляция выключена.")

@bot.command(name="варн")
async def warn(ctx, member: discord.Member, *, reason: str = "Нарушение"):
    if not is_commander(ctx):
        return
    if member.id == ADMIN_ID:
        return
    
    user_id = str(member.id)
    guild_id = str(ctx.guild.id)
    key = f"{guild_id}_{user_id}"
    
    if key not in warns:
        warns[key] = {"count": 0, "reasons": []}
    
    warns[key]["count"] += 1
    warns[key]["reasons"].append(f"{reason} ({datetime.now().strftime('%d.%m.%Y %H:%M')})")
    save_warns(warns)
    
    current_count = warns[key]["count"]
    
    if current_count >= 3:
        try:
            await member.timeout(timedelta(hours=1), reason=f"3 варна: {reason}")
            del warns[key]
            save_warns(warns)
            await ctx.send(f"{member.mention} — час мута.")
        except:
            pass
    else:
        await ctx.send(f"{member.mention} — варн {current_count}/3. {reason}")

@bot.command(name="варны")
async def show_warns(ctx, member: discord.Member):
    if not is_commander(ctx):
        return
    
    key = f"{str(ctx.guild.id)}_{str(member.id)}"
    
    if key not in warns:
        await ctx.send(f"{member.mention} без варнов.")
        return
    
    count = warns[key]["count"]
    reasons = warns[key]["reasons"]
    reasons_text = "\n".join([f"  {i+1}. {r}" for i, r in enumerate(reasons)])
    await ctx.send(f"{member.mention} — {count}/3 варнов:\n{reasons_text}")

@bot.command(name="снятьварны")
async def clear_warns(ctx, member: discord.Member):
    if not is_commander(ctx):
        return
    
    key = f"{str(ctx.guild.id)}_{str(member.id)}"
    
    if key in warns:
        del warns[key]
        save_warns(warns)
        await ctx.send(f"Варны с {member.mention} сняты.")

@bot.command(name="заткнись")
async def shut_up(ctx, member: discord.Member):
    if not is_commander(ctx):
        return
    if member.id == ADMIN_ID:
        return
    
    try:
        await member.timeout(timedelta(minutes=5), reason="A-Train")
        
        def is_target(msg):
            return msg.author == member
        
        deleted = await ctx.channel.purge(limit=20, check=is_target)
        await ctx.send(f"{member.mention} — **ай кент стоп, ай кент стоп**")
    except:
        pass

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
