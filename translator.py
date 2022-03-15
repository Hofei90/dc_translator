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
    https://www.deepl.com/de/docs-api/translating-text/request/
    "BG" - Bulgarian - 🇧🇬
    "CS" - Czech - 🇨🇿
    "DA" - Danish - 🇩🇰
    "DE" - German - 🇩🇪
    "EL" - Greek - 🇬🇷
    "EN" - English - 🇬🇧 - 🇺🇲
    "ES" - Spanish - 🇪🇸
    "ET" - Estonian - 🇪🇪
    "FI" - Finnish - 🇫🇮
    "FR" - French - 🇫🇷
    "HU" - Hungarian - 🇭🇺
    "IT" - Italian - 🇮🇹
    "JA" - Japanese - 🇯🇵
    "LT" - Lithuanian - 🇱🇹
    "LV" - Latvian - 🇱🇻
    "NL" - Dutch - 🇳🇱
    "PL" - Polish - 🇵🇱
    "PT" - Portuguese - 🇵🇹
    "RO" - Romanian - 🇷🇴
    "RU" - Russian - 🇷🇺
    "SK" - Slovak - 🇸🇰
    "SL" - Slovenian - 🇸🇮
    "SV" - Swedish - 🇸🇪
    "ZH" - Chinese - 🇨🇳
    """

    if emoji == "🇬🇧":  # UK-Englisch
        target_language = "en-GB"
    elif emoji == "🇺🇲":  # US-Englisch
        target_language = "en-US"
    elif emoji == "🇩🇪":  # Deutsch
        target_language = "de"
    elif emoji == "🇷🇺":  # Russisch
        target_language = "ru"
    elif emoji == "🇵🇱":  # Polnisch
        target_language = "pl"
    else:
        return
    return target_language


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
