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
    Liste verfÃ¼gbarer Sprachen
    https://www.deepl.com/de/docs-api/translating-text/request/
    """

    if emoji == "ð§ð¬":
        target_language = "bg"  # bulgarisch
    elif emoji == "ð¨ð¿":
        target_language = "cs"  # tschechisch
    elif emoji == "ð©ð°":
        target_language = "da"  # dÃ¤nisch
    elif emoji == "ð©ðª":
        target_language = "de"  # deutsch
    elif emoji == "ð¬ð§":
        target_language = "en-GB"  # uk-englisch
    elif emoji == "ðºð²":
        target_language = "en-US"  # us-englisch
    elif emoji == "ðªð¸":
        target_language = "es"  # spanisch
    elif emoji == "ðªðª":
        target_language = "et"  # estnisch
    elif emoji == "ð«ð®":
        target_language = "fi"  # finnisch
    elif emoji == "ð«ð·":
        target_language = "fr"  # franzÃ¶sisch
    elif emoji == "ð­ðº":
        target_language = "hu"  # ungarisch
    elif emoji == "ð®ð¹":
        target_language = "it"  # italienisch
    elif emoji == "ð¯ðµ":
        target_language = "ja"  # japanisch
    elif emoji == "ð±ð¹":
        target_language = "lt"  # litaunisch
    elif emoji == "ð±ð»":
        target_language = "lv"  # lettisch
    elif emoji == "ð³ð±":
        target_language = "nl"  # niederlÃ¤ndisch
    elif emoji == "ðµð±":
        target_language = "pl"  # polnisch
    elif emoji == "ðµð¹":
        target_language = "pt"  # portogisisch
    elif emoji == "ð·ð´":
        target_language = "ro"  # rumÃ¤nisch
    elif emoji == "ð·ðº":
        target_language = "ru"  # russisch
    elif emoji == "ð¸ð°":
        target_language = "sk"  # slovakisch
    elif emoji == "ð¸ð®":
        target_language = "sl"  # slovenisch
    elif emoji == "ð¸ðª":
        target_language = "sv"  # schwedisch
    elif emoji == "ð¨ð³":
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
        # Kein Emoji welches eine Ã¼bersetzbare LÃ¤nderflagge ist gewÃ¤hlt
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
