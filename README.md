# tulostinlauta
Tämänhetkiset ominaisuudet:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen tulostinarvosteluja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään tietokohteita.
* Käyttäjä näkee sovellukseen lisätyt tulostimet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät tulostimet.
* Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
* Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien tulostimiin liittyen.
* Käyttäjä pystyy etsimään tulostimia nimillä, merkeillä, julkaisuvuosilla
* Käyttäjä pystyy valitsemaan tulostimelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät tulostimet.

## Toiminta suurella tietomäärällä.
Testataksesi sivun toimintaa suurella tietomäärällä suorita `seed.py` scripti. Muuttamalla muuttujien `user_count`, `post_count` ja `comment_count` arvoja voit muokata luotavan testidatan suuruutta.

Sovellusta on testattu 1000 käyttäjällä, 10<sup>5</sup> julkaisulla ja 10<sup>6</sup> kommentilla. Tällöin sivu latautui välittömästi, julkaisun saa avattua välittömästi, käyttäjän profiilin saa avattua välittömästi, sekä suppea haku palauttaa tuloksen väittömästi. Laajaasti, kuten esimerkiksi yhtä kirjainta haettaessa sivun lataus voi kestää.
