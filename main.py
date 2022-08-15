import discord
from discord.ui import Button , View , Select
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find
import asyncpg
import random
import asyncio
import os







companies = ['streetband','farming','restaurant']

async def get_prefix(bot,message):
    guild = message.guild.id
    prefix_ = await bot.db.fetch('SELECT prefix FROM server_prefix WHERE guilds_id = $1',guild)
    if prefix_ == []:
        PREFIX = '.'
    else:
        PREFIX = prefix_[0]['prefix']
    global prefix
    prefix = PREFIX
    return PREFIX


bot = commands.Bot(command_prefix=get_prefix,
status = discord.Status.idle,
intents= discord.Intents.all())  
bot.remove_command("help")

async def cogs():
    initial_extensions = []
    for filename in os.listdir('./cogs') :
        if filename.endswith('.py'):
            initial_extensions.append("cogs." + filename [:-3])

    if __name__ == '__main__':
        for extension in initial_extensions :
            await bot.load_extension (extension)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(".help"))
    print('ok')        

async def create_db_pool():
    bot.db = await asyncpg.create_pool(dsn="postgres://postgres:password@localhost:5432/TeamWork")
    print ("Connection successful")

async def main():      
    await cogs()
    await create_db_pool() # again, no need to run with AbstractLoopEvent if you can await
    await bot.start(token)
    await update_stats()

