import discord, random, aiohttp, requests
from discord.ext import commands

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Game'))
    print("Client is ready and running!")


@client.command(aliases=['hey', 'hi'])
async def hello(ctx):
    greet = f"Hello {ctx.author.mention}"
    await ctx.send(greet)


@client.command(aliases=['latency', 'ping'])
async def internet(ctx):
    latency = str(round(client.latency*1000, 2)) + " ms"
    await ctx.reply(latency)


@client.command(aliases=['8ball', 'psych'])
async def eightball(ctx, *, question):
    responses = ['yes', 'no', 'maybe']
    reply = f"Question: {question} \nResponse: {random.choice(responses)}"
    await ctx.reply(reply)


@client.command(aliases=['stockprice', 'share'])
async def stock(ctx, *, ticker):
    api_key = <YOUR_API_KEY>

    price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker.upper()}&interval=5min&apikey={api_key}'

    overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker.upper()}&interval=5min&apikey={api_key}'

    news_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={ticker.upper()}&interval=5min&apikey={api_key}'

    price_response = requests.get(price_url)
    overview_response = requests.get(overview_url)
    news_response = requests.get(news_url)

    price_data = price_response.json()
    overview_data = overview_response.json()
    news_data = news_response.json()

    symbol = overview_data['Symbol']
    company = f"{overview_data['Name']} ({symbol})"
    exchange = overview_data['Exchange']
    industry = overview_data['Industry']

    title = news_data['feed'][random.randint(0, 20)]['title']
    author = news_data['feed'][random.randint(0, 20)]['authors'][0]
    sentiment = news_data['feed'][random.randint(0, 20)]['overall_sentiment_label']

    latest_data = price_data['Time Series (5min)']
    latest_timestamp = list(latest_data.keys())[0]
    latest_price = latest_data[latest_timestamp]['1. open']  # Element 2

    embed = discord.Embed(title=latest_price, colour=discord.Colour.random(), description=industry.capitalize())

    embed.set_author(name=company)
    embed.set_footer(text=exchange)

    embed.add_field(name=title, value=author)
    embed.add_field(name="Sentiment", value=sentiment, inline=True)

    await ctx.send(embed=embed)


@client.command()
async def pic(ctx, *, query):
    async with aiohttp.ClientSession() as cd:
        async with cd.get(f"https://www.reddit.com/r/{query}.json") as r:
            dogs = await r.json()
            embed = discord.Embed(title=dogs['data']['children'][random.randint(0, 26)]['data']['title'], colour=discord.Colour.random())
            embed.set_image(url=dogs['data']['children'][random.randint(0, 26)]['data']['url'])

            await ctx.send(embed=embed)


client.run('<YOUR_BOT_TOKEN>')
