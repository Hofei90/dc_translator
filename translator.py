import toml
import discord
import pathlib
import requests
import json


SKRIPTPFAD = pathlib.Path(__file__).parent
CONFIGPFAD = SKRIPTPFAD / "config.toml"
CONFIG = toml.load(CONFIGPFAD)


client = discord.Client()


@client.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    if str(reaction.emoji) == "🇬🇧":  # UK-Englisch
        lang = "en-GB"
    elif str(reaction.emoji) == "🇺🇲":  # US-Englisch
        lang = "en-US"
    elif str(reaction.emoji) == "🇩🇪":  # Deutsch
        lang = "de"
    elif str(reaction.emoji) == "🇷🇺":  # Russisch
        lang = "ru"

    # elif str(reaction.emoji) == "🇺🇦":  # Ukrainisch wohl nicht unterstützt

    else:
        return
    data = {
        "auth_key": CONFIG["deepl"],
        "text": reaction.message.content,
        "target_lang": lang
    }
    r = requests.post(CONFIG["url"], data)
    # print(r)
    # print(r.text)
    await reaction.message.reply(json.loads(r.text)["translations"][0]["text"])


client.run(CONFIG["token"])