@bot.event
async def on_command_error (ctx, error) :
        if isinstance (error, commands.CommandOnCooldown): #checks if on cooldown
            embed = discord.Embed(
                title = ('**Daddy chill**'),
                description = ("try again in **{:.2f}** seconds".format)(error.retry_after),
                colour = discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance (error, commands.CommandNotFound): pass
        else:
            await ctx.send(embed=await embeding(ctx,None,error,'red'))

@bot.event
async def on_guild_join(guild1:discord.Guild):
    guild = bot.get_guild(918741403306164285)
    server_join = find(lambda x: x.name == 'server_join',  guild.text_channels)
    general = find(lambda x: x.name == 'general',  guild1.text_channels)
    await server_join.send(embed=await embeding(server_join,'Lessgooo','Bot joined a new server:`{0}`!'.format(guild1.name),'green'))
    generalbed = discord.Embed(title = guild1.name,color=discord.Color.random())
    generalbed.add_field(name='Thanks For Inviting TeamWork Here!',value=f'Teamwork Is A Multiplayer Economy Bot, Where You Grow Together As A Team!\nTo Get Started , Use `.new` And See All The Commands Using `.help`')
    generalbed.set_footer(text='Confused? Feel Free To Join Our Server!')
    await general.send(embed=generalbed)


@bot.event
async def on_guild_remove(guild1:discord.Guild):
    guild = bot.get_guild(918741403306164285)
    general = find(lambda x: x.name == 'server_join',  guild.text_channels)
    await general.send(embed=await embeding(general,'NOOOO','Bot left a server:`{0}`!'.format(guild1.name),'red'))
    print(guild1.link)


'''@tasks.loop(minutes=30)
async def update_stats():
    dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk4MzAwMzI4MDg1MjU0NTYwNiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjU5NTAyNTE3fQ.R5tK1bmLQHw1V-p_UH80YXvrXxRWSXDvTNB9TZ-rlEQ"  # set this to your bot's Top.gg token
    bot.topggpy = topgg.DBLClient(bot, dbl_token)
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        await bot.topggpy.post_guild_count()
        print(f"Posted server count ({bot.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")'''


async def embeding(ctx,title,description,colourr):
    if colourr == 'red':
        embed = discord.Embed(title=title,description=description,color = discord.Color.red())
    elif colourr == 'green':
        embed = discord.Embed(title=title,description=description,color = discord.Color.green())
    elif colourr == 'blue':
        embed = discord.Embed(title=title,description=description,color = discord.Color.blue())
    elif colourr == 'orange':
        embed = discord.Embed(title=title,description=description,color = discord.Color.orange())
    elif colourr == 'random':
        embed = discord.Embed(title=title,description=description,color= discord.Color.random())
    return embed
   
async def stringtolist(string):
    if string == None:
        return 'error string to list'
    else:
        try:
            listRes = list(string.split(","))
            return listRes
        except:
            return string


async def listtostring(listt):
    listt = str(listt)
    listt = listt.replace('[','')
    listt = listt.replace(']','')
    listt = listt.replace("'",'')
    listt = listt.replace(" ",'')
    return listt

async def listtostring2(listt):
    listt = str(listt)
    listt = listt.replace('[','')
    listt = listt.replace(']','')
    listt = listt.replace("'",'')
    return listt

async def get_money(ctx,user,balance,profit):
    await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2',balance+profit,user)

async def item_info(ctx,infoo,item):
    info = await ctx.bot.db.fetch(f'SELECT {infoo} FROM item WHERE item_id = $1',item)
    return info[0][infoo]

async def recordtolist(record,recordname):
   record = str(record)
   record = record.replace('[','') 
   record = record.replace(']','') 
   record = record.replace('<','') 
   record = record.replace('>','') 
   record = record.replace("'",'') 
   record = record.replace("=",'') 
   record = record.replace(" ",'') 
   record = record.replace(recordname,'') 
   record = record.replace("Record",'') 
   record = list(record.split(','))
   return record

async def checking(ctx,member):
    try:
        check = await ctx.bot.db.fetch('SELECT user_id FROM teamwork WHERE user_id = $1', member)
        return True
    except:
        await ctx.send(await embeding(ctx, "**uhhh you forgettin smth**", "Create an account first!", "red"))
        return False
    
async def user_object(ctx,idd,member:discord.Member = None):
    user = member or await bot.fetch_user(idd)
    return user

async def status(ctx,user):
    if user.status == discord.Status.online:
        return '🟢'
    elif user.status == discord.Status.idle:
        return user
    elif user.status == discord.Status.offline:
        return '⚫'
    else:
        return '🔴'
    await ctx.send(str(user))

@bot.command()
async def hello(ctx):
    statuss = await status(ctx,ctx.author)
    await ctx.send(f'{statuss}{ctx.author}')
    
@bot.command()
async def new(ctx):
    user_id = ctx.author.id
    user = await bot.fetch_user(user_id)
    check = await ctx.bot.db.fetch('SELECT user_id FROM teamwork WHERE user_id = $1', user_id)
    if check != []:
        await ctx.send(embed=await embeding(ctx, '**uhhh**', 'You already have an account!', 'red'))
    else:
        guild = bot.get_guild(918741403306164285)
        server_join = find(lambda x: x.name == 'server_join',  guild.text_channels)
        await ctx.bot.db.execute('INSERT INTO stats(user_id) VALUES ($1)',user_id)
        await ctx.bot.db.execute('INSERT INTO TeamWork(user_id,leader,members) VALUES ($1 , $2 , $3 )',user_id,user_id,str(user_id))
        await ctx.bot.db.execute('INSERT INTO team_upgrades(user_id) VALUES ($1)',user_id)
        await ctx.send(embed=await embeding(ctx, '**fuiyohhh**', 'You made an account!', 'green'))
        await server_join.send(embed=await embeding(ctx,'yay',f'{user} made an account!','green'))

@bot.command()
async def support(ctx):
    await ctx.send('https://discord.gg/w6raVrN7CB')

@bot.command()
async def invite(ctx):
    await ctx.send('https://top.gg/bot/983003280852545606')


@bot.command()
async def join(ctx,Member:discord.Member):
    user = ctx.author.id
    leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',Member.id)
    author_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
    author_member=await ctx.bot.db.fetch('SELECT members FROM teamwork WHERE user_id = $1',author_info[0]['leader'])
    accept =Button(label = "Accept" , style = discord.ButtonStyle.green)
    decline=Button(label = "Decline" , style = discord.ButtonStyle.red)  
    member_exist = await ctx.bot.db.fetch('SELECT user_id FROM teamwork WHERE user_id = $1', Member.id)    
    leader_members = leader_info[0]['members']    
    async def accept_callback(interaction):
        leader_members = leader_info[0]['members']
        if interaction.user != Member:
            return 
        leader_members = (leader_members+","+str(user))
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2',None,      user)
        await ctx.bot.db.execute('UPDATE teamwork SET leader  = $1 WHERE user_id = $2',Member.id, user)
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2',leader_members , Member.id)
        await msg.edit(embed=await embeding(ctx, '**Lessgooo**',f"{ctx.author} has join **{leader_info[0]['teamname']}**","green"),view=None)    
        
    async def decline_callback(interaction):
        if interaction.user == Member:
            await msg.edit(embed=await embeding(ctx,'**oop**',f'{Member} has declined the request :<','red'),view=None)    

    accept.callback = accept_callback
    decline.callback = decline_callback
    view = View()
    view.add_item(accept)
    view.add_item(decline)
    if await checking(ctx, ctx.author.id) == False: pass
    elif len(await stringtolist(author_members[0]['members']))>1: await ctx.send(embed = await embeding(ctx, '**uhhh**', f"Leave your current team first!", 'red'))
    elif member_exist == []:                                 await ctx.send(embed = await embeding(ctx, '**uhhh**', f"{Member} doesn't have an account!", 'red'))
    elif Member == ctx.author or Member == bot.user:         await ctx.send(embed = await embeding(ctx, '**uhhh**', 'You cannot join yourself or a bot! >_<', 'red'))
    elif leader_info[0]['leader'] != Member.id :             await ctx.send(embed = await embeding(ctx,'**uhhh**',f"{Member} isn't a leader!",'red'))
    elif leader_info[0]['maxmember'] >= len(leader_members): await ctx.send(embed = await embeding(ctx,'**uhhh**',f"{Member} doesn't have any more member slots!"))
    else:
        msg = await ctx.send(embed = await embeding(ctx, '**Join Request**',f'Hey {Member.mention} , {ctx.author} wants to join your team!', 'green'),view=view)
        try:
            button = await bot.wait_for('interaction',timeout = 20)
        except asyncio.TimeoutError:
            await msg.edit(embed=await embeding(ctx,'**uhhh**',f"{Member} didn't reply on time!",'red'),view=None)

@bot.command()
async def recruit(ctx,Member:discord.Member):
    user = ctx.author.id
    author_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
    member_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', Member.id)
    member_exist = await ctx.bot.db.fetch('SELECT user_id FROM teamwork WHERE user_id = $1', Member.id)   
    accept =Button(label = "Accept" , style = discord.ButtonStyle.green)
    decline=Button(label = "Decline" , style = discord.ButtonStyle.red)
    currentmembers = author_info[0]['members']
    member_members= await ctx.bot.db.fetch('SELECT members FROM teamwork WHERE user_id = $1', member_info[0]['leader'])
    newmember = await listtostring(author_info[0]['members'])
    newmember = (newmember+','+str(Member.id))

    async def accept_callback(interaction):
        if interaction.user != Member:
            return
        if member_info[0]['leader'] == Member.id:
            await memberchange(ctx,member_info[0]['members'])
        else:
            leader = member_info[0]['leader']

        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2', str(newmember),user)
        await ctx.bot.db.execute('UPDATE teamwork SET leader = $1 WHERE user_id = $2', user , Member.id)
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2', None , Member.id)
        await msg.edit(embed=await embeding(ctx, '**Lessgooo**',f"{Member} has join **{author_info[0]['teamname']}**","green"),view=None)

    async def decline_callback(interaction):
        if interaction.user != Member:
            return
        await msg.edit(embed=await embeding(ctx,'**oop**',f'{Member} has declined the request :<','red'),view=None)
    
    accept.callback = accept_callback
    decline.callback = decline_callback
    view = View()
    view.add_item(accept)
    view.add_item(decline)

    membercount = len(await stringtolist(currentmembers))

    if await checking(ctx, user) == False:                   pass
    elif Member == ctx.author or Member.bot:                 await ctx.send(embed=await embeding(ctx,'**uhhh**', "You can't recruit yourself or a bot >_<",'red'))
    elif member_exist == []:                                 await ctx.send(embed=await embeding(ctx,'**uhhh**', f"{Member.mention} doesn't have an account!", "red"))
    elif len(await stringtolist(member_members[0]['members']))>1: await ctx.send(embed = await embeding(ctx, '**uhhh**', f"Tell {Member} to leave their current team first!", 'red'))
    elif author_info[0]['leader'] != ctx.author.id:          await ctx.send(embed=await embeding(ctx,'**uhhh**', f'You are not the leader! Tell the owner to recruit {Member}', 'red'))
    elif str(Member) in currentmembers:                      await ctx.send(embed=await embeding(ctx,'**uhhh**',  'You already recruited that person, you might wanna get check for dementia', 'red'))
    elif membercount >= author_info[0]['maxmember']:         await ctx.send(embed=await embeding(ctx,'**uhhh**',  'You have the max amount of members!', 'red'))
    else:
        msg = await ctx.send(embed=await embeding(ctx, '**Recruit Request**', f'Hey {Member.mention}, **{ctx.author}** wants to recruit you to their team!', 'random'),view=view)
        try:
            button = await bot.wait_for('interaction',timeout = 20)
        except asyncio.TimeoutError:
            await msg.edit(embed=await embeding(ctx,'**uhhh**',f"{Member} didn't reply on time!",'red'),view=None)

async def memberchange(ctx,listt):
    i = 0
    listt = list(listt)
    if len(listt) == 1:
        return
    for x in listt:
        user = listt[i]

        await ctx.bot.db.execute('UPDATE teamwork SET role = $1 WHERE user_id = $2', None , int(user))
        await ctx.bot.db.execute('UPDATE teamwork SET leader = $1 WHERE user_id = $2',int(listt[0]),int(user))
        i += 1

@bot.command()
async def shop(ctx,typee='upgrades'):
    user = ctx.author.id
    user_role = await ctx.bot.db.fetch('SELECT role FROM teamwork WHERE user_id = $1' , user)
    leader = await ctx.bot.db.fetch('SELECT leader FROM teamwork WHERE user_id = $1', user)
    money = await ctx.bot.db.fetch('SELECT balance FROM teamwork WHERE user_id = $1', leader[0]['leader'])
    i = 0
    upgrades = await ctx.bot.db.fetch('SELECT upgrades FROM roles WHERE role = $1', user_role[0]['role'])
    upgrades = await stringtolist(upgrades[0]['upgrades'])

    if typee == 'company':
        companybed = discord.Embed(title='**᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Company Shop᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆**',description='You buy companies here!',color = discord.Color.random())
        
        for x in companies:
            company = companies[i]
            company_info = await ctx.bot.db.fetch('SELECT * FROM company WHERE company = $1', company)
            if company_info[0]['price'] == 0:
                price = 'Free'
            else:
                price = f"{company_info[0]['price']}$"
            companybed.add_field(name=f"**{company_info[0]['companyy']}-__{price}__**",value=f"*{company_info[0]['motto']}*\nRequires *{company_info[0]['maxmember']}* members",inline= False)
            i += 1
        companybed.set_footer(text=f'Use {prefix}startup to buy a company!')
        await ctx.send(embed=companybed)
   
    elif typee == 'upgrades' or typee == 'upgrade':

        if await checking(ctx,user) == False: pass
        elif user_role[0]['role'] == None or user_role[0]['role'] == 'none' or user_role[0]['role'] == [] : await ctx.send(embed=await embeding(ctx,'**uhhh**','You need to be in a company!','red'))
        else:
            upgradebed = discord.Embed(title = f'**᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Upgrades Shop᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆**',description=f"💰**{money[0]['balance']}$**",color= discord.Color.random())
            upgrades = await ctx.bot.db.fetch('SELECT upgrades FROM roles WHERE role = $1', user_role[0]['role'])
            upgrades = await stringtolist(upgrades[0]['upgrades'])
            for x in upgrades:
                role_info = await ctx.bot.db.fetch('SELECT * FROM roles WHERE role = $1',user_role[0]['role'])
                item = upgrades[i]
                item_info = await ctx.bot.db.fetch('SELECT * FROM item WHERE item_id = $1', item)   
                emoji = item_info[0]['emoji']             
                upgradebed.add_field(name=f"**{emoji}{item_info[0]['item_id'].capitalize()}-__{item_info[0]['price']}__${emoji}**",value=f"{item_info[0]['description']}\nBuy ID:`{item_info[0]['item_id']}`", inline = False)
                i += 1
            await ctx.send(embed=upgradebed)

@bot.command()
async def leave(ctx):
    user_id = ctx.author.id
    author_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_id)
    leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', author_info[0]['leader'])
    teamname = await ctx.bot.db.fetch('SELECT teamname FROM teamwork WHERE user_id = $1',(author_info[0]['leader']))
    view = View(timeout=10)
    yes = Button(label='Yes',style = discord.ButtonStyle.green)
    cancle = Button(label='Cancle',style = discord.ButtonStyle.gray)
    view.add_item(yes)
    view.add_item(cancle)
    async def yes_callback(interaction):
        if interaction.user != ctx.author:
            return
        newmember = await stringtolist(leader_info[0]['members'])
        await memberchange(ctx,newmember)
        newmember.remove(str(ctx.author.id)) 
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2', None , user_id)
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2', await listtostring(newmember) , leader_info[0]['user_id'])
        await msg.edit(embed=await embeding(ctx, '**Goodbye**',f"You left **{teamname[0]['teamname']}**", 'green'), view=None)
    
    async def cancle_callback(interaction):
        if interaction.user != ctx.author:
            return        
        await msg.edit(embed=await embeding(ctx, '**Cancelled**', 'You cancelled your leave!', 'green'), view = None)
    yes.callback = yes_callback
    cancle.callback = cancle_callback
    
    if await checking(ctx, user_id) == False:  pass
    elif leader_info[0]['members'] == user_id: await ctx.send(embed = await embeding(ctx, '**uhhh**', 'Which team do you think you leavin? you alone!', 'red'))
    elif author_info[0]['leader'] == user_id:  await ctx.send(embed = await embeding(ctx, '**uhhh**', 'Transfer Ownership to one of your members first!', 'red'))
    else:
        msg = await ctx.send(embed=await embeding(ctx, '**You sure bout that?**', f"Are you sure that you want to leave **{teamname[0]['teamname']}**", 'orange'),view=view)
        try:
            button = await bot.wait_for('interaction',timeout = 20)
        except asyncio.TimeoutError:
            await msg.edit(embed=await embeding(ctx,'**uhhh**',"You didn't reply on time!",'red'),view=None)


    view.add_item(yes)
    view.add_item(cancle)

