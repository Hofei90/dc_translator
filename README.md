# Dc_Translator
[Deutsches Readme](https://github.com/Hofei90/dc_translator/blob/master/README_GERMAN.md)

A Discordbot that translates the text of a message into the selected language by sending as response 
sending the country flag of the desired language

## Preparations

### Required software
Python 3.8 or higher 

### Api-Key DeepL

First, you need to create an account on [DeepL](https://www.deepl.com) to get an **API key**. In the 
free version 500000 characters per month are available for translation.

### Create Discord Bot

Please follow the instructions on the Internet and make sure that the necessary rights are set when creating the bot. 
but do not give the bot more rights (e.g. administrator) than necessary. 
and then add the bot to the desired server.

### Installation + Configuration

The following instructions and the present service unit assume that the project is installed in 
the home directory of the user *pi*. In case of deviations the paths have to be adjusted.

```code
git clone https://github.com/Hofei90/dc_translator.git
cd /home/pi/dc_translator
cp config_vorlage.toml config.toml
nano config.toml
```

Now make the necessary entries in the configuration file, everything with <> must be filled in. If there are quotes outside the
brackets, you have to keep them!

`dc_token = "<discordtoken>"` Enter token of the Discordbot
`deepl_api_key = "<deepl_api_token>"` API-Key from DeepL

If print() output is desired, the `debug` entry can be changed from `false` to `true`.

Then start a first manual test with `python3 translator.py`.
If everything works as desired, the autostart can be set up with the help of the service unit.

```
sudo mv dc_translator.service /etc/systemd/system/dc_translator.service
sudo systemctl start dc_translator.service
sudo systemctl enable dc_translator.service
```
