"""Viimeisin toimiva versio."""

import random
from os import system, name

def kysy_koko():
    """Pelin esittely ja pelikentän koon kysyntä.

        Peli on koodattu siten, että pelikentän kokoa ja pommien lukumäärää voi halutessaan vaihtaa helposti
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
    print("Pelilaudat: pieni 5x5, iso 10x10")
    print()

    while True:
        koko = input("Anna pelilaudan koko: \"pieni\" / \"iso\": ")
        
        # koko määrittää rivien/sarakkeiden määrän (n) sekä pommine lukumäärän (lkm)
        if koko == "pieni":
            n = 5
            lkm = 3
            break
        elif koko == "iso":
            n = 10
            lkm = 13
            break
        else:
            print("Opettele kirjottaa, pls!")
            
def aseta_pommit():
    """Asettaa pommit satunnaisiin paikkoihin backend-matriisissa."""
    
    global mat_back
    global lkm
    
    i = 0
    # lkm = pommien lukumäärä (määritetään kysy_koko()-funktiossa)
    while i < lkm:
        sat_rivi = random.randint(0, n - 1)
        sat_sarake = random.randint(0, n - 1)
        if mat_back[sat_rivi][sat_sarake] != -1:
            mat_back[sat_rivi][sat_sarake] = -1
            pommit.append((sat_rivi, sat_sarake))
            i += 1           

def tulosta_ruudukko() -> str:
    """Tulostaa pelilaudan ruudukkona."""
    
    global n
    global mat_front
    
    # tulostetaan taulukon katto
    print("______" * n + "_")
    
    # tulostetaan taulukko vaakarivi kerrallaan
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
            # jos haluu pelistä vittuun
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
    x -= 1
    y -= 1
    
def numerointi():
    """Numeroidaan backend-matriisissa kosketuksissa olevien pommien määrä per ruutu."""
    
    global mat_back
    
    for i in range(len(mat_back)):
        for j in range(len(mat_back[i])):
            # jos huomataan -1 eli pommi:
            if mat_back[i][j] == -1:
                # rajataan alue, ja jonka kaikkien -1 poikkeavien arvojen tilalle lisätään yhtä isompi luku
                # chatgpt setit, linkki jossain
                for x in range(max(0, i-1), min(i+2, len(mat_back))):
                    for y in range(max(0, j-1), min(j+2, len(mat_back[i]))):
                        if mat_back[x][y] != -1:
                            mat_back[x][y] += 1

def ruutujen_muutos_frontissa():
    """Muuttaa ruutuja pelaajan antamien koordinaattien perusteella."""
    
    global nakyvat
    global x
    global y
    global peli_loppu
    global voitto
    global lkm
        
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
    """Tulostaa ohjeet / perusnäkymän pelin alettua."""
    
    print("Miinaharava Extended Horror Experience!")
    print()
    print("Toiminnot: ruudun avaus \"\" / liputus \"f\"")

def tyhjenna_terminaali():
    """Komento tyhjentää terminaalin käyttöjärjestelmän huomioiden."""
    
    # windows
    if name == "nt":
        _ = system("cls")
    # mac / linux
    else:
        _ = system("clear")

def tallenna_pelin_tiedot(avatut_ruudut, liputetut_ruudut):
    """Tallentaa pelin tiedot tiedostoon."""
    
    with open('pelin_tiedot.txt', 'w') as tiedosto:
        tiedosto.write(f"Avasit {avatut_ruudut} ruutua! Hyvä sinä!\n")
        tiedosto.write(f"Liputit {liputetut_ruudut} ruutua! Mahtavaa!\n")
    pass

def tulosta_pelin_tiedot():
    """Tulostaa pelin tiedot tiedostosta."""
    
    with open('pelin_tiedot.txt', 'r') as tiedosto:
        tiedot = tiedosto.read()
        print(tiedot)
    pass

def tappio_str() -> str:
    print("Miinaharavasi meni rikki ja osuit neuvostoaikaiseen räjähtämättömään sirpalemiinaan.")
    print()
    print("Olet nyt pyörätuolipotilas lopun ikäsi. Hävisit siis pelin :D")
    
def voitto_str() -> str:
    print("Voitit pelin lol")
    print()
    print()
    
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

# PÄÄOHJELMA
if __name__ == "__main__":
    """Käytännössä peli pelataan tässä."""
    
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
    
    while not peli_loppu:
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
                exit()
            else:
                tyhjenna_terminaali()
                tappio_str()
                tulosta_ruudukko()
                exit()
        