@bot.command()
async def kick(ctx,Member:discord.Member):
    user = ctx.author.id
    user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
    member_info= await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', Member.id)
    confirm =Button(label = "Confirm" , style = discord.ButtonStyle.green)
    cancel =Button(label = "Cancel" , style = discord.ButtonStyle.grey) 
    members = await stringtolist(user_info[0]['members'])
    view = View()

    async def confirm_callback(interaction):
        nonlocal members
        if interaction.user != ctx.author:
            return
        await memberchange(ctx,members)
        members.remove(str(Member.id))
        members = await listtostring(members)
        await ctx.bot.db.execute('UPDATE teamwork SET leader = $1 WHERE user_id = $2', Member.id , Member.id)
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2', members , int(ctx.author.id))
        await msg.edit(embed = await embeding(ctx,'**Get outta here**',f'You kicked {Member}!','green'),view=None)
    
    async def cancel_callback(interaction):
        if interaction.user != ctx.author:
            return
        await msg.edit(embed=await embeding(ctx,f'**{Member} got spared**','Succesfully cancelled','green'),view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback

    view.add_item(confirm)
    view.add_item(cancel)

    if await checking(ctx, ctx.author.id) == False: pass
    elif str(Member.id)not in members:                       await ctx.send(embed = await embeding(ctx, '**uhhh**', f"{Member} isn't on your team!", 'red'))
    elif Member == ctx.author or Member == bot.user:         await ctx.send(embed = await embeding(ctx, '**uhhh**', 'You cannot kick yourself or a bot! >_<', 'red'))
    elif user_info[0]['leader'] != user :                    await ctx.send(embed = await embeding(ctx,'**uhhh**',"You aren't a leader!",'red'))
    else:
        msg = await ctx.send(embed=await embeding(ctx, '**You sure bout that?**', f"Are you sure that you want to kick **{Member}**", 'orange'),view=view)
        try:
            button = await bot.wait_for('interaction',timeout = 20)
        except asyncio.TimeoutError:
            await msg.edit(embed=await embeding(ctx,'**uhhh**',"You didn't reply on time!",'red'),view=None)
          
@bot.command()
async def transferownership(ctx,Member:discord.Member):
    user = ctx.author.id
    user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user)
    members = await stringtolist(user_info[0]['members'])
    i = 0


    if await checking(ctx,user) == False: pass
    elif str(Member.id) not in members: await ctx.send(embed=await embeding(ctx,'**Uhhh**',f"{Member} Isn't on your team!",'red'))
    elif user != user_info[0]['leader']: await ctx.send(embed=await embeding(ctx,'**Uhhh**',"You aren't the leader!",'red'))
    elif Member.id == user: await ctx.send(embed=await embeding(ctx,'**Uhhh**',"You are already the owner!",'red'))
    else:
        for x in members:
            await ctx.bot.db.execute('UPDATE teamwork SET leader = $1 WHERE user_id = $2',Member.id,int(members[i]))
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2',user_info[0]['members'],Member.id)
        await ctx.bot.db.execute('UPDATE teamwork SET members = $1 WHERE user_id = $2',None,user)
        await ctx.send(embed=await embeding(ctx,'**Lessgoo**','Successfully transfered ownership!','green'))

