# Dc_Translator

Ein Discordbot, der den Text einer Nachricht in die ausgewählte Sprache übersetzt, indem man als Reaktion 
die Länderflagge der gewünschten Sprache sendet.

## Vorbereitungen

### Api-Key DeepL

Zunächst muss ein Konto auf [DeepL](https://www.deepl.com) erstellt werden um einen **API-Key** zu erhalten. In der 
kostenlosen Version sind 500000 Zeichen pro Monat zur Übersetzung verfügbar.

### Discord Bot erstellen

Bitte einer Anleitung im Internet folgen, darauf achten dass notwendige Rechte beim erstellen gesetzt sind, aber dem
Bot auch nicht mehr Rechte (Administrator z.B) als nötig geben und den Bot dem gewünschten Server hinzufügen.

### Installation + Konfiguration

Die folgende Anleitung als auch die Service Unit geht davon aus, dass das Projekt in das Homeverzeichnis des Users *pi*
liegt.

```code
git clone https://github.com/Hofei90/dc_translator.git
cd /home/pi/dc_translator
cp config_vorlage.toml config.toml
nano config.toml
```

In der Konfigurationsdatei nun die nötigen Eingaben tätigen, alles mit <> muss ausgefüllt werden. Stehen außerhalb der
Klammern Anfürungszeichen, so müssen diese erhalten bleiben!

`dc_token = "<discordtoken>"` Token des Discordbots eintragen
`deepl_api_key = "<deepl_api_token>"` API-Key von DeepL

Sind print() Ausgaben gewünscht, so kann der Eintrag `debug` von `false` auf `true` gestellt werden.

Anschließend ein erster manueller Test mit `python3 translator.py` starten.
Funktioniert alles wie gewünscht so kann der Autostart mit Hilfe der Service Unit eingerichtet werden.

```
sudo mv dc_translator.service /etc/systemd/system/dc_translator.service
sudo systemctl start dc_translator.service
sudo systemctl enable dc_translator.service
```
