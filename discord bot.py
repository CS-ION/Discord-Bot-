import discord
from discord.ext import commands
from googlesearch import search
from dotenv import load_dotenv
import os
import youtube_dl
from youtube_search import YoutubeSearch

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    load_dotenv()
    if message.author.id == int(os.getenv('ramanna')):
        message.author.edit(nick='UMAGA PODD')
    if message.author.id == int(os.getenv('jerin')):
        message.author.edit(nick='UMAGA BATGIRL')
    
    await bot.process_commands(message)

@bot.command()
async def join(ctx):
    try:
            await ctx.message.author.voice.channel.connect()
    except:
            pass

@bot.command()
async def play(ctx,*args):
    if  ctx.message.author.voice!=None and bot.voice_clients!=[]:

        song = ' '.join(args)
        results = YoutubeSearch(song, max_results=1).to_dict()
        for I in results:
            url = 'https://www.youtube.com'+ I['url_suffix']
        
        ytdl_format_options = {
            'format' : 'bestaudio/best' ,
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio' ,
                'preferredcodec' : 'mp3' ,
                'preferredquality' : '192' ,
             }]
        }

        ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        await ctx.send('ruko burbak gane ko download hone do')
        ytdl.download([url])
        await ctx.send('ab suno gana aur apna manoranjan karo')

        for file in os.listdir():
            if file.endswith('.mp3'):
                ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(file))

@bot.command()
async def pause(ctx):
        ctx.message.guild.voice_client.pause()        
@bot.command()
async def resume(ctx):
        ctx.message.guild.voice_client.resume()
@bot.command()
async def skip(ctx):
        ctx.message.guild.voice_client.stop()

@bot.command()
async def poda(ctx):
    for x in bot.voice_clients:
        print(bot.voice_clients)
        if(x.guild == ctx.message.guild):
            return await x.disconnect()

@bot.command()
async def b(ctx):
    await ctx.message.channel.purge(limit=2)
    
@bot.command()
async def member_count(ctx):
    await ctx.send(ctx.message.guild.member_count)

@bot.command()
async def all_members(ctx):
    for I in bot.get_all_members():
        await ctx.send(I.name)

@bot.command()
async def avatar(ctx, user: discord.User = None):
    if user==None:
        user = ctx.message.author
    await ctx.send(user.avatar_url_as())
    
@bot.command()
async def Q(ctx,*args):
            question= ' '.join(args)
            for j in search(question, tld="co.in", num=1, stop=1, pause=2):
                await ctx.send(j)
        
@bot.command()
async def roast(ctx,arg):
        if 'krishna' in arg.lower():
            await ctx.send('Smoking will kill you... meth will kill you... But, smoking meth will cure it.')
        if 'vivek' in arg.lower():
            await ctx.send('vivek got stuck in the shower because the instructions on the shampoo bottle said: Lather, Rinse, Repeat')
        if 'ramanan' in arg.lower():
            await ctx.send('What did the ramanan write on his Valentine card? You make me and my ice cream melt.')
        if 'ramil' in arg.lower():
            await ctx.send('why does ramil have white teeth ... because he loves to floss')
        if 'harshal' in arg.lower():
            await ctx.send('harshal has a new theory on inertia but it doesnt seem to go anywhere')
        if 'rounak' in arg.lower():
            await ctx.send('i am gorgeus and so am i a chirkut .... thats what she says')
        if 'ayaan' in arg.lower():
            await ctx.send('mere selmon bhoi ke bare me kya boli')
        if 'nitishna' in arg.lower():
            await ctx.send('my relationship with abi in NY was basically ''money heist'' ... IYKWIM')
        if 'abishai' in arg.lower():
            await ctx.send('absishais favourite tea .... penal-tea')
        if 'jerin' in arg.lower():
            await ctx.send('im a rider,provider,bring my bed now imma sleep right here')
        if 'shane' in arg.lower():
            await ctx.send('I will have a English Breakfast Tea with a pinch of sugar and a tinge of mint in it, you peasant worker')
        if 'manav' in arg.lower():
            await ctx.send('even my mom ignores me and only asks if u have any khakras left after i return from school')
        if 'ujjwal' in arg.lower():
            await ctx.send('naam he mera ujjwal babu aur me lollipop lagelu')
        if 'vineet' in arg.lower():
            await ctx.send('even mcdonalds had to shut down their farms coz you ate all their poultry')

@bot.command()
async def dhanyavaad(ctx):
    if ctx.message.author.id == 518342269955342347 :
        await ctx.send('aate hai')
        await ctx.bot.logout()
    else :
        await ctx.send('bhediyon me itna dam nahi ki sheron ko bhaga sake')

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
bot.run(token)
