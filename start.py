import random
import pygame

def game_over(): 
    leveys, korkeus = 1600, 900
    ikkuna = pygame.display.set_mode((leveys, korkeus))
    pygame.display.set_caption("Game Over")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        lataa_kuva = pygame.image.load("horror.jpg").convert()
        ikkuna.blit(lataa_kuva, (0, 0))
        pygame.display.flip()

print("Pelaat peliä Miinaharava Extended Horror Experience!")
print("Pelilaudan koot: pieni 5x5, iso 10x10")
koko = input("Anna pelilaudan koko (pieni / iso): ")

if koko == "iso":
    n = 10
    y_n = 5
elif koko == "pieni":
    n = 5
    y_n = 2


matriisi = [['/' for _ in range(n)] for _ in range(n)]


rivi = int(input("Anna rivi: "))
sarake = int(input("Anna sarake: "))

ruutu = "0"
matriisi[rivi][sarake] = ruutu


for _ in range(y_n):
    satunnainen_rivi = random.randint(0, n - 1)
    satunnainen_sarake = random.randint(0, n - 1)
    if matriisi[satunnainen_rivi][satunnainen_sarake] == ruutu:
        y_n += 1
    else:
        matriisi[satunnainen_rivi][satunnainen_sarake] = 'B'

for rivi in matriisi:
    print(' '.join(rivi))

