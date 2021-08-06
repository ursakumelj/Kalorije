from model import Dan, Kalorije

IME_DATOTEKE = "podatki.json"

def tekstovni_vmesnik():
    belezeni_dnevi = Dan(IME_DATOTEKE)
    belezeni_dnevi.preberi_iz_datoteke()
    while True:
        ukaz = prikaz_moznosti()
        if ukaz == 1:
            podatki = prikaz_za_izpolnitev()
            koncno = Kalorije(podatki[0], podatki[1], podatki[2], podatki[3], podatki[4])
            izracun = koncno.izracun_kalorij()
            belezeni_dnevi.dodaj_izracun_v_dan(izracun)
            belezeni_dnevi.shrani_v_datoteko()
        elif ukaz == 2:
            print(belezeni_dnevi.stanje_izracuna_do_sedaj())
            input("pritisni 1 za naprej")
        elif ukaz == 3:
            belezeni_dnevi.pobrisi_vse_dneve()
            print("Pobrisali smo vse dneve.")
            input("pritisni 1 za naprej")

def prikaz_za_izpolnitev():
    print("Izpolni podatke:") 
    teza = int(input("teža:"))
    visina = int(input("višina:"))
    starost = int(input("starost:"))
    spol = input("spol (ženski ali moški):")
    aktivnost = int(input("Kako zelo ste aktivni? 1 za skoraj nič, 2 za malo/1-3 dni na teden, 3 za srednje/3-5 dni na teden, 4 za veliko/6-7 dni na teden, in 5 za zelo veliko/večkrat na dan:"))
    return (teza, visina, starost, spol, aktivnost)

def prikaz_moznosti():
    print("Živjo! Vpiši 1, da ")
    return int(input("1/2/3"))

tekstovni_vmesnik()