@bot.command()
async def team(ctx,Member:discord.Member=None):
    user = Member or ctx.author
    leader = await ctx.bot.db.fetch('SELECT leader FROM teamwork WHERE user_id = $1', user.id)
    team_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', leader[0]['leader'])
    team_upgrade = await ctx.bot.db.fetch('SELECT * FROM team_upgrades WHERE user_id = $1', leader[0]['leader'])
    company_info = await ctx.bot.db.fetch('SELECT * FROM company WHERE company = $1',team_info[0]['company'])
    upgrades = ['income','discount']
    members = await stringtolist(team_info[0]['members'])
    company_emoji = {'restaurant':'🍽','farming':'🌱','streetband':'🎸'}
    i = 0
    ii = 0
    upgradesV = []

    if await checking(ctx,user.id) == False: return



    membersV = set()
    if team_info[0]['company'] == None or team_info[0]['company'] == 'none': 
        company = ''
        company_icon = ('https://cdn.discordapp.com/attachments/987626752031457332/990155830701752370/blobs.jpg')
    else: 
        company = (f"{company_emoji[team_info[0]['company']]} {team_info[0]['company'].upper()}")
        company_icon = company_info[0]['company_icon']
    
    embed = discord.Embed(title = team_info[0]['teamname'] , color = discord.Color.random())
    embed.add_field(name = '᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Stats᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆', value = f"💵**{team_info[0]['balance']}$**  Money\n👤**{len(members)}** Members\n💎**{team_info[0]['gem']}** Gems\n{company}",inline=False)
    for x in upgrades:
        if team_upgrade[0][upgrades[i]] != 0:
            upgradesV.append(f'**{team_upgrade[0][upgrades[i]]}%** {upgrades[i]}')
        i += 1
    if upgradesV != []:
     '\n'.join(upgradesV)
     embed.add_field(name='᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Team Upgrades᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',value = upgradesV[0])
    for x in members:
        member_ = members[ii]
        user = await bot.fetch_user(member_)
        role = await ctx.bot.db.fetch('SELECT role FROM teamwork WHERE user_id = $1', int(member_))
        await ctx.send(role[0]['role'])
        if {role[0]['role']} == None or {role[0]['role']} == 'none':
            memberrole = ''
        else:
            memberrole = f"-{role[0]['role']}"
        user_ = await bot.fetch_user(member_)
        memberV_ = (f'**{user_}**{memberrole}')
        membersV.add(memberV_)
        ii += 1
    
    if membersV != None:
        ' \n '.join(membersV)
        membersV = str(membersV)
        membersV= membersV.replace('{','')
        membersV= membersV.replace('}','')
        membersV= membersV.replace(',','\n')
        membersV=membersV.replace("'",'')    
        embed.add_field(name='᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Members᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',value = membersV , inline = False)
    embed.set_thumbnail(url=company_icon)
    leader = leader[0]['leader']
    user = await bot.fetch_user(leader)
    embed.set_footer(text=f"Owned by {await bot.fetch_user(leader)}",icon_url=user.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def rename(ctx):
    user_id = ctx.author.id
    user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id= $1', user_id) 
   
    
    if await checking(ctx, user_id) == False: pass
    elif user_info[0]['leader'] != user_id: await ctx.send(embed= await embeding(ctx, '**uhhh**', "You aren't the leader!", 'red'))
    else:
        await ctx.send(embed = await embeding(ctx, None, 'What will be your team name?', 'random'))
        try:
            msg = await bot.wait_for('message',timeout = 20 , check=lambda message: message.author == ctx.author)  
            
            if len(msg.content) > 15: 
                await ctx.send(embed = await embeding(ctx, '**uhhh**', 'Keep message lower than 15!', 'red'))        
                return
            
            await ctx.bot.db.execute('UPDATE teamwork SET teamname = $1 WHERE user_id = $2', msg.content,user_id)
            await ctx.send(embed= await embeding(ctx,"**lessgoo**",f"Your team name is now **{msg.content}**",'green'))
        except asyncio.TimeoutError:
            await ctx.send(embed=await embeding(ctx,'**uhhh**',"You didn't reply on time!",'red'))

@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx):
    guild = ctx.message.guild.id
    currentpref = await ctx.bot.db.fetch('SELECT prefix FROM server_prefix WHERE guilds_id = $1', guild)

    await ctx.send(embed = await embeding(ctx, None, 'What will be your prefix?', 'random'))
    try:
        msg = await bot.wait_for('message',timeout = 20 , check=lambda message: message.author == ctx.author)  
        if len(msg.content) > 15: 
            await ctx.send(embed = embeding(ctx, '**uhhh**', 'Keep message lower than 15!', 'red'))        
            return 
        
        if currentpref == []:
            await ctx.bot.db.execute('INSERT INTO server_prefix (guilds_id,prefix) VALUES ($1,$2)', guild,msg.content)
        else:
            await ctx.bot.db.execute('UPDATE server_prefix SET prefix = $1 WHERE guilds_id = $2',msg.content,guild)
        await ctx.send(embed= await embeding(ctx,"**lessgoo**",f"Your prefix is now `{msg.content}` !",'green'))
    
    except asyncio.TimeoutError:
            await ctx.send(embed=await embeding(ctx,'**uhhh**',"You didn't reply on time!",'red'))  

