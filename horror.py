
import random

matriisi = [[]]

koko = input("Anna koko (iso tai pieni): ")

def luo_kentta():

    global matriisi 
    global koko

    if koko == "iso":
        n = 10
        
    elif koko == "pieni":
        n = 5
        
    else:
        print(f"Väärä koko, syötä iso/pieni")

    matriisi = [['0' for _ in range(n)] for _ in range(n)]

    return koko



""" 
luo pelikentän käyttäjän haluaman koon mukaan

Parametrit:
iso = 10x10 pelikenttä
pieni = 5x5 pelikenttä

"""


def aseta_pommit():

    global matriisi
    global koko

    if koko == "iso":
        n = 10
        lkm = 5
        
    elif koko == "pieni":
        n = 5
        lkm = 2

    pommit_koordinaatit = []

    for _ in range(lkm):
        
        satunnainen_rivi = random.randint(0, n - 1)
        satunnainen_sarake = random.randint(0, n - 1)
        matriisi[satunnainen_rivi][satunnainen_sarake] = 'B'
        pommit_koordinaatit.append((satunnainen_rivi,satunnainen_sarake))

    
    
    return pommit_koordinaatit




"""
aettaa pommeja pelikentän koon mukaisen määrän

Parametrit:
iso = 5 pommia
pieni = 2 pommia

"""


def pelaajan_valinta(pommit_koordinaatit):
    global matriisi

    pelaajan_valinnat = []

    while True:
        for rivi in matriisi:
            print(' '.join(rivi))

        rivi = int(input("Anna rivi: "))
        sarake = int(input("Anna sarake: "))

        pelaajan_valinta_koordinaatti = (rivi, sarake)

        if pelaajan_valinta_koordinaatti in pommit_koordinaatit:
            print("Game Over")
            break

        valittu_ruutu = "J"
        try:
            matriisi[rivi][sarake] = valittu_ruutu
        except IndexError:
            print("Virhe: list assignment index out of range")
            break

        pelaajan_valinnat.append((valittu_ruutu, pelaajan_valinta_koordinaatti))

    return valittu_ruutu, pelaajan_valinta_koordinaatti, pelaajan_valinnat
        


    
"""
luo pelikentälle pelaajan valinnan

Parametrit:
valittu_ruutu = tuple, jossa koordinaatit. esim (1,2)

"""

def montako_miinusta(pelaajan_valinta):
    pass

"""
laskee, montako -1 arvoa on pelaajan valitseman ruudun ympärillä

Parametrit:
valittu_ruutu = tuple, jossa koordinaatit. esim (1,2)

"""

def peli_paattyy():

    print(f"peli päättyi, {tulokset}")

    

"""
jos osuu pommiin, tulee game over.

"""

luo_kentta()

pommit_koordinaatit = aseta_pommit()   

tulokset = pelaajan_valinta(pommit_koordinaatit)

peli_paattyy(tulokset)

