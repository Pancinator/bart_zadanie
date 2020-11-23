## Vypracované zadanie na back-end
#### Zmeny uskutočnené po poslednej oprave:
  1. Drvivá väčšina chybných testov bola bohužial spôsobená kvôli nešťastnemu resp. zlému enkódovaniu/dekódovaniu do/z ACII            formatu čo spôsobilo následne zlé ukladanie v adresárovom systéme, tento problem sa vyriešil robustnejším spôsobom a to            využívaním urllib knižnice.
  2. Problém s nutnosťou prítomnosti "trailing slash" na konci URL requestov tak isto by mal byť vyriešený, automatizované testy        teda už nemusia byť upravené.
  3. Bol pridaný jendoduchý serializér na kontorlu validnosti JSON requestu na vytvorenie galérie. 
  4. Endpoint GET /images/{w}x{h}/{path} si už viac nevyžaduje celú cestu k obrázku. 

#### Pár poznámok k riešeniu:
  1. K vypracovaniu som použil Django a Django REST Framework riešenie je prerobené tak aby fungovalo bez použitia databázy.
  2. K ukladaniu do adresárovej štruktúry som použil FileSystemStorage modul.
  3. K simulovaniu metód POST a DELETE som využil program ***Postman*** a jeho desktopového agenta.   
  4. Náhľadový obrázok je prispôsobený do výslednej veľkosti pomocou metódy ***thumbnail*** a odoslaný vo forme Httpresponse typu          image/jpeg.
  5. Uploadovaný obrázok je ukládaný podľa nasledujúcej schémy: media/<gallery_name>/<image_name>
  6. Nie je povolených viacero obrázkov s rovnakým menom v jednej galérií
  
    
#### Návod na inštaláciu a spustenie django servera:
Navod bol vytváraný pre platformu Windows (Python version 3.8):

  1. clone git repo do ľubovoľného priečinka
  2. Vytvorte nový virtual environment a to nasledovne: "yourfolder"\bart_zadanie\bart>python -m venv .\venv
  3. aktivujte virtuálny environment: venv\Scripts\activate
  3. nainštalujte potrebné balíčky: python -m pip install -r requirements.txt 
  4. change directory: cd gallery_showroom
  5. vykonajte migrácie: python manage.py makemigrations
  6. migrujte: python manage.py migrate
  7. spustite server: python manage.py runserver
  8. API overview je dostupné v prehliadači na adrese http://127.0.0.1:8000/api/
  
  
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
        - serializers.py
        - tests.py
        - urls.py
        - views.py
      - media (folder)
      - manage.py
