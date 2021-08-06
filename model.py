import hashlib
import json
import random


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, dan, kalorije=None):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.dan = dan
        self.kalorije = kalorije
    
    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik        
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Dan())
            uporabnik.v_datoteko()
            return uporabnik

    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"


    def v_slovar(self):
        if self.kalorije is None:
            pretvorjene_kalorije = {}
        else:
            pretvorjene_kalorije = self.kalorije.v_slovar()
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "dan": self.dan.v_slovar(),
            "kalorije": pretvorjene_kalorije
        }

    def v_datoteko(self):
        with open(
            Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w"
        ) as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        dan = Dan.iz_slovarja(slovar["dan"])
        if slovar["kalorije"] == {}:
            kalorije = None
        else:
            kalorije = Kalorije.iz_slovarja(slovar["kalorije"])
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, dan, kalorije)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

    def dodaj_kalorije(self, teza, visina, starost, spol, aktivnost):
        self.kalorije = Kalorije(teza, visina, starost, spol, aktivnost)

    def dodaj_dan(self):
        izracun = self.kalorije.izracun_kalorij()
        self.dan.dodaj_izracun_v_dan(izracun)

    def izbrisi_dneve(self):
        self.dan.pobrisi_vse_dneve()



class Kalorije:
    def __init__(self, teza, visina, starost, spol, aktivnost):
        self.teza = teza
        self.visina = visina
        self.starost = starost
        self.spol = spol
        self.aktivnost = aktivnost

    def izracun_bmr(self):
        if self.spol == "zenski":
            izracun = 10 * self.teza + 6.25 * self.visina - 5 * self.starost - 161
        
        elif self.spol == "moski":
            izracun = 10 * self.teza + 6.25 * self.visina - 5 * self.starost + 5
        
        return izracun

    def izracun_kalorij(self):
        izracun_bmr = self.izracun_bmr()

        if self.aktivnost == 1:
            skupaj = izracun_bmr * 1.2
        
        elif self.aktivnost == 2:
            skupaj = izracun_bmr * 1.375

        elif self.aktivnost == 3:
            skupaj = izracun_bmr * 1.55

        elif self.aktivnost == 4:
            skupaj = izracun_bmr * 1.725

        elif self.aktivnost == 5:
            skupaj = izracun_bmr * 1.9

        return skupaj

    
    def v_slovar(self):
        return {
            "teza": self.teza,
            "visina": self.visina,
            "starost": self.starost,
            "spol": self.spol,
            "aktivnost": self.aktivnost
        }
    
    @classmethod
    def iz_slovarja(cls, slovar):
        teza = slovar["teza"]
        visina = slovar["visina"]
        starost = slovar["starost"]
        spol = slovar["spol"]
        aktivnost = slovar["aktivnost"]
        kalorije = Kalorije(teza, visina, starost, spol, aktivnost)
        return kalorije

#    def shrani_v_datoteko(self, ime_datoteke):
#        with open(ime_datoteke, "w") as dat:
#            slovar = self.v_slovar()
#            json.dump(slovar, dat)

#    def preberi_iz_datoteke(ime_datoteke):
#        with open(ime_datoteke) as dat:
#            slovar = json.load(dat)
#            return Dan.iz_slovarja(slovar)


class Dan:
    def __init__(self):
        self.dnevi = [] 

    def dodaj_izracun_v_dan(self, izracun):
        self.dnevi.append(izracun)

    def stanje_izracuna_do_sedaj(self):
        return self.dnevi

    def pobrisi_vse_dneve(self):
        self.dnevi.clear()
    
    def v_slovar(self):
        slovar = {"krneki": self.dnevi}
        return slovar

    @classmethod
    def iz_slovarja(cls, slovar):
        dan = Dan()
        dan.dnevi = slovar["krneki"]
        return dan

#    def shrani_v_datoteko(self):
#        with open(self.ime_datoteke, "w") as dat:
#            slovar = self.dnevi()
#            json.dump(slovar, dat)

#    def preberi_iz_datoteke(self):
#        with open(self.ime_datoteke) as dat:
#            slovar = json.load(dat)
#            self.dnevi = slovar