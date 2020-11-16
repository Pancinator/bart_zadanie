## Vypracované zadanie na back-end
##### Pár poznámok k riešeniu:
  1. K vypracovaniu som použil Django a Django REST Framework riešenie je prerobené tak aby fungovalo bez použitia databázy.
  2. K ukladaniu do adresárovej štruktúry som použil FileSystemStorage modul.
  3. K simulovaniu metód POST a DELETE som využil program ***Postman*** a jeho desktopového agenta.   
  4. Náhľadový obrázok je prispôsobený do výslednej veľkosti pomocou metódy ***thumbnail*** a odoslaný vo forme Httpresponse typu          image/jpeg.
  5. Uploadovaný obrázok je ukládaný podľa nasledujúcej schémy: media/<gallery_name>/<image_name>
  6. Nie je povolených viacero obrázkov s rovnakým menom v jednej galérií
  
##### Pokus o zvládnutie bonusovej úlohy:
  1. Pokusil som o získane access tokenu tak ako bolo popísané vo facebook doku, avšak narazil som na chybovú hlášku o nevalídnosti        client_secret, aj keď som response_type nastavil na token tak ako to bolo popísané v zadaní. Implementáciu som preto nedokončil.
  2. Použitý request: https://graph.facebook.com/v8.0/oauth/access_token?client_id=1053174974861205&redirect_uri=https%3A%2F%2Flocalhost%2Ftoken&response_type=token
  3. Skúsil som aj login request (dočítal som sa že je nutný aj login na získanie Code parametru): https://www.facebook.com/dialog/oauth?client_id=1053174974861205&redirect_uri=https%3A%2F%2Flocalhost%2Ftoken&response_type=code. Ale aplikácia nepodporuje logovanie. 

##### Štruktúra repozitára:
Oproti predchádzajúcemu riešeniu niesú využité súbory models.py a serializers.py
  - bart
    - gallery_showroom (django project)
      - gallery_showroom 
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
      - bart_gallery (app)
        - admin.py
        - apps.py
        - models.py
        - ~~serializers.py~~
        - tests.py
        - urls.py
        - views.py
      - media (folder)
      - manage.py
