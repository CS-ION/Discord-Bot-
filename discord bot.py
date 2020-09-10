import discord
from discord.ext import commands
from googlesearch import search
from dotenv import load_dotenv
import os
import youtube_dl
from youtubesearchpython import SearchVideos
import asyncio
import random

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord...\n")
    
    for file in os.listdir():
        if file.endswith('.mp3'):
            os.remove(file)

song_list = {'674567305291890698':[],'735195524122017923':[],'753491412258914395':[]}
        
@bot.command(aliases=['seru'])
async def join(ctx):
    global song_list
    song_list[ctx.guild.id] = []
    if ctx.guild.voice_client in bot.voice_clients:
        await ctx.send('abbe hum tumhare baap he, tumhare kehne se pehle aa gaye')
        return
    try:
        await ctx.message.author.voice.channel.connect()
    except:
        await ctx.send('abbe mandbuddhi, VC to join karo')

@bot.command(aliases=['kalikukka','p'])
async def play(ctx,*args):
    
    if  ctx.message.author.voice!=None and (ctx.guild.voice_client in bot.voice_clients):
        
        global song_list
        songa = ' '.join(args)
        song_list[ctx.guild.id].append(songa)

        await ctx.send(f'**`{songa}` ko line me lagwa diye he**')

        if ctx.message.guild.voice_client.is_playing()==False and 'buffer_list[ctx.guild.id] != []':
            download(ctx.message.guild.voice_client,ctx.guild.id)
        else:
            return
    else:
        await ctx.send('abbe mandbuddhi, VC to join karo')       

def download(voice_client,server_id):

    global song_list
    global buffer_list
    
    try:
        song = song_list[server_id][0]
    except:
        return
    song_list[server_id].pop(0)

    for file in os.listdir():
                if file.endswith('.mp3'):
                    os.remove(file)

    results = SearchVideos(song,offset=1,mode='dict',max_results=1)
    x = results.result()
    for I in x['search_result']:
        songa = I['title']

        #await ctx.send(f'*ruko burbak `{songa}` ko download hone do*')

        ytdl_format_options = {
                'format' : 'bestaudio/best' ,
                'postprocessors' : [{
                       'key' : 'FFmpegExtractAudio' ,
                       'preferredcodec' : 'mp3' ,
                       'preferredquality' : '192' ,
                       }]
                }

        ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        #ytdl.download([I['link']])

    #await ctx.send(f'*ab suno`{songa}` aur apna manorajan karo*')

    if voice_client.is_playing()==False:

        audio = ytdl.extract_info(I['link'],download = False)
        streamable_url = audio['formats'][0]['url']
        before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        voice_client.play(discord.FFmpegPCMAudio(streamable_url,before_options = before_options),after =lambda e: download(voice_client,server_id))
    
       
        for file in os.listdir():
            if file.endswith('.mp3'):
                voice_client.play(discord.FFmpegPCMAudio(file),after =lambda e: download(voice_client,server_id))

    else:
        return
    
@bot.command(aliases=['line','q'])
async def queue(ctx):
    global song_list
    if  ctx.message.author.voice!=None:
        if song_list[ctx.guild.id] == []:
            await ctx.send('jab koi line he hi nahi to kya dekho ge be')
            return
        for i,s in enumerate(song_list[ctx.guild.id]):
            await ctx.send(f'*{i+1})*: **`{s}`**')
    else:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        
@bot.command(aliases = ['hatt','r'])
async def remove(ctx,position : int):
    global song_list
    if  ctx.message.author.voice!=None:
        if song_list[ctx.guild.id] == []:
            await ctx.send('jab koi line he hi nahi to kya hatao ge be')
            return
        try :
            await ctx.send(f'kya yaar, `{song_list[position-1]}` humse hi hatwana tha')
            song_list[ctx.guild.id].pop(position-1)
        except:
            await ctx.send('ek minute... ye kya, tumhara to number hi line ke bahar he')
    else:
        await ctx.send('abbe mandbuddhi, VC to join karo')
    

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
            song_list[ctx.guild.id]=[]
            return await x.disconnect()
    if bot.voice_clients==[]:
        await ctx.send('abbe hum gaye hi kab jo tum humko nikaloge')

@bot.command()
async def kick(ctx, member : discord.Member):
    await member.kick(reason = None)
    await ctx.send(f'{member.mention} ko dhakke maar ke nikal diye he be')

@bot.command()
async def b(ctx , no : int):
    await ctx.message.channel.purge(limit=no)
    
