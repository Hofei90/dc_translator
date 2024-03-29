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


def replace_notification_char(text):
    return text.replace("@", "")


def set_target_language(emoji):
    """
    List of available languages
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
    elif emoji == "🇬🇷":  # griechisch
        target_language = "el"
    elif emoji == "🇬🇧":
        target_language = "en-GB"  # uk-englisch
    elif emoji == "🇺🇲":
        target_language = "en-US"  # us-englisch
    elif emoji == "🇪🇸" or emoji == "🇪🇦":
        target_language = "es"  # spanisch
    elif emoji == "🇪🇪":
        target_language = "et"  # estnisch
    elif emoji == "🇫🇮":
        target_language = "fi"  # finnisch
    elif emoji == "🇫🇷":
        target_language = "fr"  # französisch
    elif emoji == "🇭🇺":
        target_language = "hu"  # ungarisch
    elif emoji == "🇮🇩":  # indonesisch
        target_language = "id"
    elif emoji == "🇮🇹":
        target_language = "it"  # italienisch
    elif emoji == "🇯🇵":
        target_language = "ja"  # japanisch
    elif emoji == "🇰🇷":  # koreanisch
        target_language = "ko"
    elif emoji == "🇱🇹":
        target_language = "lt"  # litaunisch
    elif emoji == "🇱🇻":
        target_language = "lv"  # lettisch
    elif emoji == "🇳🇴":  # norwegisch
        target_language = "nb"
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
    elif emoji == "🇹🇷":  # türkisch
        target_language = "tr"
    elif emoji == "🇺🇦":  # ukrainisch
        target_language = "uk"
    elif emoji == "🇨🇳":
        target_language = "zh"  # chinesisch
    else:
        return
    return target_language


@client.event
async def on_raw_reaction_add(raw_reaction_action_event):
    if DEBUG:
        print(raw_reaction_action_event.emoji)

    channel = client.get_channel(raw_reaction_action_event.channel_id)
    message = await channel.fetch_message(raw_reaction_action_event.message_id)
    target_language = set_target_language(str(raw_reaction_action_event.emoji))
    if target_language is None:
        # No emoji which is a translatable country flag chosen
        return

    result = translator.translate_text(message.content, target_lang=target_language)

    if DEBUG:
        print(result)

    text_without_notification = replace_notification_char(result.text)
    await message.reply(text_without_notification)


if CONFIG["welcome_message"]:
    @client.event
    async def on_member_join(member):
        work_channel = search_work_channel(WORK_CHANNEL_NAME)
        if work_channel is not None:
            await work_channel.send(f"{CONFIG['welcome_message_text']}")


client.run(CONFIG["dc_token"])
