import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # nécessaire pour on_member_join etc.

bot = commands.Bot(command_prefix="!", intents=intents)

# ID de ton salon de logs
LOG_CHANNEL_ID = 1449678507247665183
# ID du rôle à attribuer automatiquement
AUTO_ROLE_ID = 1449675786704654417
# ID du salon de bienvenue
WELCOME_CHANNEL_ID = 1449930948031414283  # Ton ID de salon de bienvenue

async def log(message):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_member_join(member):
    # Ajout automatique du rôle
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        await member.add_roles(role)
        await log(f"✨ Rôle attribué à {member.mention} à son arrivée.")

    # Envoi du message de bienvenue
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Bienvenue sur le serveur, {member.mention} ! 🎉 N'hésite pas à te présenter !")

@bot.event
async def on_message_delete(message):
    await log(f"❌ Message supprimé dans {message.channel.mention} par {message.author.mention} : {message.content}")

@bot.command(help="Expulse un membre du serveur.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} a été expulsé.")
    await log(f"🚪 {member} a été expulsé par {ctx.author}. Raison : {reason}")

@bot.command(help="Bannit un membre du serveur.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} a été banni.")
    await log(f"⛔ {member} a été banni par {ctx.author}. Raison : {reason}")

@bot.command(help="Supprime tous les messages du salon en cours.")
@commands.has_permissions(manage_messages=True)
async def clearall(ctx):
    await ctx.send("🧹 Suppression de tous les messages en cours...")
    deleted_count = 0
    while True:
        deleted = await ctx.channel.purge(limit=100)
        deleted_count += len(deleted)
        if len(deleted) < 100:
            break
    await ctx.send(f"🧹 Salon vidé, {deleted_count} messages supprimés.", delete_after=5)
    await log(f"🧹 Salon {ctx.channel.mention} vidé par {ctx.author} ({deleted_count} messages supprimés)")

@bot.command(name="commands", help="Affiche la liste des commandes disponibles.")
async def commands_list(ctx):
    help_message = "Voici les commandes disponibles :\n"
    for command in bot.commands:
        desc = command.help or "Pas de description."
        help_message += f"- **!{command.name}** : {desc}\n"
    await ctx.send(help_message)

bot.run(TOKEN)