@bot.command()
async def startup(ctx,company):
    company = company.lower()
    user_info= await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',ctx.author.id)
    company_info = await ctx.bot.db.fetch('SELECT * FROM company WHERE company = $1', company)
    companies=['restaurant','farming','streetband']
    company_role = await ctx.bot.db.fetch(f'SELECT company_role FROM company WHERE company = $1',company)
    company_role= company_role[0]['role']
    roles = await stringtolist(company_role)
    members = await stringtolist(user_info[0]['members'])
    rolecount= len(roles)
    membercount =len(members)
    membercount = len(await stringtolist(user_info[0]['members']))
    i=0
    if await checking(ctx,ctx.author.id) == False: pass
    elif ctx.author.id != user_info[0]['leader']: await ctx.send(embed=await embeding(ctx,'**uhhh**',"You aren't the leader!",'red'))
    elif company not in companies: await ctx.send(embed=await embeding(ctx,'**uhhh**','What company is that:skull:?','red'))
    elif user_info[0]['balance'] < company_info[0]['price']: await ctx.send(embed=await embeding(ctx,'**uhhh**',"You don't have enough money!",'red'))
    elif membercount != company_info[0]['maxmember']: await ctx.send(embed=await embeding(ctx,'**uhhh**',f"You need **{company_info[0]['maxmember']}** members for this company!",'red'))
    else:
        spent = abs(company_info[0]['price']-user_info[0]['balance'])
        for x in members:
            await ctx.bot.db.execute('UPDATE teamwork SET role= $1 WHERE user_id= $2',roles[i],int(members[i]))
            i += 1

        await ctx.bot.db.execute('UPDATE teamwork SET balance= $1 WHERE user_id= $2',spent,ctx.author.id)
        await ctx.bot.db.execute('UPDATE teamwork SET company= $1 WHERE user_id= $2',company,ctx.author.id)
        await ctx.send(embed=await embeding(ctx,'**Lessgoo**',f"You now have a **{company_info[0]['companyy']}** company!",'green'))

