import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from cryptography.fernet import Fernet
from os.path import exists

if not exists('filekey.key'):
    print("Please run encryptFile.py first.")

else:
    # Decrypting the key for use
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    fernet = Fernet(key)

    with open('token.txt', 'rb') as encrypted_key_file:
        encrypted = encrypted_key_file.read()

    decrypted_key = fernet.decrypt(encrypted)
    decrypted_key = str(decrypted_key)
    decrypted_key = decrypted_key.lstrip("b'").rstrip("\\n'")


# Make it easier for me to call functions
    bot = discord.Bot()

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")
    
    @bot.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx, number: discord.Option(int)):
            if number < 100:
                    await ctx.channel.purge(limit=number)
                    await ctx.send("Cleared by <@{.author.id}>. There were **{}** messages cleared.".format(ctx, str(number)))
                    await ctx.respond("Successfully cleared messages!")
            if number > 100:
                await ctx.respond("You cannot purge more than 100 messages at once")

    @bot.slash_command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx):
        await ctx.respond("Not implemented, never will be. Stop being lazy and use Discord's built in kick feature.")

    @bot.slash_command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx):
        await ctx.respond("Not implemented, never will be. Stop being lazy and use Discord's built in ban feature.")

    @bot.slash_command()
    @commands.has_permissions(moderate_members=True)
    async def mute(ctx):
        await ctx.respond("Not implemented, never will be. Stop being lazy and use Discord's built in timeout feature.")

    # Error handling
    @purge.error
    async def purge_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You're not allowed to run this command!")

    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You're not allowed to run this command!")
        # End of mute command

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You're not allowed to run this command!")

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You're not allowed to run this command!")

    bot.run(decrypted_key)