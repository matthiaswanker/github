import discord
import os
import time
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check


client = commands.Bot(command_prefix="<")

import asyncio

from datetime import datetime



@client.command(description="Retrieves info about the current server and sends it back as an embed message.")
async def serverinfo(ctx):
    server = ctx.guild
    numVoiceChannels = len(server.voice_channels)
    numTextChannels = len(server.text_channels)
    numChannels = numVoiceChannels + numTextChannels

    roles = list(server.roles)
    roles = reversed(roles)
    rolesString = ""
    for role in roles:
        rolesString += f"{role.name}, " 

    emojis = server.emojis
    emojiString = ""
    for emoji in emojis:
        emojiString += str(emoji)

    timeNow = datetime.utcnow()
    serverAge = timeNow - server.created_at
    serverAgeInS = serverAge.total_seconds()
    serverAgeYears = divmod(serverAgeInS, 31536000)
    serverAgeDays = divmod(serverAgeYears[1], 86400)
    serverAgeHours = divmod(serverAgeDays[1], 3600)
    serverAgeMinutes = divmod(serverAgeHours[1], 60)
    serverAgeString = f"({int(serverAgeYears[0])} years, {int(serverAgeDays[0])} days, {int(serverAgeHours[0])} hours, {int(serverAgeMinutes[0])} minutes ago)"
    
    embed=discord.Embed(title="SERVER INFO", description="Here is the info I could retrieve for this server: ", color=0x000000)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="NAME:", value=server.name, inline=True)
    embed.add_field(name="ID:", value=server.id, inline=True)
    embed.add_field(name="OWNER:", value=f"{server.owner}", inline=True)
    embed.add_field(name="REGION:", value=server.region, inline=True)
    embed.add_field(name="MEMBERS:", value=server.member_count, inline=True)
    embed.add_field(name="MEMBERS BOOSTING:", value=server.premium_subscription_count, inline=True)
    embed.add_field(name="ROLES:", value=rolesString[:-2], inline=False)
    embed.add_field(name="SERVER CHANNELS:", value=f"{numChannels} channels ({numTextChannels} text, {numVoiceChannels} voice)", inline=False)
    await ctx.send(embed=embed)
    if len(emojis) > 0:
        await ctx.send("**Server Custom Emojis:**\n" + emojiString)
    else:
        await ctx.send("**Server Custom Emojis:**\nNo custom emojis.")

@client.event
async def on_ready():
    
    await client.change_presence(activity=discord.Streaming(name='Sea of Thieves', url='https://www.twitch.tv/toxicohcr'))
    
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# error
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(embed=discord.Embed(
		    description=f' {ctx.author.name}, could not found command ',
		    color=1127128))

@client.command(name='dm',pass_context=True)

async def dm(ctx, *argument):
    #creating invite link
    invitelink = await ctx.channel.create_invite(max_uses=1,unique=True)
    #dming it to the person
    await ctx.author.send(invitelink)
# convert



class Slapper(commands.Converter):
	async def convert(self, ctx, argument):
		to_slap = random.choice(ctx.guild.members)
		return '{0.author} slapped {1} because *{2}*'.format(
		    ctx, to_slap, argument)
@client.command()
async def userinfo(ctx, *, user: discord.User = None): 
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)


@client.event
async def on_ready():
    global startdate
    startdate = datetime.now()

@client.command(help = "Prints details of Server")
async def i_am(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)
    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))




# tells_secret

@client.command()
async def secret(ctx):
    secret = 'how are you'
    response = "❗how are you❗\n||{}|| im toxico".format(secret)
    await ctx.send(response)
# cat_pics
import requests
@client.command()
async def catto(ctx):
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    
    cat_embed = discord.Embed()
    cat_embed.set_image(url=f"{r[0]['url']}")
    
    await ctx.send(embed=cat_embed)

@client.command()
async def dog(ctx):
    r = requests.get("https://api.thedogapi.com/v1/images/search").json()
    
    cat_embed = discord.Embed()
    cat_embed.set_image(url=f"{r[0]['url']}")
    
    await ctx.send(embed=cat_embed)



@client.command()
@commands.is_owner()
async def rules(ctx):
    await ctx.channel.purge(limit=1)
    embed=discord.Embed(color=0xBDB5D5)
    embed.set_thumbnail(url="https://cdn.tixte.com/uploads/hi.has.rocks/kp471cuah9a.jpg")
    embed.add_field(name="👋 Welcoem to toxico server !", value="Welcome to the official ** TOXICO ** Discord server! We are happy to welcome you and hope you have a good time interacting with all the other players in the community. Before interacting with other players, we ask that you ** read our rules carefully ** so that you fully understand what you will be held responsible for.", inline=False)
    embed.add_field(name="✉️ Private Masseges", value="Contact  <@577898008822415370> For infos about the bot and many other dont write to the bot he will not be  write back in private. Dont spam in the servers this bot in the future will be like an automod if spam it will be kick him", inline=False)
    embed.add_field(name="")
    await ctx.send(embed=embed)

