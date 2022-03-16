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
    """
    Liste verfügbarer Sprachen
    https://www.deepl.com/de/docs-api/translating-text/request/
    """

    if emoji == "🇧🇬":
        target_language = "bg"  # bulgarisch
    elif emoji == "🇨🇿":
        target_language = "cs"  # tschechisch
    elif emoji == "🇩🇰":
        target_language = "da"  # dänisch
    elif emoji == "🇩🇪":
        target_language = "de"  # deutsch
    elif emoji == "🇬🇧":
        target_language = "en-GB"  # uk-englisch
    elif emoji == "🇺🇲":
        target_language = "en-US"  # us-englisch
    elif emoji == "🇪🇸":
        target_language = "es"  # spanisch
    elif emoji == "🇪🇪":
        target_language = "et"  # estnisch
    elif emoji == "🇫🇮":
        target_language = "fi"  # finnisch
    elif emoji == "🇫🇷":
        target_language = "fr"  # französisch
    elif emoji == "🇭🇺":
        target_language = "hu"  # ungarisch
    elif emoji == "🇮🇹":
        target_language = "it"  # italienisch
    elif emoji == "🇯🇵":
        target_language = "ja"  # japanisch
    elif emoji == "🇱🇹":
        target_language = "lt"  # litaunisch
    elif emoji == "🇱🇻":
        target_language = "lv"  # lettisch
    elif emoji == "🇳🇱":
        target_language = "nl"  # niederländisch
    elif emoji == "🇵🇱":
        target_language = "pl"  # polnisch
    elif emoji == "🇵🇹":
        target_language = "pt"  # portogisisch
    elif emoji == "🇷🇴":
        target_language = "ro"  # rumänisch
    elif emoji == "🇷🇺":
        target_language = "ru"  # russisch
    elif emoji == "🇸🇰":
        target_language = "sk"  # slovakisch
    elif emoji == "🇸🇮":
        target_language = "sl"  # slovenisch
    elif emoji == "🇸🇪":
        target_language = "sv"  # schwedisch
    elif emoji == "🇨🇳":
        target_language = "zh"  # chinesisch
    else:
        return
    return target_language


@client.event
async def on_reaction_add(reaction, _):  # (reation, user)
    if DEBUG:
        print(reaction.emoji)

    target_language = set_target_language(str(reaction.emoji))
    if target_language is None:
        # Kein Emoji welches eine übersetzbare Länderflagge ist gewählt
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
