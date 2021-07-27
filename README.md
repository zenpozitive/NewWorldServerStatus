# New World Server Status

## Description

Discord Bot to know the status of New World game servers.
It is based on https://www.newworld.com/fr-fr/support/server-status

## Pull on your server

### Link

https://discord.com/api/oauth2/authorize?client_id=869262316053618748&permissions=2048&scope=bot

### Requirements

You need to have the **manager server role** to use the link.
The bot only need write permission to works (no abuses).

## Commands

### Required ones

When the bot comes to your server, **you have two commands to use if you wants the Bot works properly**, else, nothing will happen.

Select the written channel where the bot will write when the server is up or down
> $channel NameOfTheTchatChannel

*Ex: $channel general*

Select the New World server to check the status (only one is possible for now)
> $server NameOfTheServer

*Ex : $server Yomi*

### Optional ones

Get the server list
> $server list

Get the language list
> $lang list

Change the language (the default one is english (EN)
> $lang MYLANGUAGECODE

*Ex : $lang FR*

## What is does exactly

The bot will write "Server is now available" or "Server is unavailable" when the status changed.
There is no default channel for the bot, so don't forget to use the two commands at the start.

## Other information

That's my first Python development and my first Discord bot. The code is not the most optimized, is not the prettiest one too, but it works as I wanted to.
Be free to do pull requests and I will look at it when I've got time.

## Improvements

✅ Add language choice (with a command) with two languages : french and english
- Have the ability to choose more than one server to watch
- Remove the server list in my code to take it automatically from the status page (that's awful)
