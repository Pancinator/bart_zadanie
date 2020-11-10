## Vypracované zadanie na back-end
##### Pár poznámok k riešeniu:
  1. K vypracovaniu som použil Django a Django REST Framework.
  2. Vrámci vypracovania boli vytvorené dva modely (tabuľky) a to Image a Gallery, relačný vzťah medzi týmito tabuľkami je
     Many-To-Many.
  3. Model Gallery reprezentuje galériu, kde sú uložené referencie na jednotlivé obrázky, slúži ako zoznam obrázkov. Image model          predstavuje jednotlivé obrázky, slúži na udržiavanie referencií na obrázky uložené v priečinku ***media***.
  3. K simulovaniu metód POST a DELETE som využil program ***Postman*** a jeho desktopového agenta.   
  4. Náhľadový obrázok je prispôsobený do výslednej veľkosti pomocou metódy ***thumbnail*** a odoslaný vo forme Httpresponse typu          image/jpeg.
 
##### Pokus o zvládnutie bonusovej úlohy:
  1. Pokusil som o získane access tokenu tak ako bolo popísané vo facebook doku, avšak narazil som na chybovú hlášku o nevalídnosti        client_secret, aj keď som response_type nastavil na token tak ako to bolo popísané v zadaní. Implementáciu som preto nedokončil.
  2. Použitý request: https://graph.facebook.com/v8.0/oauth/access_token?client_id=1053174974861205&redirect_uri=https%3A%2F%2Flocalhost%2Ftoken&response_type=token

##### Štruktúra repozitára:
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
