# Dc_Translator

Ein Discordbot, der den Text einer Nachricht in die ausgewählte Sprache übersetzt, indem man als Reaktion 
die Länderflagge der gewünschten Sprache sendet.

## Vorbereitungen

### Benötigte Software
Python 3.8 oder höher 


### Api-Key DeepL

Zunächst muss ein Konto auf [DeepL](https://www.deepl.com) erstellt werden, um einen **API-Key** zu erhalten. In der 
kostenlosen Version sind 500000 Zeichen pro Monat zur Übersetzung verfügbar.

### Discord Bot erstellen

Bitte einer Anleitung im Internet folgen und dabei darauf achten, dass die notwendige Rechte beim Erstellen gesetzt 
werden, jedoch dem Bot auch nicht mehr Rechte (z.B. Administrator) als nötig geben 
und anschließend den Bot dem gewünschten Server hinzufügen.

### Installation + Konfiguration

Die folgende Anleitung und die vorliegende Service Unit gehen davon aus, dass das Projekt in 
dem Homeverzeichnis des Users *pi* liegt. Bei Abweichungen müssen die Pfade angepasst werden.

```code
git clone https://github.com/Hofei90/dc_translator.git
cd /home/pi/dc_translator
pip3 install --user -r requirements.txt
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
