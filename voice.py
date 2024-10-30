from nextcord.ext import commands
import nextcord

def run_voice_bot():
    TOKEN = 'MTExODIxODA3NDg0ODUwMTgyMA.Gqr8tC.mOja5gA4ORy4T3zq7xUa5bc7NN86M17A1srCYc'
    intents = nextcord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)  # Change prefix to '/'
    
    @bot.command()
    async def join(ctx):
        print("The voice bot is running")
        # Get the guild (server) the command was called from
        guild = ctx.guild

        # Look for a voice channel named 'gaming'
        voice_channel = nextcord.utils.get(guild.voice_channels, name='Lobby')

        if voice_channel is not None:
            if ctx.voice_client is not None:  # If the bot is already connected to a voice channel
                await ctx.voice_client.disconnect()  # Disconnect from current voice channel
            await voice_channel.connect()  # Connect to the 'gaming' voice channel
            await ctx.send("I have joined the 'gaming' voice channel!")
        else:
            await ctx.send("I couldn't find a voice channel named 'gaming'!")

   