@bot.command()
async def member_count(ctx):
        await ctx.send(ctx.message.guild.member_count)

@bot.command()
async def all_members(ctx):
    for I in bot.get_all_members():
        await ctx.send(I.name)

@bot.command()
async def change(ctx, member : discord.Member, *args):
    new = ' '.join(args)
    await member.edit(nick = new)

@bot.command()
async def avatar(ctx, user: discord.User = None):
    if user==None:
        user = ctx.message.author
    await ctx.send(user.avatar_url_as())

@bot.command()
async def mobile(ctx , member : discord.Member):
    if member.is_on_mobile() == True :
        await ctx.send('kaun sa mobilewa pe ho be , nokia ?')
    elif member.is_on_mobile() == False:
        await ctx.send('PC use karta hai bade aadmi kahin ka')
    
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

    await ctx.send(roasts.get(arg.lower(),"kiska naam diya hai <:abeysaale:731486907208433724>"),tts = True)

@bot.command()
async def proifucts(ctx):
    hershel=['https://cdn.discordapp.com/emojis/742244405523513344.png?v=1','https://cdn.discordapp.com/emojis/735902946432254083.png?v=1','https://cdn.discordapp.com/emojis/727173056073564220.png?v=1']
    await ctx.send('https://cdn.discordapp.com/emojis/736858611627851787.png?v=1')
    await ctx.send('https://cdn.discordapp.com/emojis/736858136790564966.png?v=1')
    await ctx.send(random.choice(hershel))

@bot.command()
async def SC(ctx):
    sc = ['https://cdn.discordapp.com/emojis/726719083076255755.png?v=1','https://cdn.discordapp.com/emojis/727172647519125544.png?v=1','https://cdn.discordapp.com/emojis/750210732184043580.png?v=1']
    await ctx.send(random.choice(sc))

@bot.command()
async def NizwaHC(ctx):
    await ctx.send('https://cdn.discordapp.com/emojis/728912662083403847.png?v=1')

@bot.command()
async def MuscatHC(ctx):
    ramna=['https://cdn.discordapp.com/emojis/743124529471160401.png?v=1','https://cdn.discordapp.com/emojis/727881883987476490.png?v=1']
    ronek=['https://cdn.discordapp.com/emojis/727889938674352169.png?v=1','https://cdn.discordapp.com/emojis/727890732190531644.png?v=1']
    await ctx.send(random.choice(ramna))
    await ctx.send(random.choice(ronek))
    
@bot.command()
async def meme(ctx):
    memes = ['https://media.discordapp.net/attachments/674638164467515432/753290676351008928/4bpjdv.png?width=362&height=406',
             'https://media.discordapp.net/attachments/674638164467515432/753290636093948084/Z.png?width=412&height=406',
             'https://media.discordapp.net/attachments/674638164467515432/753290581677178920/20200820_093621.png?width=356&height=406',
             'https://media.discordapp.net/attachments/674638164467515432/753290525259464844/SPOILER_bruh.png',
             'https://media.discordapp.net/attachments/674638164467515432/753290466430025798/SPOILER_Z.png',
             'https://media.discordapp.net/attachments/674638164467515432/753290416861872278/9k.png',
             'https://media.discordapp.net/attachments/674638164467515432/753290299165507634/SPOILER_9k.png',
             'https://media.discordapp.net/attachments/674638164467515432/753290251254104094/SPOILER_Z.png',
             'https://media.discordapp.net/attachments/674638164467515432/753290178944172102/SPOILER_Z.png?width=817&height=406',
             'https://media.discordapp.net/attachments/674638164467515432/753290066515853332/SPOILER_lmaoooo.png',
             'https://images-ext-1.discordapp.net/external/b2bXXz8lOxAnfYAbXuVYRxGAEuGT984QVhkWu96H5OQ/%3Fwidth%3D313%26height%3D375/https/media.discordapp.net/attachments/674567305291890701/752818609994203186/SPOILER_MR_CHIRKU.png',
             'https://media.discordapp.net/attachments/674638164467515432/753289976589975753/SPOILER_9k.png']
    await ctx.send(random.choice(memes))
                   
@bot.command()
async def girlfriend(ctx, arg):
    gfs = {
        'salman' : 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/201310/salman-kat-and-ash_story-size_660_100813113758.jpg'
    }

    await ctx.send(gfs.get(arg.lower(), "kiski girlfriend pooch rahe ho <:abeysaale:731486907208433724>"))

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