@client.command()
async def verify(ctx):
    helpembed=discord.Embed(title="Verification", url="https://www.discord.com", description="You have been verified!", color=discord.Color.blue())
    await ctx.author.send(embed=helpembed)






@client.command()
async def rules_1(ctx):
  await("Welcome to the official ** Toxico ** Discord server! We are happy to welcome you and hope you have a good time interacting with all the other players in the community. Before interacting with other players, we ask that you ** read our rules carefully ** so that you fully understand what you will be held responsible for")

@client.command()
async def rules_2(ctx):
  await ctx.send("Welcome to the official ** MINEAOT ** Discord server! We are happy to welcome you and hope you have a good time interacting with all the other players in the community. Before interacting with other players, we ask that you ** read our rules carefully ** so that you fully understand what you will be held responsible for")
# textblocks
@client.command()
async def multi_quote(ctx, *args):
    one_word_per_line = '\n'.join(args)
    quote_text = 'You said:\n>>> {}'.format(one_word_per_line)
    await ctx.send(quote_text)


@client.command()
async def block_quote(ctx, *, arg):
    quote_text = 'You said:\n> {}'.format(arg)
    await ctx.send(quote_text)

# say
@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response), await ctx.message.delete()


# owner_server
@client.command()
@commands.is_owner()
async def list_guilds(ctx):
	servers = client.guilds
	for guild in servers:
		embed = discord.Embed(colour=0x7289DA)
		embed.set_footer(text=f"Guilds requested by {ctx.author}",
		                 icon_url=ctx.author.avatar_url)
		embed.add_field(name=(str(guild.name)),
		                value=str(guild.member_count) + " members",
		                inline=False)
		await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def list_guild(ctx):
	servers = client.guilds
	description_info = ""

	for guild in servers:
		description_info += "**" + str(guild.name) + "**\n" + str(
		    guild.member_count
		) + " members\n\n"  # This will loop through each guild the bot is in and it the name and member count to a variable that holds everything

	embed = discord.Embed(
	    description=description_info, colour=0x7289DA
	)  # Edit the embed line to include the description we created above
	embed.set_footer(text=f"Guilds requested by {ctx.author}",
	                 icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)


import random



import typing

# bottle
@client.command()
async def bottles(ctx, amount: typing.Optional[int] = 99, *, liquid="beer"):
	await ctx.send('{} bottles of {} on the wall!'.format(amount, liquid))


from discord import Member

# avatar
@client.command()
async def getpfp(ctx, member: Member = None):
	if not member:
		member = ctx.author
	await ctx.send(member.avatar_url)

# avatar
@client.command()
@commands.guild_only()
async def avatar(self, ctx, *, user: discord.Member = None):
	""" Get the avatar of you or someone else """
	user = user or ctx.author
	await ctx.send(
	    f"Avatar to **{user.name}**\n{user.avatar_url_as(size=1024)}")


class MemberRoles(commands.MemberConverter):
	async def convert(self, ctx, argument):
		member = await super().convert(ctx, argument)
		return [role.name
		        for role in member.roles[1:]]  # Remove everyone role!

#role
@client.command()
async def roles(ctx, *, member: MemberRoles):
	"""Tells you a member's roles."""
	await ctx.send('I see the following roles: ' + ', '.join(member))


import typing

# ban
@client.command()
async def ban(ctx,
              members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0,
              *,
              reason: str):
	"""Mass bans members with an optional delete_days parameter"""
	for member in members:
		await member.ban(delete_message_days=delete_days, reason=reason)


import typing



	
@client.command()
async def poll(ctx, msg, duration):
  embed=discord.Embed()
  embed.title=msg
  embed.description="React for fun."
  embed.set_footer(text="👑 Toxico bot")
  embed.color=0x00ffff
  msg = await ctx.send(embed=embed)
  await msg.add_reaction('🎉')
  await msg.add_reaction('😃')
  await msg.add_reaction('🏴')
  await msg.add_reaction('😁')
  await msg.add_reaction('🌐')
  await msg.add_reaction('<a:emoji_52:794534864892198983>')
  await ctx.send("react lol")
  

emoji = client.get_emoji(794534864892198983)
  

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server')
        break

# delete
@client.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, amount=None):
	await ctx.channel.purge(limit=int(amount))
	await ctx.channel.send('deleted some massages')
	
	
	

    


# ping
@client.command()
async def ping(ctx):
	await ctx.send(
	    "pong!"
	)  

@client.command()
async def servers(ctx):
    await ctx.send(f"{str(client.guilds)}")

@client.command()
@commands.is_owner()
async def join_voice(self, ctx):
    channel = ctx.author.voice.channel
    print(channel.id)
    await self.client.VoiceChannel.connect()
	

client.run(
    "secret token"
)
