import discord
import responses
import chat
from discord.ext import commands
import asyncio
import json
import os
import openai
from gtts import gTTS
import nextcord








if os.path.exists('frag_counts.json') and os.path.getsize('frag_counts.json') > 0:
    with open('frag_counts.json', 'r') as f:
        frag_counts = json.load(f)
else:
    frag_counts = {}
    
async def send_message(ctx, response):
    await ctx.send(response)

def run_discord_bot():
    global user_confirmation_msg
  
    
    
    TOKEN = 'MTExODIxODA3NDg0ODUwMTgyMA.Gqr8tC.mOja5gA4ORy4T3zq7xUa5bc7NN86M17A1srCYc'
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='/', intents=intents)  # Change prefix to '/'

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        
    @bot.event
    async def on_message(message):
        # if message.author.id == 636890054681165853:
        #             try:
        #                 # Check if the user is in a voice channel
        #                 if message.author.voice:
        #                     voice_channel = message.author.voice.channel
        #                     voice_client = await voice_channel.connect()
        #                     # The 'after' argument is a function that gets called after the source has finished playing
        #                     def after_playing(error):
        #                         coro = voice_client.disconnect(),
        #                         fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        #                         try:
        #                             fut.result()
        #                         except:
        #                             # an error happened sending the message
        #                             pass
        #                     voice_client.play(nextcord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source="playme.mp3"),after=after_playing)            
        #                     # voice_client.play(nextcord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=f"{word}.mp3"), after=after_playing)
        #                     os.remove(f"{word}.mp3")
        #                 else:
        #                     await message.reply(file=nextcord.File(f"playme.mp3"))
        #                     os.remove(f"{word}.mp3")
        #             except Exception as e:
        #                 print(str(e))
                  
        #                 print(e)
        #             # We found a word match in the message, so we can exit the loop early
                
            
        # # We do not want the bot to reply to itself
        if message.author.id == bot.user.id:
            return
        
        words = [
        "Lesbian",
        "Heteronormativity",
        "Homophobia",
        "Transphobia",
        "Pride",
        "LGBT",
        "LGBTQ",
        "LGBTQIA",
        "LGBTQ+",
        "Rainbow",
        "Coming Out",
        "Closeted",
        "Transitioning",
        "Hormone Therapy",
        "Sexual Orientation",
        "Gender Identity",
        "Same-Sex",
        "Homosexual",
        "Heterosexual",
        "suck",
        "balls",
        "gay",
        "dick",
        "daddy",
        "dad",
        "pussy"
    ]
        for word in words:
                if word.lower() in message.content.lower():
                    try:
                        # Check if the user is in a voice channel
                        if message.author.voice:
                            voice_channel = message.author.voice.channel
                            voice_client = await voice_channel.connect()

                            # Use gTTS to generate an audio file
                            sound = gTTS(text=f"This is for You {message.author}", lang='en', slow=False)
                            sound.save(f'{word}.mp3')

                            

                            # The 'after' argument is a function that gets called after the source has finished playing
                            def after_playing(error):
                                coro = voice_client.disconnect()
                                fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                                try:
                                    fut.result()
                                except:
                                    # an error happened sending the message
                                    pass
                            voice_client.play(nextcord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source="playme.mp3"),after=after_playing)            
                            # voice_client.play(nextcord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=f"{word}.mp3"), after=after_playing)
                            os.remove(f"{word}.mp3")
                        else:
                            await message.reply(file=nextcord.File(f"playme.mp3"))
                            os.remove(f"{word}.mp3")
                    except Exception as e:
                        print(str(e))
                  
                        print(e)
                    # We found a word match in the message, so we can exit the loop early
                    break

        # Process commands
        await bot.process_commands(message)
    
   
  
                
                
    @bot.command()
    async def val(ctx, *, user_message):
        response = responses.handle_responses(user_message)
        await send_message(ctx, response)

    @bot.command()
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @bot.command()
    async def record(ctx):
        if not ctx.voice_client:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        user = ctx.message.author
        vc = ctx.voice_client

        # Create a file to store the audio
        with open('audio.raw', 'wb') as audio_file:
            while vc.is_speaking(user):
                
                # Read audio data
                data = await vc.recv()

                # Write data to file
                audio_file.write(data)
                print("is lisening")
      
                
    @bot.command()            
    async def leaderboard(ctx):
        sorted_frag_counts = sorted(frag_counts.items(), key=lambda x: x[1]['top'], reverse=True)

        leaderboard_embed = discord.Embed(title="Top Fragger Leaderboard:" ,description="\n".join([f'{i+1}. {username} = {details["top"]} {":star2:" * details["top"]}' for i, (username, details) in enumerate(sorted_frag_counts)]))
        sorted_frag_counts_1 = sorted(frag_counts.items(), key=lambda x: x[1]['bottom'], reverse=True)

        await ctx.send(embed=leaderboard_embed)
        leaderboard_embed_2= discord.Embed(title="Bottom Fragger Leaderboard:" ,description="\n".join([f'{i+1}. {username} = {details["bottom"]} {":poop:" * details["bottom"]}' for i, (username, details) in enumerate(sorted_frag_counts_1)]))
        await ctx.send(embed=leaderboard_embed_2)
     
        
        
        # <@1047933870357618821>
        # <@312703013720555520>
    @bot.command()
    async def test(ctx):
        await ctx.send('Hello!')      
        
    @bot.command()
    async def bottomfrag(ctx,*, user_message):
        
        confirm_message = await ctx.send(f':poop: : Are you sure {user_message} was the bottom fragger? Confirm with a reaction!')
        await ctx.send("You Have 5 seconds to Confirm !")
        await confirm_message.add_reaction('✅') 
        await confirm_message.add_reaction('❌')  

        def check(reaction, user):
        
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == confirm_message.id
        try:
     
            reaction, user = await bot.wait_for('reaction_add', timeout=5.0, check=check)

            if str(reaction.emoji) == '✅':
              
                    
                frag_counts[user_message] = frag_counts.get(user_message, {'top': 0, 'bottom': 0})
                frag_counts[user_message]['bottom'] += 1
                
                Bottomfragg_embed = discord.Embed(title=f'Sucked ass today !:poop::poop::poop::poop:',description=f'{user_message} Earned a :poop: \n Total bottom frags: {frag_counts[user_message]["bottom"]}', color=discord.Colour.purple())

                await ctx.send(embed=Bottomfragg_embed)  
                sorted_frag_counts_1 = sorted(frag_counts.items(), key=lambda x: x[1]['bottom'], reverse=True)
                leaderboard_embed_2= discord.Embed(title="Bottom Fragger Leaderboard:" ,description="\n".join([f'{i+1}. {username} = {details["bottom"]} {":poop:" * details["bottom"]}' for i, (username, details) in enumerate(sorted_frag_counts_1)]), color=discord.Colour.purple())
                await ctx.send(embed=leaderboard_embed_2)
                await ctx.send('https://tenor.com/view/poop-pooping-otso-otso-shit-gif-13336997')
                with open('frag_counts.json', 'w') as f:
                    json.dump(frag_counts, f)
            elif str(reaction.emoji) == '❌':
                await ctx.send(f'{user_message} why are u wasting my time ? :middle_finger::middle_finger::middle_finger:')  

        except asyncio.TimeoutError:
        
            await ctx.send('No confirmation received, command cancelled.')

    @bot.command()
    async def topfrag(ctx, *, user_message):
        user_confirmation_msg = f':supervillain: : Are you sure {user_message} was the Top fragger? Confirm with a reaction!'
        
        confirm_message = await ctx.send(f'{user_confirmation_msg} Confirm with a reaction!')
        await confirm_message.add_reaction('✅') 
        await confirm_message.add_reaction('❌')  

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == confirm_message.id
        
        try:
            loop_iterations = 0
            respones_on_orkhan = [f"Double checking, are you REALLY sure {user_message} was the top fragger? Confirm with a reaction again!",f"That has to be a joke?! \\n It really can't be {user_message} Did he really got the most kills?Can you confirm it again?",f"Are you fucking kidding me that{user_message} he really top fragged?Can you confirm it again?"]
            while True:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                
                if str(reaction.emoji) == '✅':
                    if user_message in ["<@1047933870357618821>", "<@312703013720555520>"]:
                        confirm_message = await ctx.send(respones_on_orkhan[loop_iterations])
                        await confirm_message.add_reaction('✅') 
                        await confirm_message.add_reaction('❌')
                        loop_iterations = loop_iterations+1
                        print(loop_iterations)
                        if loop_iterations == 3 and str(reaction.emoji) == '✅':
                            orkhan_top = discord.Embed(title="I CAN'T BELIVE THAT MF TOP FRAGGED", description=":middle_finger:")
                            await ctx.send(embed=orkhan_top)
                            break
                    else:
                        break
                else:
                    await ctx.send(f'{user_message}, why are you wasting my time?:middle_finger::middle_finger:')
                    return

            frag_counts[user_message] = frag_counts.get(user_message, {'top': 0, 'bottom': 0})
            frag_counts[user_message]['top'] += 1
            
            topfrag_embed = discord.Embed(title=f'VALO GODDDDDDDDDDDD! !:dizzy::dizzy::dizzy:',description=f'{user_message} Earned a :dizzy: \n Total Top frags: {frag_counts[user_message]["top"]}', color=discord.Colour.purple())

            await ctx.send(embed=topfrag_embed)
            sorted_frag_counts = sorted(frag_counts.items(), key=lambda x: x[1]['top'], reverse=True)

            leaderboard_embed = discord.Embed(title="Top Fragger Leaderboard:" ,description="\n".join([f'{i+1}. {username} = {details["top"]} {":star2:" * details["top"]}' for i, (username, details) in enumerate(sorted_frag_counts)]))
            sorted_frag_counts_1 = sorted(frag_counts.items(), key=lambda x: x[1]['bottom'], reverse=True)

            await ctx.send(embed=leaderboard_embed)
            await ctx.send('https://tenor.com/view/leonardo-dicaprio-clapping-clap-applause-amazing-gif-16384995')
            with open('frag_counts.json', 'w') as f:
                json.dump(frag_counts, f)
        except asyncio.TimeoutError:
            await ctx.send('No confirmation received, command cancelled.')
        
    # @bot.command()
    # async def bottomfrag(ctx, *, user_message):
    #     user_confirmation_msg = f':poop:  : Are you sure {user_message} was the bottom fragger?'
        
    #     confirm_message = await ctx.send(f'{user_confirmation_msg} Confirm with a reaction!')
    #     await confirm_message.add_reaction('✅') 
    #     await confirm_message.add_reaction('❌')  

    #     def check(reaction, user):
    #         return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == confirm_message.id
        
    #     try:
    #         while True:
    #             reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

    #             if str(reaction.emoji) == '✅':
    #                 if user_message in ["<@1047933870357618821>", "<@312703013720555520>"]:
    #                     confirm_message = await ctx.send(f"Double checking, are you REALLY sure {user_message} was the bottom fragger? Confirm with a reaction again!")
    #                     await confirm_message.add_reaction('✅') 
    #                     await confirm_message.add_reaction('❌')  
    #                 else:
    #                     break
    #             else:
    #                 await ctx.send(f'{user_message}, why are you wasting my time?')
    #                 return

    #         frag_counts[user_message] = frag_counts.get(user_message, {'top': 0, 'bottom': 0})
    #         frag_counts[user_message]['bottom'] += 1
    #         await ctx.send(f'{user_message} sucked ass today! Total bottom frags: {frag_counts[user_message]["bottom"]}')  
    #         sorted_frag_counts = sorted(frag_counts.items(), key=lambda x: x[1]['bottom'], reverse=True)
    #         leaderboard = "\n".join([f'{i+1}. {username} = {details["bottom"]} {":poop:" * details["bottom"]}' for i, (username, details) in enumerate(sorted_frag_counts)])

    #         await ctx.send(f"Bottom Fragger Leaderboard:\n{leaderboard}")
    #         with open('frag_counts.json', 'w') as f:
    #             json.dump(frag_counts, f)
    #     except asyncio.TimeoutError:
    #         await ctx.send('No confirmation received, command cancelled.')

    # @bot.command()
    # async def topfrag(ctx, *, user_message):
    #     confirm_message = await ctx.send(f':supervillain: : Are you sure {user_message} was the Top fragger? Confirm with a reaction!')
    #     await ctx.send("You Have 5 seconds to Confirm !")
    #     await confirm_message.add_reaction('✅') 
    #     await confirm_message.add_reaction('❌')  

    #     def check(reaction, user):
        
    #         return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == confirm_message.id
    #     try:
     
    #         reaction, user = await bot.wait_for('reaction_add', timeout=5.0, check=check)

    #         if str(reaction.emoji) == '✅':
    #             if user_message in ["<@1047933870357618821>", "<@312703013720555520>"]:
    #                 await ctx.send(f"Are you sure this mf top fragged?")

    #             frag_counts[user_message] = frag_counts.get(user_message, {'top': 0, 'bottom': 0})
    #             frag_counts[user_message]['top'] += 1
    #             await ctx.send(f'{user_message} is a valo goddddd ! Total top frags: {frag_counts[user_message]["top"]}')
    #             sorted_frag_counts = sorted(frag_counts.items(), key=lambda x: x[1]['top'], reverse=True)

    #             leaderboard_embed = discord.Embed(title="Top Fragger Leaderboard:" ,description="\n".join([f'{i+1}. {username} = {details["top"]} {":star2:" * details["top"]}' for i, (username, details) in enumerate(sorted_frag_counts)]))
    #             sorted_frag_counts_1 = sorted(frag_counts.items(), key=lambda x: x[1]['bottom'], reverse=True)

    #             await ctx.send(embed=leaderboard_embed)
    #             with open('frag_counts.json', 'w') as f:
    #                 json.dump(frag_counts, f)
    #         elif str(reaction.emoji) == '❌':
    #             await ctx.send(f'{user_message} why are u wasting my time ? ')  

    #     except asyncio.TimeoutError:
        
    #         await ctx.send('No confirmation received, command cancelled.')
            
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            command_error = discord.Embed(title="Sorry I couldn't Understand the command !",description="Here is the list of available Commands !\n 1. /topfrag\n2. /bottomfrag\n3. /leaderboard\n4. /val",color=discord.Colour.red())
            await ctx.send(embed=command_error)   
        elif isinstance(error, commands.MissingRequiredArgument):
            if str(error.param) == 'user_message':
                command_error = discord.Embed(title="You must include a user @ after the command Please try again.",description="Here is an Example : \n /topfrag @Hercules ",color=discord.Colour.red())
                await ctx.send(embed=command_error)  
          
    bot.run(TOKEN)
    