@bot.command()
async def buy(ctx,*,item):
    item.lower()   
    user = ctx.author.id
    user_info=  await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
    leader=     await ctx.bot.db.fetch('SELECT leader FROM teamwork WHERE user_id = $1', user)
    leader=     leader[0]['leader']
    leader_inv= await ctx.bot.db.fetch('SELECT * FROM stats WHERE user_id = $1',leader)
    leader_info=await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',leader)
    balance=    leader_info[0]['balance']
    role_info=  await ctx.bot.db.fetch('SELECT * FROM roles WHERE role = $1', user_info[0]['role'] )
    
    upgrades=   await ctx.bot.db.fetch('SELECT upgrades FROM roles WHERE role = $1',user_info[0]['role'])
    upgrades=   await stringtolist(upgrades[0]['upgrades'])
    
    items=      await ctx.bot.db.fetch('SELECT item_id FROM item WHERE type = $1','item')
    items=      await recordtolist(items,'item_id')
    
    multipliers=await ctx.bot.db.fetch('SELECT item_id FROM item WHERE type= $1','multiplier')
    multipliers= await recordtolist(multipliers,'item_id')

    item_info = await ctx.bot.db.fetch('SELECT * FROM item WHERE item_id = $1', item)

    if await checking(ctx,user) == False : pass
    elif item not in items and item not in upgrades and item not in multipliers: await ctx.send(embed= await embeding(ctx,'**uhhh**',"What item is that? :skull:",'red'))
    elif item_info[0]['price'] > balance: await ctx.send(embed=await embeding(ctx,'**uhhh**',"You're too broke!😹",'red'))
    else:
        inventory = leader_inv[0]['inventory']
        balance = balance - item_info[0]['price']
        if inventory == None or inventory == 'None':
           newinventory = (item)
        else:
            newinventory = (f'{inventory},{item}')        
        
        if item_info[0]['type'] == 'multiplier': 
            if item not in upgrades: 
                await ctx.send(embed=await embeding(ctx,'**uhhh**',"You can't buy this item!",'red'))
                return
            else:
                if inventory != None and item in inventory:
                    await ctx.send(embed=await embeding(ctx,'**uhhh**','You already have this item!','red'))      
                    return         
                else:    
                    await ctx.bot.db.execute('UPDATE teamwork SET multiplier = $1 WHERE user_id = $2', leader_info[0]['multiplier'] + 1 , leader)
        await ctx.bot.db.execute('UPDATE stats SET inventory = $1 WHERE user_id = $2', newinventory,leader)
        await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2', balance , leader) 
        await ctx.send(embed=await embeding(ctx,'**Fuiyohhh**',f"You bought **{item_info[0]['item'].capitalize()}**{item_info[0]['emoji']}!",'green')) 

