import random

koko = input("Anna koko (iso tai pieni): ")

if koko == "iso":
    n = 10
    y_n = 5
elif koko == "pieni":
    n = 5
    y_n = 2


matriisi = [['|_|' for _ in range(n)] for _ in range(n)]

for _ in range(y_n):
    satunnainen_rivi = random.randint(0, n - 1)
    satunnainen_sarake = random.randint(0, n - 1)
    matriisi[satunnainen_rivi][satunnainen_sarake] = 'B'

for rivi in matriisi:
    print(' '.join(rivi))