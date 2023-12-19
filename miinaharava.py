"""Miinaharava Extended Horror Experience!"""

import random
from os import system, name

def tyhjenna_terminaali():
    """Tyhjentää terminaalin käyttöjärjestelmä huomioiden."""
    
    # windows
    if name == "nt":
        _ = system("cls")
    # mac / linux
    else:
        _ = system("clear")

def kysy_koko():
    """Esittelee pelin ja kysyy pelikentän koon.

        Peli on koodattu siten, että pelikentän kokoa ja pommien lukumäärää voi halutessaan vaihtaa helposti,
        ja koko muu peli adaptoituu niiden mukaan.
    """
    
    global n
    global lkm
    
    print("_______")
    print("|     |")
    print("|  D: |")
    print("|_____|")
    print("Pelaat peliä Miinaharava Extended Horror Experience!")
    print()
    print("Pelilaudat: pieni \"p\" / iso \"i\"")
    print()

    while True:
        koko = input("Anna koko: ")
        
        # koko määrittää rivien/sarakkeiden määrän (n) sekä pommien lukumäärän (lkm)
        if koko == "p":
            n = 5
            lkm = 3
            break
        elif koko == "i":
            n = 10
            lkm = 13
            break
        else:
            print("Virheellinen toiminto!")

def alusta_listat_ja_matriisit():
    """Alustaa listat ja matriisit."""
    
    global mat_back
    global mat_front
    global pommit
    global liput
    global nakyvat
    
    # backend-matriisi
    mat_back = [[0 for rivi in range(n)] for sarake in range(n)] 
    # frontend-matriisi
    mat_front = [[" " for rivi in range(n)] for sarake in range(n)]
    # pommien koordinaatit
    pommit = []
    # lippujen koordinaatit
    liput = []
    # avatut ruudut
    nakyvat = []

def aseta_pommit():
    """Asettaa pommit satunnaisiin paikkoihin backend-matriisissa."""
    
    i = 0
    # lkm = pommien lukumäärä (määritetään kysy_koko()-funktiossa)
    while i < lkm:
        sat_rivi = random.randint(0, n - 1)
        sat_sarake = random.randint(0, n - 1)
        if mat_back[sat_rivi][sat_sarake] != -1:
            mat_back[sat_rivi][sat_sarake] = -1
            pommit.append((sat_rivi, sat_sarake))
            i += 1           

def numerointi():
    """Numeroi backend-matriisissa kosketuksissa olevien pommien määrä per ruutu."""
    
    for i in range(len(mat_back)):
        for j in range(len(mat_back[i])):
            # jos huomataan -1 eli pommi:
            if mat_back[i][j] == -1:
                # rajataan alue, ja jonka kaikkien -1 poikkeavien arvojen tilalle lisätään yhtä isompi luku
                # chatgpt setit: https://chat.openai.com/share/556805c3-c6f9-47d0-b1d3-e9bb33296c3f
                for x in range(max(0, i-1), min(i+2, len(mat_back))):
                    for y in range(max(0, j-1), min(j+2, len(mat_back[i]))):
                        if mat_back[x][y] != -1:
                            mat_back[x][y] += 1

def tulosta_ruudukko() -> str:
    """Tulostaa pelilaudan ruudukkona."""
    
    # tulostetaan ruudukon katto
    print("______" * n + "_")
    
    # tulostetaan ruudukko vaakarivi kerrallaan
    for lista in mat_front:
        print("|     " * n + "|")
        # iteroidaan listan alkiot, jotta saadaa rivin jokaiseen slottiin oikeat arvot
        rivi = ""
        for alkio in range(n):
            rivi += "|  " + str(lista[alkio]) + "  "
        print(rivi + "|")
        print("|_____" * n + "|")

def pelaajan_valinta():
    """Kysyy avattavan ruudun koordinaatit."""
    
    global toiminto
    global x
    global y

    # looppi yksinkertaista virheenkäsittelyä varten
    while True:
        try:
            # "" / "å" / "f"
            toiminto = input("Toiminto: ")
            # takaovi jos haluu pelistä vittuun
            if toiminto == "å":
                exit()
            elif (toiminto != "") and (toiminto != "f"):
                print("Virheellinen toiminto!")
                continue
         
            x = int(input("Anna x: "))
            y = int(input("Anna y: "))
            
            if (x > n) or (x < 0) or (y > n) or (y < 0):
                print(f"Anna lukuja vain väliltä 0-{n}.")
            else:
                break
        except ValueError:
            print("Vain numerot kelpaavat!")
    
    # muutetaan reaalimaailman koordinaatit python-ystävällisiksi (listojen eka indeksi 0 eikä 1!)
    y -= 1
    x -= 1  
    