@bot.command()
async def ping(ctx):
    await ctx.send(embed=await embeding(ctx,'**🏓Pong!**','*{0}Milliseconds*'.format(round(bot.latency, 1)),'random'))
@bot.command()
async def fetch(ctx,column,db,whereplace,typee,wherevalue):
    if typee == 'int': wherevalue = int(wherevalue)
    info = await ctx.bot.db.fetch(f'SELECT {column} FROM {db} WHERE {whereplace} = $1',wherevalue)
    await ctx.send(info[0][column])

@bot.command()
async def say(ctx,*,msg):
    msg.lower()
    await ctx.send(msg)

@bot.command() 
async def leaderboard(ctx):
    msg = await ctx.send('Loading message..<a:loading:1002540830994735165> ')
    tops = await ctx.bot.db.fetch('SELECT teamname , balance , user_id, leader FROM teamwork ORDER BY balance DESC NULLS LAST')
    top = {}
    for i in tops:
        top[i[0]] = i[0]
   
    embed = discord.Embed(
        title = ('**Richest Teams**'),
        colour = discord.Colour.random(),)
    visible_index = 1
    index = 0
    for i in top:
        if tops[index]['user_id'] != tops[index]['leader']:
            pass
        else:
            leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',tops[index]['leader'])
            embed.add_field(name =f" **{visible_index}.** {tops[index]['teamname']} ({await bot.fetch_user(tops[index]['user_id'])})" , value = f"Money: *{tops[index]['balance']}$* \n Members: *{len(await stringtolist(leader_info[0]['members']))}*" , inline = False )
            if visible_index == 10:
                embed.set_footer(text= 'can u get on top?')
                await msg.edit('',embed = embed)
                break
            else:
                visible_index += 1
            
        index += 1

