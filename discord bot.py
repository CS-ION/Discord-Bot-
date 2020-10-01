import discord
from discord.ext import commands
from googlesearch import search
from dotenv import load_dotenv
import os
import asyncio
import youtube_dl
from youtubesearchpython import SearchVideos
import random
import sports
from pycricbuzz import Cricbuzz
import ratings
import tracemalloc

tracemalloc.start()

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord...\n")

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        for I in message.embeds:
                if I!=[]:
                    if 'IPL POLLING' in I.title:
                        await message.add_reaction(emoji = '1️⃣')
                        await message.add_reaction(emoji = '2️⃣')
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx , error):
    await ctx.send(f'abe mandbuddhi {ctx.message.author.mention}')
    await ctx.send(error)

load_dotenv()
servers = (os.getenv('server1'),os.getenv('server2'),os.getenv('server3'),os.getenv('server4'),os.getenv('server5'))
song_list = dict.fromkeys(servers,[])
Pause_list = dict.fromkeys(servers, False)

@bot.command(aliases=['seru'])
async def join(ctx):
    global song_list
    global Pause_list
    song_list[ctx.guild.id] = []
    Pause_list[ctx.guild.id] = False
    if ctx.guild.voice_client in bot.voice_clients:
        await ctx.send('abbe hum tumhare baap he, tumhare kehne se pehle aa gaye')
        return
    try:
        await ctx.message.author.voice.channel.connect()
        await ctx.send('swagat to karo humara')
    except:
        await ctx.send('abbe mandbuddhi, VC to join karo')

@bot.command(aliases=['kalikukka','p'])
async def play(ctx,*args):
    
    if  ctx.message.author.voice!=None and (ctx.guild.voice_client in bot.voice_clients):
        
        global song_list
        global Pause_list
        songa = ' '.join(args)
        song_list[ctx.guild.id].append(songa)

        if len(song_list[ctx.guild.id])!=1 or ctx.message.guild.voice_client.is_playing()==True or Pause_list[ctx.guild.id]==True:
            await ctx.send(f'**`{songa}` ko line me lagwa diye he**')

        if ctx.message.guild.voice_client.is_playing()==False and Pause_list[ctx.guild.id]==False:
           download(ctx,ctx.message.guild.voice_client,ctx.guild.id)

    else:
        await ctx.send('abbe mandbuddhi, VC to join karo')       

def download(ctx,voice_client,server_id):
    asyncio.run_coroutine_threadsafe(playing_song(ctx,voice_client,server_id),bot.loop)
    pass

async def playing_song(ctx,voice_client,server_id):

    global song_list
    radio = {'HiFM':os.getenv('HiFM'),
            'Merge':os.getenv('Merge'),
            'Virgin':os.getenv('Virgin') }
    
    try:
        song = song_list[server_id][0]
    except:
        return
    song_list[server_id].pop(0)

    if song in radio.keys():
        voice_client.play(discord.FFmpegPCMAudio(radio[song]),after =lambda e: download(ctx,voice_client,server_id))
        await ctx.send(f'Now Playing : {song} Radio') 
        return
    
    results = SearchVideos(song,offset=1,mode='dict',max_results=1)
    x = results.result()
    for I in x['search_result']:

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
    
    embed = discord.Embed(title=f"*ab suno\n`{I['title']}`\naur apna manorajan karo*", colour=discord.Colour.red())
    embed.set_thumbnail(url = I['thumbnails'][0])
    embed.add_field( name='Duration' , value = I['duration'])
    await ctx.send(embed=embed)

    if voice_client.is_playing()==False:

        audio = ytdl.extract_info(I['link'],download = False)
        streamable_url = audio['formats'][0]['url']
        before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        voice_client.play(discord.FFmpegPCMAudio(streamable_url,before_options = before_options),after =lambda e: download(ctx,voice_client,server_id))

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
            await ctx.send(f'kya yaar, `{song_list[ctx.guild.id][position-1]}` humse hi hatwana tha')
            song_list[ctx.guild.id].pop(position-1)
        except:
            await ctx.send('ek minute... ye kya, tumhara to number hi line ke bahar he')
    else:
        await ctx.send('abbe mandbuddhi, VC to join karo')
    
