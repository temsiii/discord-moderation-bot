import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1449678507247665183

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_embed(self, title, description, fields=None, image_url=None):
        embed = discord.Embed(title=title, description=description, color=discord.Color.red())
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        if image_url:
            embed.set_image(url=image_url)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        fields = [
            ("Auteur", message.author.mention, False),
            ("Salon", message.channel.mention, False),
            ("Contenu", message.content or "[Aucun texte]", False)
        ]

        image_url = None
        for att in message.attachments:
            if att.url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                image_url = att.url
            fields.append(("Pièce jointe", f"[{att.filename}]({att.url})", False))

        await self.log_embed("🗑️ Message supprimé", "Un message a été supprimé", fields, image_url)

async def setup(bot):
    await bot.add_cog(Logs(bot))
