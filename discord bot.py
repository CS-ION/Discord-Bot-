import discord
from discord.ext import commands
from googlesearch import search
from dotenv import load_dotenv
import os
import youtube_dl
from youtube_search import YoutubeSearch

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord...\n")
    
    for file in os.listdir():#cleanup
        if file.endswith('.mp3'):
            os.remove(file)

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    '''
    if 'lol' in message.content.lower() or 'lmao' in message.content.lower():
        await message.channel.send('https://giphy.com/gifs/SalmanKhanFilms-lol-lmao-rofl-XHpoWfKOXwldWj6AqD')
    if 'nitishna' in message.content.lower() or 'prachi' in message.content.lower():
        await message.channel.send('https://giphy.com/gifs/bypriyashah-alia-bhatt-the-kapil-sharma-show-3ohfFjT9c0GPfGkZ0I')
        
    if message.author.id == int(os.getenv('ramanna')):
        await message.author.edit(nick='UMAGA MO-LOL-ITY')
    if message.author.id == int(os.getenv('jerin')):
        await message.author.edit(nick='UMAGA BATGIRL')
    '''
    
    await bot.process_commands(message)

song_list = []

@bot.command(aliases=['seru'])
async def join(ctx):
    global song_list
    song_list = []
    try:
        await ctx.message.author.voice.channel.connect()
    except:
        await ctx.send('abbe mandbuddhi, VC to join karo')


@bot.command(aliases=['kalikukka','p'])
async def play(ctx,*args):

    global song_list
    
    if  ctx.message.author.voice!=None and bot.voice_clients!=[]:

        if ctx.message.guild.voice_client.is_playing()==True:
            song = ' '.join(args)
            song_list.append(song)
            await ctx.send(f'**`{song}` ko line me lagwa diye he**')
            return

        for file in os.listdir():
            if file.endswith('.mp3'):
                os.remove(file)

        if song_list == []:
            song = ' '.join(args)
        else :
            song = song_list[0]
            song_list.pop(0)
            song_list.append(' '.join(args))
            
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
        await ctx.send(f'*ruko burbak `{song}` ko download hone do*')
        ytdl.download([url])
        await ctx.send(f'**ab suno `{song}` aur apna manoranjan karo**')
        #add embed 
        for file in os.listdir():
            if file.endswith('.mp3'):
                ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(file))


@bot.command(aliases=['line','q'])
async def queue(ctx):
    global song_list
    if song_list == []:
        await ctx.send('jab koi line he hi nahi to kya dekho ge be')
        return
    
    for i,s in enumerate(song_list):
        await ctx.send(f'*{i+1})*: **`{s}`**')
        

@bot.command(aliases = ['hatt','r'])
async def remove(ctx,position : int):
    global song_list
    if song_list == []:
        await ctx.send('jab koi line he hi nahi to kya hatao ge be')
        return

    try :
        await ctx.send(f'kya yaar, `{song_list[position-1]}` humse hi hatwana tha') #yeh gunda ko even i wanted to hatt
        song_list.pop(position-1)
    except:
        await ctx.send('ek minute... ye kya, tumhara to number hi line ke bahar he')
    

@bot.command(aliases = ['niruthu'])
async def pause(ctx):
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    ctx.message.guild.voice_client.pause()
    await ctx.send('kya yaar beech me rok kar poora maza kharab kar diye')
    
@bot.command(aliases = ['thodurum'])
async def resume(ctx):
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    ctx.message.guild.voice_client.resume()
    await ctx.send('je hui na baat ab maze karo')

@bot.command(aliases = ['poda_patti','s'])
async def skip(ctx):
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    ctx.message.guild.voice_client.stop()
    await ctx.send('kya yaar, itne badhiya gane ko hata diya')

@bot.command(aliases = ['poda','d'])
async def disconnect(ctx):
    global song_list
    for x in bot.voice_clients:
        if(x.guild == ctx.message.guild):
            song_list = []
            return await x.disconnect()
    if bot.voice_clients==[]:
        await ctx.send('abbe hum gaye hi kab jo tum humko nikaloge')

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
    roasts = {
    'krishna': 'Smoking will kill you... meth will kill you... But, smoking meth will cure it.',
    'vivek' : 'vivek got stuck in the shower because the instructions on the shampoo bottle said: Lather, Rinse, Repeat',
    'ramanan' : 'What did the ramanan write on his Valentine card? You make me and my ice cream melt.',
    'ramil' : 'why does ramil have white teeth ... because he loves to floss',
    'harshal' : 'harshal has a new theory on inertia but it doesnt seem to go anywhere',
    'rounak' : 'i am gorgeus and so am i a chirkut .... thats what she says',
    'ayaan' : 'mere selmon bhoi ke bare me kya boli',
    'nitishna' : 'my relationship with abi in NY was basically ''money heist'' ... IYKWIM',
    'abishai':'absishais favourite tea .... penal-tea',
    'jerin' : 'im a rider,provider,bring my bed now imma sleep right here',
    'shane' : 'I will have a English Breakfast Tea with a pinch of sugar and a tinge of mint in it, you peasant worker',
    'manav' : 'even my mom ignores me and only asks if u have any khakras left after i return from school',
    'ujjwal' : 'naam he mera ujjwal babu aur me lollipop lagelu',
    'vineet' : 'even mcdonalds had to shut down their farms coz you ate all their poultry'
    }

    await ctx.send(roasts.get(arg.lower(),"kiska naam diya hai <:abeysaale:731486907208433724>"))

@bot.command()
async def dhanyavaad(ctx):
    if ctx.message.author.id == 518342269955342347 :
        await ctx.send('aate hai')
        for file in os.listdir():
            if file.endswith('.mp3'):
                os.remove(file)
        await ctx.bot.logout()
    else :
        await ctx.send('bhediyon me itna dam nahi ki sheron ko bhaga sake')

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
bot.run(token)


