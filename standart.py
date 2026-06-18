import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = 991057181677850694

PREFIX = "лейт-"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def is_admin(ctx):
    return ctx.author.id == ADMIN_ID

@bot.event
async def on_ready():
    print(f"⭐ {bot.user} — Лейтенант Белов готов!")

@bot.command(name="приказ")
async def order(ctx, *, text: str):
    if not is_admin(ctx):
        return
    await ctx.send(f"⭐ **ПРИКАЗ КОМАНДОВАНИЯ:**\n{text}")

@bot.command(name="доклад")
async def report(ctx):
    if not is_admin(ctx):
        return
    
    guild = ctx.guild
    members = guild.member_count
    channels = len(guild.channels)
    roles = len(guild.roles)
    
    await ctx.send(
        f"⭐ **ДОКЛАД ПО ОБСТАНОВКЕ:**\n"
        f"👥 Личный состав: {members}\n"
        f"📡 Каналов: {channels}\n"
        f"🎖 Ролей: {roles}"
    )

@bot.command(name="назначить")
async def assign_role(ctx, member: discord.Member, *, role_name: str):
    if not is_admin(ctx):
        return
    
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"⭐ Роль `{role_name}` не найдена.")
        return
    
    try:
        await member.add_roles(role, reason="Назначение по приказу")
        await ctx.send(f"⭐ {member.mention} назначен на должность `{role_name}`.")
    except:
        await ctx.send("⭐ Ошибка. Проверь права и роль.")

@bot.command(name="снять")
async def remove_role(ctx, member: discord.Member, *, role_name: str):
    if not is_admin(ctx):
        return
    
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"⭐ Роль `{role_name}` не найдена.")
        return
    
    try:
        await member.remove_roles(role, reason="Снятие по приказу")
        await ctx.send(f"⭐ {member.mention} освобождён от должности `{role_name}`.")
    except:
        await ctx.send("⭐ Ошибка. Проверь права и роль.")

@bot.command(name="есть")
async def acknowledge(ctx):
    if not is_admin(ctx):
        return
    await ctx.send("⭐ Есть, товарищ генерал!")

@bot.command(name="чисто")
async def clean(ctx):
    if not is_admin(ctx):
        return
    
    def is_bot_message(msg):
        return msg.author == bot.user
    
    deleted = await ctx.channel.purge(limit=100, check=is_bot_message)
    await ctx.send(f"⭐ Следы заметены. Удалено {len(deleted)} сообщений.", delete_after=5)

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
