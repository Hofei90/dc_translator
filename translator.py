import pathlib

import deepl
import discord
import toml


SKRIPTPFAD = pathlib.Path(__file__).parent
CONFIGPFAD = SKRIPTPFAD / "config.toml"
CONFIG = toml.load(CONFIGPFAD)
DEBUG = CONFIG["debug"]

WORK_CHANNEL_NAME = "anmeldung"


if CONFIG["welcome_message"]:
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
else:
    client = discord.Client()


translator = deepl.Translator(CONFIG["deepl_api_key"])


def search_work_channel(work_channel_name):
    channels = client.get_all_channels()
    work_channel = None
    for channel in channels:
        if str(channel) == work_channel_name:
            work_channel = client.get_channel(channel.id)
            break
    return work_channel


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

    result = translator.translate_text(reaction.message.content, target_lang=target_language)

    if DEBUG:
        print(result)

    await reaction.message.reply(result.text)


if CONFIG["welcome_message"]:
    @client.event
    async def on_member_join(member):
        work_channel = search_work_channel(WORK_CHANNEL_NAME)
        if work_channel is not None:
            await work_channel.send(f"{CONFIG['welcome_message_text']}")


client.run(CONFIG["dc_token"])