def ruutujen_muutos_frontissa():
    """Muuttaa näkyviä ruutuja pelaajan antamien koordinaattien perusteella."""
    
    global peli_loppu
    global voitto
    global y
    global x
        
    # liputus
    if toiminto == "f":
        if mat_front[y][x] != "F":
            # katsotaan montako lippua on vielä käytettävissä
            if len(liput) < lkm:
                mat_front[y][x] = "F"
                # lisätään koordinaatit liputettujen ruutujen listaan
                liput.append((y, x))
        # lipun muutos tyhjäksi
        elif mat_front[y][x] == "F":
            mat_front[y][x] = " "
            # poistetaan koordinaatit liputettujen ruutujen listaan
            liput.remove((y, x))
            
    # ruudun avaus moodi
    else:
        # jos ruutu on 0 mat_backissa...
        if mat_back[y][x] == 0:
            # ...niin muutetaan se ruutu 0 ja avataan muutkin ruudut siitä ympäriltä fronttiin
            for y in range(max(0, y-1), min(y+2, len(mat_back))):
                for x in range(max(0, x-1), min(x+2, len(mat_back[y]))):
                    if mat_back[y][x] != -1:
                        mat_front[y][x] = mat_back[y][x]
                        # lisätään koordinaatit avattujen ruutujen listaan
                        if (y, x) not in nakyvat:
                            nakyvat.append((y, x))
        
        # jos osutaan pommiin ;)
        elif mat_back[y][x] == -1:
            # lisätään koordinaatit avattujen ruutujen listaan
            nakyvat.append((y, x))
            # iteroidaan matriisi läpi ja muutetaan kaikki pommit fronttiin esille
            for i in range(len(mat_back)):
                for j in range(len(mat_back[i])):
                    # jos huomataan -1 eli pommi:
                    if mat_back[i][j] == -1:
                        mat_front[i][j] = "M"
            # ja päätetään peli     
            peli_loppu = True
        
        # muussa tapauksessa avataan ainoastaan kyseinen ruutu
        else:
            mat_front[y][x] = mat_back[y][x]
            # lisätään koordinaatit avattujen ruutujen listaan
            nakyvat.append((y, x))
    
    # testataan voittoa (onko kaikki pommit liputettu)
    maara = 0
    for lippu in liput:
        if lippu in pommit:
            maara += 1
    
    if maara == lkm:    
        peli_loppu = True
        voitto = True

def ohjeet_str() -> str:
    """Tulostaa ohjeet/perusnäkymän pelin aikana."""
    
    print("Miinaharava Extended Horror Experience!")
    print()
    print("Toiminnot: ruudun avaus \"\" / liputus \"f\"")       

def voitto_str() -> str:
    """Tulostaa ohjeet/perusnäkymän voittoa varten."""
    
    print("Voitit pelin lol")
    print()
    print("Toiminnot: kyllä \"k\" / ei \"e\"")

def tappio_str() -> str:
    """Tulostaa ohjeet/perusnäkymän tappiota varten."""
    
    print("Miinaharavasi meni rikki ja osuit neuvostoaikaiseen räjähtämättömään sirpalemiinaan.")
    print("Olet nyt pyörätuolipotilas lopun ikäsi. Hävisit siis pelin :D")
    print("Toiminnot: kyllä \"k\" / ei \"e\"")

def tallenna_pelin_tiedot(nakyvat, liput):
    """Tallentaa pelin tiedot tiedostoon."""
    
    with open("pelin_tiedot.txt", "w") as tiedosto:
        tiedosto.write("____________________________________________\n")
        tiedosto.write("Pelitiedot:\n")
        tiedosto.write(f"Avasit {len(nakyvat)} ruutua. Hyvä sinä!\n")
        tiedosto.write(f"Liputit {len(liput)} ruutua. Mahtavaa!\n")
        tiedosto.write("____________________________________________")

def tulosta_pelin_tiedot() -> str:
    """Tulostaa pelin tiedot tiedostosta."""
    
    with open("pelin_tiedot.txt", "r") as tiedosto:
        tiedot = tiedosto.read()
        print(tiedot)

def kysy_lopetus():
    """Kysyy käyttäjältä pelitietojen tulostuksesta ja uudelleenpelaamisesta."""
    
    global lopeta_pelaaminen
    
    while True:
        tulosta = input("Pelitietojen tulostus: ")
        if tulosta == "k":
            tulosta_pelin_tiedot()
            break
        elif tulosta == "e":
            break
        else:
            print("Virheellinen toiminto!")
    
    while True:
        lopetus = input("Pelin lopetus: ")
        if lopetus == "e":
            break
        elif lopetus == "k":
            lopeta_pelaaminen = True
            break
        else:
            print("Virheellinen toiminto!")


# PÄÄOHJELMA
if __name__ == "__main__":
    """Käytännössä peli pelataan tässä."""
    
    lopeta_pelaaminen = False
    
    while not lopeta_pelaaminen:
        tyhjenna_terminaali()
        
        # kysytään alkuarvoja
        kysy_koko()
        
        # alustetaan matriisit ja listat sekä asetetaan mat_backiin pommit ja niiden ympärille numerot
        alusta_listat_ja_matriisit()
        aseta_pommit()
        numerointi()
        
        # ruutujen_muutos_frontissa()-funktiossa testataan pommiin osumista sekä voittoa
        peli_loppu = False
        voitto = False
        
        while True:
            tyhjenna_terminaali()
            ohjeet_str()
            tulosta_ruudukko()
            pelaajan_valinta()
            ruutujen_muutos_frontissa()
            
            if peli_loppu:
                if voitto:
                    tyhjenna_terminaali()
                    voitto_str()
                    tulosta_ruudukko()
                    tallenna_pelin_tiedot(nakyvat, liput)
                    break
                else:
                    tyhjenna_terminaali()
                    tappio_str()
                    tulosta_ruudukko()
                    tallenna_pelin_tiedot(nakyvat, liput)
                    break
        kysy_lopetus()
    exit()