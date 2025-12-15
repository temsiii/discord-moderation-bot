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

async def log_embed(title: str, description: str, fields: list = None, image_url: str = None):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    if image_url:
        embed.set_image(url=image_url)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_member_join(member):
    # Ajout automatique du rôle
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        await member.add_roles(role)
        await log_embed(
            title="✨ Nouveau membre",
            description=f"Rôle attribué à {member.mention} à son arrivée."
        )

    # Envoi du message de bienvenue
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Bienvenue sur le serveur, {member.mention} ! 🎉 N'hésite pas à te présenter !")

@bot.event
async def on_message_delete(message):
    content = message.content or "[Pas de texte]"
    description = f"Message supprimé dans {message.channel.mention} par {message.author.mention}"
    fields = [("Contenu", content, False)]
    image_url = None

    if message.attachments:
        # Si plusieurs pièces jointes, on affiche la première en image, les autres en champs
        first_image_set = False
        for attachment in message.attachments:
            if not first_image_set and attachment.url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                image_url = attachment.url
                first_image_set = True
            fields.append(("Pièce jointe", f"[{attachment.filename}]({attachment.url})", False))

    await log_embed(title="❌ Message supprimé", description=description, fields=fields, image_url=image_url)

@bot.command(help="Expulse un membre du serveur.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} a été expulsé.")
    await log_embed(
        title="🚪 Membre expulsé",
        description=f"{member} a été expulsé par {ctx.author}.",
        fields=[("Raison", reason or "Aucune raison fournie.", False)]
    )

@bot.command(help="Bannit un membre du serveur.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} a été banni.")
    await log_embed(
        title="⛔ Membre banni",
        description=f"{member} a été banni par {ctx.author}.",
        fields=[("Raison", reason or "Aucune raison fournie.", False)]
    )

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
    await log_embed(
        title="🧹 Salon vidé",
        description=f"Salon {ctx.channel.mention} vidé par {ctx.author}.",
        fields=[("Messages supprimés", str(deleted_count), False)]
    )

@bot.command(name="commands", help="Affiche la liste des commandes disponibles.")
async def commands_list(ctx):
    help_message = "Voici les commandes disponibles :\n"
    for command in bot.commands:
        desc = command.help or "Pas de description."
        help_message += f"- **!{command.name}** : {desc}\n"
    await ctx.send(help_message)

bot.run(TOKEN)
