# SOE-ProgAlap2-Beadando-Szotar
Ujvari Vera

A program egy angol értelmező szótárat és QUIZ-t mutat be.

# Dictionary 
A szótárat ilyen szerkezetű json fájlból lehet inicializálni:

``` 
{
    "easel": "a wooden frame to hold a picture while it is being painted",
    "ink": "coloured liquid for writing, drawing and printing",
    "apple": "a round fruit with shiny red or green skin that is fairly hard and white inside"
}
```

Egy szó beírása után a ``` SEARCH ```gombbal kereshetünk rá annak jelentésére.
Egy véletlenszerűen kiválasztott szóra is rákereshetünk a ``` RANDOM ``` segítségével. 
Ha olyan szóra keresünk rá, ami nem található meg a szótárban, azt a program jelzi.
A szótárban nem csak rákeresni lehet szavakra, hanem hozzáadni új szó-definíció párost is
az ``` ADD ``` gomb lenyomásával. Ha a beírt szó már létezik a szótárban, Exceptiont kapunk,
amit a programunkban is olvashatunk, nem csak a konzolon.
Létezik egy ``` UPDATE DEFINITION``` gomb is, amivel egy már létező szó definícióját tudjuk átírni,
de új szót ez a gomb nem enged hozzáadni a szótárhoz. 



# QUIZ
A QUIZ egy új ablakban jelenik meg, a szótár ``` LET'S TAKE A QUIZ ```  gomb megnyomása után. 

A QUIZ véletlenszerűen kiválaszt egy szót a szótárból, majd 4 definíciót kínál, de csak egy helyes.
Radiobuttonok segítségével jelölhetjük meg a szerintünk jó megfejtést.
Ha eltaláljuk a helyes megoldást, akkor kapunk 1 pontot, más esetben nem.
A ``` NEXT ``` gomb lenyomása után újabb kérdés és válaszlehetőségeket kapunk, mindez addig megy,
míg nem nyomunk rá az ``` EXIT THE QUIZ ```nyomra. Ezután egy messageboxban kapunk tájékoztatást,
hogy a feltett kérdések-jó válaszok arányában hány százalékot értünk el.
Feltett kérdések száma annyi, ahányszor rányomtunk a NEXT gombra, mielőtt kiléptünk az EXIT-tel.
A ``` RESET ``` opcióval lenullázhatjuk az addig elért pontszámunkat, ha nem szép
az eredményünk, illetve ekkor a kérdések számlálója is újra indul.


# Plot
A szótárnak van egy olyan gombja, hogy ``` PROBABILITY OF OCCURRENCE ```, ami megmutatja a QUIZ befejezése után,
hogy egyes szavak hányszor lettek megkérdezve egy kör alatt.
Ha a QUIZ kitöltés előtt szeretnénk rányomni, akkor nem fogunk tudni rákattintani. 







