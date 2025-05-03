# Tulostinlauta

## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään itselleen profiilikuvan, sekä kuvauksen.
* Käyttäjä näkee itsensä, sekä muiden profiilin luomispäivän.
* Käyttäjä pystyy lisäämään sovellukseen tulostinarvosteluja.
* Käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään tietokohteita.
* Käyttäjä pystyy valitsemaan tulostimelle yhden tai useamman luokittelun.
* Käyttäjä näkee sovellukseen lisätyt tulostimet.
* Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien tulostimiin liittyen.
* Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
* Käyttäjä pystyy etsimään tulostimia nimillä, merkeillä, julkaisuvuosilla, sekä luokilla
* Käyttäjä näkee muiden käyttäjäsivut, jossa näkyy myös heidän julkaisunsa.

## Sovelluksen asennus
Asenna `flask`-kirjasto:
```
$ pip install flask
```
Luo tietokannan taulut ja indeksit, sekä lisää alkutiedot:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
Sovelluksen voi käynnistää komennolla:
```
$ flask run
```

## Toiminta suurella tietomäärällä
Testataksesi sivun toimintaa suurella tietomäärällä suorita `seed.py` scripti. Muuttamalla muuttujien `user_count`, `post_count` ja `comment_count` arvoja voit muokata luotavan testidatan suuruutta.

Sovellusta on testattu 1000 käyttäjällä, 10<sup>5</sup> julkaisulla ja 10<sup>6</sup> kommentilla. Tällöin sivu latautui välittömästi, julkaisun saa avattua välittömästi, käyttäjän profiilin saa avattua välittömästi, sekä suppea haku palauttaa tuloksen väittömästi. Laajaasti, kuten esimerkiksi yhtä kirjainta haettaessa sivun lataus voi kestää.
