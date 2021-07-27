import os
import re
import discord
import urllib.request
import bs4 as bs
import time
import asyncio
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Variables globales
myServer = ''
status = ''
channelName = ''
selectedChannel=None

# Serveurs en dur pour le moment
lstServers = ["Antillia","Atlantis","Baltia","Bionorr","Eridu","Finias","Gaecrimund","Gemini","Indus","Kay","Klomm","Lacerta","Maski","Muspelheim","Niraya US","Nysa","Olympus","Penglai","Perseus","Riax","Roruva","Sanghata","Sanjiva","Suddene","Tapana","Themiscyra","Thule","Uvici","Vieladon","Xanadu","Xeovir","Yama","Andromeda","Annwyn","Arupa","Aseira","Asgard","Biringan","Cibola","Cosmos","Creonn","Crush","Diyu","Duzakh","Fae","Glougnor","Hades","Ife","Inferni","Irkalla","Istedol","Kamaloka","Kamma","Kasanaan","Kitezh","Kvenland","Laestrygon","Lane","Lemuria","Lyonesse","Manasic","Naraka","Nav","Pavo","Peta","Plaeth","Raedur","Sculptor","Slaekk","Tirach","Yeuval","Yomi","Zerzura","Adiri","Aquila","Bolaris","Celoan","Chaeus","Feostri","Ivinet","Joustral","Leuthorr","Machina","Mu","Niraya SA","Nostralanar","Olthigon","Orion","Paradiso","Qaessa","Shangri-La","Tamag","Ursa","Vaikuntha","Wealdis","Xeasiq","Aquarius","Centaur","Corvus","Dromgoole","Ephelyn","Lyra","Samavasarana","Scorpius","Tuma","Arali","Aukumea","Barzakh","Breran","Burotu","Ekera","El Dorado","Fieryth","Heaxil","Hyperborea","Iketho","Kur","Maharova","Murias","Ocadalon","Pangaia","Pleroma"]

# Instanciation du bot
bot = commands.Bot(command_prefix="$")

# Tâche de fond
async def background_task():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await call_web()
        await asyncio.sleep(30)

# Appel de la page web
async def call_web():
    global status

    if selectedChannel:
        page = urllib.request.urlopen('https://www.newworld.com/fr-fr/support/server-status')
        soup = bs.BeautifulSoup(page, 'html.parser')

        allDivs = soup.findAll('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server'})

        # Pour chaque serveur
        for row in allDivs:
            if myServer in row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-name'}).text:
                if row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-status--down'}):
                    if status != False:
                        await selectedChannel.send('Le serveur \'' + myServer + '\' n\'est pas accessible')
                        status=False
                elif row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-status--up'}):
                    if status != True:
                        await selectedChannel.send('Le serveur \'' + myServer + '\' est accessible')
                        status=True
                else:
                    await selectedChannel.send('Impossible d\'obtenir le statut du serveur')

# Commande du choix du canal du bot
@bot.command()
async def channel(ctx, arg=None):
    global channelName
    global selectedChannel

    if arg is None:
        await ctx.send('Merci de spécifier le nom du canal de discussion pour le bot')
    else:
        selectedChannel = discord.utils.get(ctx.guild.channels, name=arg)

        if selectedChannel:
            channelName = arg
            await selectedChannel.send('Le canal a bien été choisi')
        else:
            await ctx.send('Le canal choisi n\'a pas été trouvé, vérifiez son orthographe')

# Commande du choix du serveur New World
@bot.command()
async def server(ctx, arg=None):
    global myServer
    
    if arg is None:
        await ctx.send('Merci de spécifier le nom du serveur en paramètre')
    else:
        if arg in lstServers:
            myServer = arg
            await ctx.send('Le serveur a bien été remplacé par \'' + arg + '\'')
            await call_web()
        else:
            await ctx.send('Le serveur spécifié doit faire parti de la liste des serveurs actuels')

# Lancement du bot
bot.loop.create_task(background_task())
bot.run(TOKEN)