@bot.command(aliases = ['niruthu'])
async def pause(ctx):
    global Pause_list
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    ctx.message.guild.voice_client.pause()
    Pause_list[ctx.guild.id] = True
    await ctx.send('kya yaar beech me rok kar poora maza kharab kar diye')
    
@bot.command(aliases = ['thodurum'])
async def resume(ctx):
    global Pause_list
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    ctx.message.guild.voice_client.resume()
    Pause_list[ctx.guild.id] = False
    await ctx.send('je hui na baat ab maze karo')

@bot.command(aliases = ['poda_patti','s'])
async def skip(ctx):
    global Pause_list
    if ctx.message.author.voice == None:
        await ctx.send('abbe mandbuddhi, VC to join karo')
        return
    Pause_list[ctx.guild.id] = False
    ctx.message.guild.voice_client.stop()
    await ctx.send('kya yaar, itne badhiya gane ko hata diya')
   
@bot.command(aliases = ['poda','d'])
async def disconnect(ctx):
    global Pause_list
    global song_list
    for x in bot.voice_clients:
        if(x.guild == ctx.message.guild):
            song_list[ctx.guild.id]=[]
            Pause_list[ctx.guild.id] = False
            await ctx.send('phir milte he')
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
    duplicate = []
    for I in bot.get_all_members():
        if ctx.guild == I.guild:
            if I.name in duplicate:
                continue
            await ctx.send(I.name)
            duplicate.append(I.name)

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
    hershel=['https://cdn.discordapp.com/emojis/742244405523513344.png?v=1',
    'https://cdn.discordapp.com/emojis/735902946432254083.png?v=1',
    'https://cdn.discordapp.com/emojis/727173056073564220.png?v=1']
    await ctx.send('https://cdn.discordapp.com/emojis/736858611627851787.png?v=1')
    await ctx.send('https://cdn.discordapp.com/emojis/736858136790564966.png?v=1')
    await ctx.send(random.choice(hershel))

@bot.command()
async def SC(ctx):
    sc = ['https://cdn.discordapp.com/emojis/726719083076255755.png?v=1',
    'https://cdn.discordapp.com/emojis/727172647519125544.png?v=1',
    'https://cdn.discordapp.com/emojis/750210732184043580.png?v=1',
    'https://cdn.discordapp.com/emojis/760778635937841153.png?v=1']
    await ctx.send(random.choice(sc))

@bot.command()
async def NizwaHC(ctx):
    romir = ['https://cdn.discordapp.com/emojis/728912662083403847.png?v=1',
             'https://cdn.discordapp.com/attachments/674567305291890701/760782607373303828/unknown.png']
    await ctx.send(random.choice(romir))

@bot.command()
async def MuscatHC(ctx):
    ramna=['https://cdn.discordapp.com/emojis/743124529471160401.png?v=1',
           'https://cdn.discordapp.com/emojis/727881883987476490.png?v=1',
           'https://cdn.discordapp.com/emojis/760779912587509771.png?v=1']
    ronek=['https://cdn.discordapp.com/emojis/727889938674352169.png?v=1',
           'https://cdn.discordapp.com/emojis/727890732190531644.png?v=1']
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
             'https://media.discordapp.net/attachments/674638164467515432/753289976589975753/SPOILER_9k.png',
             'https://media.discordapp.net/attachments/674567305291890701/760773029193318440/Z.png?width=400&height=251']
    await ctx.send(random.choice(memes))
                   
@bot.command()
async def girlfriend(ctx, arg):
    gfs = {
        'salman' : 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/201310/salman-kat-and-ash_story-size_660_100813113758.jpg'
    }

    await ctx.send(gfs.get(arg.lower(), "kiski girlfriend pooch rahe ho <:abeysaale:731486907208433724>"))

@bot.command()
async def pingu(ctx, member:discord.Member):
    if member.discriminator == '4777':
        await ctx.send('poda patti')
        return
    n=0
    while n<6:
        await ctx.send(member.mention)
        n=n+1

