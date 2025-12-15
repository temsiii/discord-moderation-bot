import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} kick.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banni.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearall(self, ctx):
        deleted = await ctx.channel.purge()
        await ctx.send(f"🧹 {len(deleted)} messages supprimés.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
