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

# Globals variables
myServer = ''
status = ''
channelName = ''
selectedChannel = None

# Translations variables
TranslationAvailableServer = ''
TranslationUnavailableServer = ''
TranslationStatusUnavailable = ''
TranslationUnspecifiedChannelName = ''
TranslationChannelChoiceConfirmation = ''
TranslationUnableToFindChannel = ''
TranslationUnspecifiedServerName = ''
TranslationServerChoiceConfirmation = ''
TranslationServerNotInTheList = ''
TranslationUnspecifiedLanguage = ''
TranslationLanguageNotInTheList = ''
TranslationLanguageChoiceConfirmation = ''

# Readonly variables
lstServers = ["Antillia","Atlantis","Baltia","Bionorr","Eridu","Finias","Gaecrimund","Gemini","Indus","Kay","Klomm","Lacerta","Maski","Muspelheim","Niraya US","Nysa","Olympus","Penglai","Perseus","Riax","Roruva","Sanghata","Sanjiva","Suddene","Tapana","Themiscyra","Thule","Uvici","Vieladon","Xanadu","Xeovir","Yama","Andromeda","Annwyn","Arupa","Aseira","Asgard","Biringan","Cibola","Cosmos","Creonn","Crush","Diyu","Duzakh","Fae","Glougnor","Hades","Ife","Inferni","Irkalla","Istedol","Kamaloka","Kamma","Kasanaan","Kitezh","Kvenland","Laestrygon","Lane","Lemuria","Lyonesse","Manasic","Naraka","Nav","Pavo","Peta","Plaeth","Raedur","Sculptor","Slaekk","Tirach","Yeuval","Yomi","Zerzura","Adiri","Aquila","Bolaris","Celoan","Chaeus","Feostri","Ivinet","Joustral","Leuthorr","Machina","Mu","Niraya SA","Nostralanar","Olthigon","Orion","Paradiso","Qaessa","Shangri-La","Tamag","Ursa","Vaikuntha","Wealdis","Xeasiq","Aquarius","Centaur","Corvus","Dromgoole","Ephelyn","Lyra","Samavasarana","Scorpius","Tuma","Arali","Aukumea","Barzakh","Breran","Burotu","Ekera","El Dorado","Fieryth","Heaxil","Hyperborea","Iketho","Kur","Maharova","Murias","Ocadalon","Pangaia","Pleroma"]
lstLangs = ['EN', 'FR']

# Bot instanciation
bot = commands.Bot(command_prefix="$")

# French translations
def setLanguage(langToSet):
    global TranslationAvailableServer, TranslationUnavailableServer, TranslationStatusUnavailable, TranslationUnspecifiedChannelName, TranslationChannelChoiceConfirmation, TranslationUnableToFindChannel, TranslationUnspecifiedServerName, TranslationServerChoiceConfirmation, TranslationServerNotInTheList, TranslationUnspecifiedLanguage, TranslationLanguageNotInTheList, TranslationLanguageChoiceConfirmation
        
    if langToSet == 'FR':
        TranslationUnavailableServer = 'Le serveur \'{}\' n\'est pas accessible'
        TranslationAvailableServer = 'Le serveur \'{}\' est accessible'
        TranslationStatusUnavailable = 'Impossible d\'obtenir le statut du serveur'
        TranslationUnspecifiedChannelName = 'Merci de spécifier le nom du canal de discussion pour le bot'
        TranslationChannelChoiceConfirmation = 'Le canal a bien été modifié'
        TranslationUnableToFindChannel = 'Le canal spécifié n\'a pas été trouvé'
        TranslationUnspecifiedServerName = 'Merci de spécifier le nom du serveur en paramètre'
        TranslationServerChoiceConfirmation = 'Le serveur a bien été remplacé par \'{}\''
        TranslationServerNotInTheList = 'Le serveur spécifié doit appartenir de la liste des serveurs disponibles'
        TranslationUnspecifiedLanguage = 'Merci de spécifier la langue souhaitée'
        TranslationLanguageNotInTheList = 'Merci de spécifier une langue prise en charge'
        TranslationLanguageChoiceConfirmation = 'La langue a bien été remplacée par {}'
    elif langToSet == 'EN':
        TranslationUnavailableServer = 'The server \'{}\' is unavailable'
        TranslationAvailableServer = 'The serveur \'{}\' is available'
        TranslationStatusUnavailable = 'Unable to find the server status'
        TranslationUnspecifiedChannelName = 'The channel name must be specified'
        TranslationChannelChoiceConfirmation = 'The channel has been selected'
        TranslationUnableToFindChannel = 'The channel cannot be found'
        TranslationUnspecifiedServerName = 'The server name must be specified'
        TranslationServerChoiceConfirmation = 'The server has been replaced by \'{}\''
        TranslationServerNotInTheList = 'The specified server must be in the official server list'
        TranslationUnspecifiedLanguage = 'The language must be specified'
        TranslationLanguageNotInTheList = 'The specified language must be in the available languages list'
        TranslationLanguageChoiceConfirmation = 'The language has been replaced by {}'

# Background task
async def background_task():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await call_web()
        await asyncio.sleep(30)

# Call of the web page
async def call_web():
    global status

    if selectedChannel:
        page = urllib.request.urlopen('https://www.newworld.com/fr-fr/support/server-status')
        soup = bs.BeautifulSoup(page, 'html.parser')

        allDivs = soup.findAll('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server'})

        # For each server
        for row in allDivs:
            if myServer in row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-name'}).text:
                if row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-status--down'}):
                    if status != False:
                        await selectedChannel.send(TranslationUnavailableServer.format(myServer))
                        status=False
                elif row.findChild('div', attrs = {'class' : 'ags-ServerStatus-content-responses-response-server-status--up'}):
                    if status != True:
                        await selectedChannel.send(TranslationAvailableServer.format(myServer))
                        status=True
                else:
                    await selectedChannel.send(TranslationStatusUnavailable)

# Channel choice command
@bot.command()
async def channel(ctx, arg=None):
    global channelName
    global selectedChannel

    if arg is None:
        await ctx.send(TranslationUnspecifiedChannelName)
    else:
        selectedChannel = discord.utils.get(ctx.guild.channels, name=arg)

        if selectedChannel:
            channelName = arg
            await selectedChannel.send(TranslationChannelChoiceConfirmation)
        else:
            await ctx.send(TranslationUnableToFindChannel)

# Language choice command
@bot.command()
async def lang(ctx, arg=None):
    if arg is None:
        await ctx.send(TranslationUnspecifiedLanguage)
    else:
        if arg in lstLangs:
            setLanguage(arg)
                
            await ctx.send(TranslationLanguageChoiceConfirmation.format(arg))
        elif arg == 'list':
            await ctx.send(', '.join(lstLangs))
        else:
            await ctx.send(TranslationLanguageNotInTheList)

# Server choice command
@bot.command()
async def server(ctx, arg=None):
    global myServer
    
    if arg is None:
        await ctx.send(TranslationUnspecifiedServerName)
    else:
        if arg in lstServers:
            myServer = arg
            await ctx.send(TranslationServerChoiceConfirmation.format(arg))
            await call_web()
        elif arg == 'list':
            await ctx.send(', '.join(lstServers))
        else:
            await ctx.send(TranslationServerNotInTheList)

# Configure translation
setLanguage('EN')

# Start bot
bot.loop.create_task(background_task())
bot.run(TOKEN)
