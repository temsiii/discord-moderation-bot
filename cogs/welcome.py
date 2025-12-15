import discord
from discord.ext import commands

AUTO_ROLE_ID = 1449675786704654417
WELCOME_CHANNEL_ID = 1449930948031414283

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            await member.add_roles(role)

        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(f"Bienvenue {member.mention} 🎉")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
