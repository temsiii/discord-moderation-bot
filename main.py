import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

LOG_CHANNEL_ID = 1449678507247665183
AUTO_ROLE_ID = 1449675786704654417
WELCOME_CHANNEL_ID = 1449930948031414283


class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands synchronisées")


bot = MyBot()


# ─────────────────────────────
# OUTIL LOG EMBED
# ─────────────────────────────
async def log_embed(title, description, fields=None, image_url=None):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    if image_url:
        embed.set_image(url=image_url)

    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)


# ─────────────────────────────
# READY
# ─────────────────────────────
@bot.event
async def on_ready():
    print(f"🤖 Connecté en tant que {bot.user}")


# ─────────────────────────────
# NOUVEAU MEMBRE
# ─────────────────────────────
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        await member.add_roles(role)
        await log_embed(
            "✨ Nouveau membre",
            f"{member.mention} a rejoint le serveur.",
            [("Rôle attribué", role.mention, False)]
        )

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Bienvenue {member.mention} 🎉")


# ─────────────────────────────
# MESSAGE SUPPRIMÉ
# ─────────────────────────────
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    fields = [("Auteur", message.author.mention, False),
              ("Salon", message.channel.mention, False),
              ("Contenu", message.content or "[Aucun texte]", False)]

    image_url = None
    if message.attachments:
        for att in message.attachments:
            if att.url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                image_url = att.url
            fields.append(("Pièce jointe", f"[{att.filename}]({att.url})", False))

    await log_embed("🗑️ Message supprimé", "Un message a été supprimé", fields, image_url)


# ─────────────────────────────
# /mod → MENU DÉROULANT
# ─────────────────────────────
@bot.tree.command(name="mod", description="Menu de modération")
@app_commands.describe(
    action="Action à effectuer",
    membre="Membre concerné"
)
@app_commands.choices(action=[
    app_commands.Choice(name="Kick un membre", value="kick"),
    app_commands.Choice(name="Ban un membre", value="ban"),
    app_commands.Choice(name="Clear ALL le salon", value="clear_all"),
])
async def mod(interaction: discord.Interaction, action: app_commands.Choice[str], membre: discord.Member = None):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Permission refusée", ephemeral=True)
        return

    if action.value == "kick":
        if not membre:
            await interaction.response.send_message("❌ Membre requis", ephemeral=True)
            return
        await membre.kick()
        await interaction.response.send_message(f"👢 {membre} kick.")
        await log_embed("🚪 Kick", f"{membre} kick par {interaction.user}")

    elif action.value == "ban":
        if not membre:
            await interaction.response.send_message("❌ Membre requis", ephemeral=True)
            return
        await membre.ban()
        await interaction.response.send_message(f"🔨 {membre} banni.")
        await log_embed("⛔ Ban", f"{membre} banni par {interaction.user}")

    elif action.value == "clear_all":
        deleted = await interaction.channel.purge()
        await interaction.response.send_message("🧹 Salon nettoyé", ephemeral=True)
        await log_embed(
            "🧹 Clear ALL",
            f"{len(deleted)} messages supprimés",
            [("Salon", interaction.channel.mention, False)]
        )


bot.run(TOKEN)