@bot.command()
async def inventory(ctx,Member:discord.Member=None):
    user = Member or ctx.author
    user_leader = await ctx.bot.db.fetch('SELECT leader FROM teamwork WHERE user_id = $1',user.id)
    user_inventory = await ctx.bot.db.fetch('SELECT inventory FROM stats WHERE user_id = $1',user.id)
    if await checking(ctx,user.id) == False: return
    else:
        inventory = '**Nothing In Inventory**'
        if user_inventory[0]['inventory'] == []:
            await ctx.send('[]')
        else:
            i = 0
            user_inventory = await stringtolist(user_inventory[0]['inventory'])
            items = list(dict.fromkeys(user_inventory))
            for x in items:
                item = items[i]
                count = user_inventory.count(item)
                if inventory == '**Nothing In Inventory**':
                    inventory = f"**x{count} {await item_info(ctx,'item',item)}{await item_info(ctx,'emoji',item)}**"
                else:
                    inventory = await stringtolist(inventory)
                    inventory.append(f"**x{count} {await item_info(ctx,'item',item)}{await item_info(ctx,'emoji',item)}**")
                i += 1
            inventory = await listtostring2(inventory)
            inventory = inventory.replace(',','\n')
            inventorybed= discord.Embed(title= '᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Inventory᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',description=inventory,colour=discord.Color.random())
            await ctx.send(embed=inventorybed)

@bot.command()
async def help(ctx):
    view = View()
    generalbed = discord.Embed(title='᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Help᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',description='`<>` = Required | `[]` = Optional',colour = discord.Color.random())
    generalbed.add_field(name='__Get Started__',value='*`{0}new \n{0}rename\n{0}startup <company>`*'.format(prefix),inline=True)
    generalbed.add_field(name='__Team Management__',value='*`{0}join <user>\n{0}recruit <user>\n{0}kick <user>\n{0}leave`*'.format(prefix),inline=True)
    generalbed.add_field(name="\u200b",value="\u200b",inline=False)
    generalbed.add_field(name='__Information__',value='*`{0}team [user]\n{0}inventory [user]\n{0}shop company/upgrade\n{0}leaderboard`*'.format(prefix),inline=True)
    generalbed.add_field(name='__Extra Economy__',value='*`{0}beg\n{0}gamble <amount>\n{0}guess <amount>`*'.format(prefix),inline=True)
    generalbed.add_field(name="\u200b",value="\u200b",inline=False)
    generalbed.add_field(name='__Settings__',value='*`{0}help\n{0}support\n{0}invite\n{0}changeprefix`*'.format(prefix),inline=True)
   
    select = Select(
        placeholder='See different commands',
        options=[
            discord.SelectOption(
                label='Company commands',
                emoji="📃"),
            discord.SelectOption(
                label='General commands',
                emoji="🏷")
        ])

  
    async def select_callback(interaction):
        if select.values[0] == 'Company commands': 
            companybed = discord.Embed(title='᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Help᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',description='Required = `<>` | Optional = `[]`',colour = discord.Color.random())
            companybed.add_field(name='__Farming🌱__',value='*`{0}plant\n{0}harvest\n{0}sell <plant>`*'.format(prefix),inline=False)
            companybed.add_field(name='__StreetBand🎸__',value='*`{0}play\n{0}sing`*'.format(prefix),inline=False)
            companybed.add_field(name='__Restaurant🍕__',value='*`{0}cook\n{0}serve\n{0}promote`*'.format(prefix),inline=False)
            await msg.edit(embed=companybed)
        elif select.values[0] == 'General commands':
            await msg.edit(embed=generalbed)

    select.callback = select_callback
    view.add_item(select)
    
    msg = await ctx.send(embed=generalbed,view=view) 



'''@bot.event
async def on_message(message):
    prefix = '.'
    if bot.user.mentioned_in(message):
        await message.channel.send(embed=await embeding(message,'Hello!',"My prefix is `{0}`\nType `{0}help` for more info".format(prefix),'random'))'''

@recruit.error
async def recruit_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','Who are you recruiting?','red')
    embed.add_field(name='Example:',value=f'`{prefix}recruit @obama`')
    await ctx.send(embed=embed)

@join.error
async def join_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','Who are you joining?','red')
    embed.add_field(name='Example:',value=f'`{prefix}join @EDP445`')
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','Who are you kicking?','red')
    embed.add_field(name='Example:',value=f'`{prefix}kick @Kanye`')
    await ctx.send(embed=embed)        

@transferownership.error
async def transferownership_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','Who are you transffering ownership to?','red')
    embed.add_field(name='Example:',value=f'`{prefix}transferownership @Pewdipie`')
    await ctx.send(embed=embed)

@startup.error
async def startup_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','Which company are you starting?','red')
    embed.add_field(name='Example:',value=f'`{prefix}startup farming`')
    embed.set_footer(text=f'Use {prefix}shop company to see the companies!')
    await ctx.send(embed=embed)

@buy.error
async def buy_error(ctx,error):
    embed= await embeding(ctx,'**Uhhh**','What are you buying?','red')
    embed.add_field(name='Example:',value=f'`{prefix}buy mcqueen shoes`')
    await ctx.send(embed=embed)




asyncio.run(main())