@bot.command()
async def everyone(ctx):

    L = [os.getenv('Vivek'),
    os.getenv('Dannyboi'),
    os.getenv('ValdyFox'),
    os.getenv('FractalsAreBae'),
    os.getenv('Silent_Killer'),
    os.getenv('SKULL_TROOPER'),
    os.getenv('jetso'),
    os.getenv('yallaboi'),]

    for I in L:
        if I == ctx.message.author.id :
            continue
        await ctx.send(f'<@!{I}>')

@bot.command()
async def ipl(ctx):
    match = sports.get_match(sports.CRICKET, 's', 'a')
    if match.match_time == 'Match Finished':
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return
    embed = discord.Embed(title='IPL 2020', colour=discord.Colour.gold())
    embed.add_field(name=match.away_team , value=match.away_score , inline = False)
    embed.add_field(name=match.home_team , value=match.home_score , inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def current_score(ctx):   
    match = Cricbuzz()
    try:
        details = match.livescore(match_id())
        embed1 = discord.Embed(title=f"Current Batting Team : {details['batting']['team']}", colour=discord.Colour.red())
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return

    embed1.add_field(
            name = f"Batsman Name : {details['batting']['batsman'][0]['name']}",
            value = f"Runs Scored : {details['batting']['batsman'][0]['runs']}\n"
            f"Balls Faced : {details['batting']['batsman'][0]['balls']}\n"
            f"Fours Hit : {details['batting']['batsman'][0]['fours']}\n"
            f"Sixes Hit : {details['batting']['batsman'][0]['six']}\n",
            inline = False)
    
    embed1.add_field(
            name = f"Batsman Name : {details['batting']['batsman'][1]['name']}",
            value = f"Runs Scored : {details['batting']['batsman'][1]['runs']}\n"
            f"Balls Faced : {details['batting']['batsman'][1]['balls']}\n"
            f"Fours Hit : {details['batting']['batsman'][1]['fours']}\n"
            f"Sixes Hit : {details['batting']['batsman'][1]['six']}\n",
            inline = False)
    
    await ctx.send(embed = embed1)

    embed2 = discord.Embed(title=f"Current Bowling Team : {details['bowling']['team']}", colour=discord.Colour.green())
    
    embed2.add_field(
        name = f"Bowler Name : {details['bowling']['bowler'][0]['name']}",
        value = f"Overs Done : {details['bowling']['bowler'][0]['overs']}\n"
        f"Runs Given : {details['bowling']['bowler'][0]['runs']}\n"
        f"Wickets Taken : {details['bowling']['bowler'][0]['wickets']}",
        inline = False)
    
    await ctx.send(embed = embed2)    

def match_id():
    c = Cricbuzz()
    matches = c.matches()
    for I in matches:
        if I['srs']=='Indian Premier League 2020' and (I['mchstate']=='toss' or I['mchstate']=='inprogress'):
            return I['id']

@bot.command()
async def teams(ctx):
    c = Cricbuzz()
    try:
        I = c.matchinfo(match_id())
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return
    embed1 = discord.Embed(title= I['team1']['name'], colour=discord.Colour.blue())
    for X,J in enumerate(I['team1']['squad']):
        embed1.add_field(name = J,value = f'{X+1}',inline = False)
    embed2 = discord.Embed(title= I['team2']['name'], colour=discord.Colour.gold())
    for X,J in enumerate(I['team2']['squad']):
        embed2.add_field(name = J,value = f'{X+1}',inline = False)
    await ctx.send(embed = embed1)
    await ctx.send(embed = embed2) 

@bot.command()
async def status(ctx):
    c = Cricbuzz()
    try:
        I = c.matchinfo(match_id())
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return
    await ctx.send(I['status'])

@bot.command()
async def toss(ctx):
    c = Cricbuzz()
    try:
        I = c.matchinfo(match_id())
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return
    await ctx.send(I['toss'])

@bot.command()
async def venue(ctx):
    c = Cricbuzz()
    try:
        match = c.matchinfo(match_id())
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return
    match = c.matchinfo(match_id())
    await ctx.send(match["venue_name"])
    await ctx.send(match['venue_location'])
    
@bot.command()
async def score_card(ctx):
    c = Cricbuzz()
    try:
        scorecard = c.scorecard(match_id())['scorecard'][0]
    except:
        await ctx.send('abe saale abhi to koi game nahi chal raha hai')
        return

    embed1 = discord.Embed(title = f"Batting Team : {scorecard['batteam']}" , colour=discord.Colour.blue())
    embed1.description = f"Score {scorecard['runs']}/{scorecard['wickets']}, Overs {scorecard['overs']}"
    for I in scorecard['batcard']:
        embed1.add_field(
                        name=I['name'],
                        value=f"Runs{I['runs']}\n"
                        f"Balls Faced {I['balls']}\n"
                        f"Fours {I['fours']}\n"
                        f"Sixes {I['six']}\n"
                        f"{I['dismissal']}",
                        inline = False)

    embed2 = discord.Embed(title = f"Bowling Team : {scorecard['bowlteam']}" , colour=discord.Colour.gold())
    for I in scorecard['bowlcard']:
        embed2.add_field(
                        name=I['name'],
                        value=f"Overs : {I['overs']}\n"
                        f"Maidens : {I['maidens']}\n"
                        f"Runs Given : {I['runs']}\n"
                        f"Wickets Taken : {I['wickets']}\n"
                        f"wides : {I['wides']}\n"
                        f"no balls : {I['nballs']}",
                        inline = False)
    
    await ctx.send(embed = embed1)
    await ctx.send(embed = embed2)

@bot.command()
async def prev_match(ctx):
    c = Cricbuzz()
    matches = c.matches()
    for I in matches:
        if I['srs']=='Indian Premier League 2020' and I['mchstate']=='mom':
            embed = discord.Embed(title = f"{I['team1']['name']} vs {I['team2']['name']}" , colour = discord.Colour.blue())
            embed.description = f"{I['status']}"
            await ctx.send(embed = embed)

@bot.command()
async def next_match(ctx):
    c = Cricbuzz()
    matches = c.matches()
    for I in matches:
        if I['srs']=='Indian Premier League 2020' and I['mchstate']=='preview':
            embed = discord.Embed(title = f"{I['team1']['name']} vs {I['team2']['name']}" , colour = discord.Colour.blue())
            embed.description = f"{I['status']}"
            await ctx.send(embed = embed)

@bot.command()
async def poll(ctx):
    c = Cricbuzz()
    matches = c.matches()
    for I in matches:
        if I['srs']=='Indian Premier League 2020' and (I['mchstate']=='inprogress' or I['mchstate']=='preview'):
            embed = discord.Embed(title = f"IPL POLLING\n{I['team1']['name']} vs {I['team2']['name']}" , colour = discord.Colour.blue())
            embed.description = f"{I['team1']['name']} : 1️⃣\n\n{I['team2']['name']} : 2️⃣ "
            await ctx.send(embed = embed)
  
@bot.command()
async def football(ctx,*args):
    try:
        match = sports.get_match(sports.SOCCER, args[0], args[2])
    except:
        await ctx.send('abe shuru to hone do')
        return
    embed = discord.Embed(title = ' '.join(args).upper(), colour=discord.Colour.blurple()) 
    embed.description = f'{match.league}'
    embed.add_field( name = f'{match.away_team}', value =  f'{match.away_score}')
    embed.add_field( name = f'{match.home_team}' , value = f'{match.home_score}')
    await ctx.send(embed = embed)

@bot.command()
async def rating(ctx,*args):
    key = ratings.get_player(' '.join(args))
    if key == None:
        await ctx.send('sorry yaar player not found')
        return
    elif type(key)==int:
        await ctx.send(f'https://media.contentapi.ea.com/content/dam/ea/fifa/fifa-21/ratings-collective/f20assets/player-shields/{key}.png')
    else:
        await ctx.send(key)
                                 
@bot.command()
async def ping(ctx):
    await ctx.send(f'rukawat ki khed he\nping : {round(bot.latency,2)}')

@bot.command()
async def dhanyavaad(ctx):
    if ctx.message.author.id == 518342269955342347 :
        await ctx.send('aate hai')
        await ctx.bot.logout()
    else :
        await ctx.send('bhediyon me itna dam nahi ki sheron ko bhaga sake')

token=os.getenv('token')
bot.run(token)
