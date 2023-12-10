"""Viimeisin toimiva versio."""

import pygame
import random
from os import system, name

def game_over():
    """Avaa koko näytön kokoisen ikkunan jossa on kuva."""
    
    # toimii, mutta ei halutulla tavalla. vika on tavassa käyttää funktiota ja pygamea itsessään
    leveys, korkeus = 1600, 900
    ikkuna = pygame.display.set_mode((leveys, korkeus))
    pygame.display.set_caption("Game Over")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        lataa_kuva = pygame.image.load("scoreboard.jpg").convert()
        ikkuna.blit(lataa_kuva, (0, 0))
        pygame.display.flip()

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
    
    # lkm = pommien lukumäärä (määritetään kysy_koko()-funktiossa)
    for _ in range(lkm):
        sat_rivi = random.randint(0, n - 1)
        sat_sarake = random.randint(0, n - 1)
        mat_back[sat_rivi][sat_sarake] = -1

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
        for alkio in range(0, n):
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
                
            x = int(input("Anna x: "))
            y = int(input("Anna y: "))
            
            if (toiminto != "") and (toiminto != "f"):
                print("Virheellinen toiminto!")
            elif (x > n) or (x < 0) or (y > n) or (y < 0):
                print(f"Anna lukuja vain väliltä 0 - {n}.")
            else:
                break
        except ValueError:
            print("Vain numerot kelpaavat!")
    
    # muutetaan koordinaatit python-ystävällisiksi (listojen eka on indeksi 0 eikä 1!)
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
    global g_over
    
    # lisätään koordinaatit jo valittujen joukkoon (täl listal ei atm mitään käyttöö)
    nakyvat.append((x, y))
    
    # liputus
    if toiminto == "f":
        if mat_front[y][x] != "F":
            mat_front[y][x] = "F"
        # lipun muutos tyhjäksi
        elif mat_front[y][x] == "F":
            mat_front[y][x] = " "
            
    # ruudun avaus moodi
    else:
        # jos ruutu on 0 mat_backissa...
        if mat_back[y][x] == 0:
            # ...niin muutetaan se ruutu 0 ja avataan muutkin ruudut siitä ympäriltä fronttiin
            for y in range(max(0, y-1), min(y+2, len(mat_back))):
                for x in range(max(0, x-1), min(x+2, len(mat_back[y]))):
                    if mat_back[y][x] != -1:
                        mat_front[y][x] = mat_back[y][x]
        
        # jos osutaan pommiin ;)
        elif mat_back[y][x] == -1:
            # iteroidaan matriisi läpi ja muutetaan kaikki pommit fronttiin esille
            for i in range(len(mat_back)):
                for j in range(len(mat_back[i])):
                    # jos huomataan -1 eli pommi:
                    if mat_back[i][j] == -1:
                        mat_front[i][j] = "M"
            # ja päätetään peli     
            g_over = True
        
        # muussa tapauksessa avataan ainoastaan kyseinen ruutu
        else:
            mat_front[y][x] = mat_back[y][x]          

def ohjeet() -> str:
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
    # else:
        # _ = system("clear")
        
      
# kvg mitä meinaa :D (taitaa olla vähän turha mut näyttää ainaki kivalt)
if __name__ == "__main__":
    """Käytännössä peli pelataan tässä."""
    
    tyhjenna_terminaali()
    
    # kysytään alkuarvoja
    kysy_koko()
    
    # backend-matriisi
    mat_back = [[0 for rivi in range(n)] for sarake in range(n)] 
    # frontend-matriisi
    mat_front = [[" " for rivi in range(n)] for sarake in range(n)]
    # listataan liputetut koordinaatit (tupleina?) atm hyödytön
    liput = []
    # listataan jo näkyvissä olevat ruudut (tupleina?) atm hyödytön
    nakyvat = []
    
    # asetetaan pommit ja niiden ympärille numerot mat_backiin
    aseta_pommit()
    numerointi()
    
    # ruutujen_muutos_frontissa()-funktiossa testataan pommiin osumista
    g_over = False
    
    while not g_over:
        tyhjenna_terminaali()
        ohjeet()
        tulosta_ruudukko()
        pelaajan_valinta()
        ruutujen_muutos_frontissa()
        
        if g_over:
            # pirkkaversio. tää ei oo horroria nähnykkää
            tyhjenna_terminaali()
            print("Miinaharavasi meni rikki ja osuit neuvostoaikaiseen räjähtämättömään sirpalemiinaan.")
            print()
            print("Olet nyt pyörätuolipotilas lopun ikäsi. Hävisit siis pelin :D")
            tulosta_ruudukko()
            exit()
