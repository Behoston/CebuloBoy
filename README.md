# Cebulo Boy - bot

Bot służy do pobierania ofert ze sklepów:
 - [al.to](https://al.to)
 - [x-kom](https://x-kom.pl)
 - [morele](https://morele.net)
 - [hard-pc](https://sklep.hard-pc.pl)
 - [komputronik](https://www.komputronik.pl/)
 - [proline](https://proline.pl/)

i wysyłaniu powiadomień na [Telegrama](https://telegram.org/).


## Setup

#### Python
Bot działa na **Pythonie 3.5** i wyżej.

Jak ktoś naprawdę musi to niech sobie sam sportuje do 2,
ale się tym nie chwali.


#### Zależności
Wymagane są dodatkowe biblioteki. Wystarczy zainstalować:

```bash
pip install -r requirements.txt
```

Zauważyłem, że nie wszędzie da się zainstalować tą wersję, której używałem u siebie.
W tym wypadku można próbować użyć pliku bez zamrożonej wersji bibliotek.

```bash
pip install -r requirements.in
```


#### CRON

Aby bot się uruchamiał, należy skopiować plik [cebulobot.cron](./cebulobot.cron)
do katalogu `/etc/cron.d/`.


#### Telegram API

Trzeba skopiować sobie plik konfuguracyjny:
```bash
cp sample_config.py config.py
```
i uzupełnić jego zawartość.

W kodzie trzeba uzupełnić `token` do API Telegrama.
Można go uzyskać od [BotFathera](https://telegram.me/BotFather).

Trzeba też wpsiać id kanału na którym bot ma pisać.
W tym celu trzeba:
1. Dodać bota do kanału.
2. Napisać na kanale cokolwiek (lub napisać do bota bezpośrednio).
3. Wykonać:
   ```bash
   python3 boy.py update
   ```
   żeby pobrać ostatnie wiadomości i eventy, które dostał bot.
4. Odszukać interesujące `chat_id` i wpsiać do kodu bota.

Można to pewnie zautomatyzować, jednak ja nie miałem ani potrzeby,
ani dobrego pomysłu jak to zrealizować
(nazwy kanałów mogą się zmieniać, powiadomień bot może dostawać dużo z różnych miejsc).
