import requests, discord, threading, random, json, tracemalloc, asyncio
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from webserver import keep_alive


tracemalloc.start()

prefix = "!" 

my_secret = os.environ['webhook']
log_webhook = os.environ['webhook']

my_secret = os.environ['token']
token = os.environ['token']

intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=prefix, help_command=None, intents=intents)


@bot.event
async def on_ready():
 members = sum([guild.member_count for guild in bot.guilds])
 await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Aogiri Tree"))
 print("Members")


@bot.command()
async def spfollow(ctx, *, username=None):
    if ctx.channel.type != discord.ChannelType.private:

        if ctx.channel.id != 987525174968590336:
            embed = discord.Embed(color=0x2ac3d4, description=f"<@{ctx.author.id}> Use this command in <#987525174968590336>")
            await ctx.send(embed=embed)
            return

        #Re
        role_id = discord.utils.get(ctx.guild.roles, name="C- Rated Ghoul")
        if role_id not in ctx.author.roles:
            embed = discord.Embed(color=0x2ac3d4, description=f" <@{ctx.author.id}> wrong role")
            await ctx.send(embed=embed)
            return

        webhook = DiscordWebhook(url=log_webhook)
        embed = DiscordEmbed(title='Spotify', description=(f'**{ctx.author} : {bot.command_prefix}spfollow -> {username}**'), color=3066993)
        webhook.add_embed(embed)
        response = webhook.execute()

        print(f' [ * ] @{ctx.author} | ({ctx.author.id}) -> {bot.command_prefix}spfollow ~ ({username})')

        _tokens = []
        for _ in open('./tokens.txt', 'r'):
            _tokens.append(_.rstrip())


        def follow(target):
            for x in range(50):
                try:
                    headers = {
                        "accept": "application/json",
                        "Accept-Encoding": "gzip, deflate, br",
                        "accept-language": "en",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                        "app-platform": "WebPlayer",
                        "Referer": "https://open.spotify.com/",
                        "spotify-app-version": "1.1.52.204.ge43bc405",
                        "authorization": f"Bearer {random.choice(_tokens)}",
                    }

                    try:
                        r = requests.put(f"https://api.spotify.com/v1/me/following?type=user&ids={target}", headers=headers)
                    except Exception as e:
                        print(e)

                except:
                    pass

        embed = discord.Embed(color=0x2ac3d4, description=f"**__*Adding*__** `50` **__*Followers To*__** `{username}`")
        await ctx.send(embed=embed)
        threading.Thread(target=follow, args=(username,)).start()

keep_alive()
bot.run(token)
