import json
import pathlib

import discord
import requests
import toml

SKRIPTPFAD = pathlib.Path(__file__).parent
CONFIGPFAD = SKRIPTPFAD / "config.toml"
CONFIG = toml.load(CONFIGPFAD)
DEBUG = CONFIG["debug"]

client = discord.Client()


def set_target_language(emoji):
    if emoji == "🇬🇧":  # UK-Englisch
        target_anguage = "en-GB"
    elif emoji == "🇺🇲":  # US-Englisch
        target_anguage = "en-US"
    elif emoji == "🇩🇪":  # Deutsch
        target_anguage = "de"
    elif emoji == "🇷🇺":  # Russisch
        target_anguage = "ru"
    else:
        return
    return target_anguage


@client.event
async def on_reaction_add(reaction, _):  # (reation, user)
    if DEBUG:
        print(reaction.emoji)

    target_language = set_target_language(str(reaction.emoji))
    if target_language is None:
        # Kein Emoji zur Übersetzung gewählt
        return

    data = {
        "auth_key": CONFIG["deepl_api_key"],
        "text": reaction.message.content,
        "target_lang": target_language
    }
    r = requests.post(CONFIG["deepl_url"], data)

    if DEBUG:
        print(r)
        print(r.text)

    await reaction.message.reply(json.loads(r.text)["translations"][0]["text"])


client.run(CONFIG["dc_token"])
