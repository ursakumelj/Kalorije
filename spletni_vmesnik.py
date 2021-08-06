import bottle
from model import Uporabnik

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.iz_datoteke(uporabnisko_ime)


@bottle.get("/")
def zacetna_stran():
    bottle.redirect("/dnevnik/")


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("prijava.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "prijava.html", napaka=e.args[0]
        )

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.get("/dnevnik/")
def prikaz_dnevnika():
    uporabnik = trenutni_uporabnik()
    return bottle.template("dnevnik.html", uporabnik=uporabnik)

@bottle.post("/dodaj_dan/")
def dodajmo_nov_dan():
    uporabnik = trenutni_uporabnik()
    teza = float(bottle.request.forms["teza"])
    spol = (bottle.request.forms["spol"])
    starost = float(bottle.request.forms["starost"])
    visina = float(bottle.request.forms["visina"])
    aktivnost = float(bottle.request.forms["aktivnost"])
    uporabnik.dodaj_kalorije(teza, visina, starost, spol, aktivnost)
    uporabnik.dodaj_dan()
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.post("/izbrisi_dneve/")
def izbrisimo_dneve():
    uporabnik = trenutni_uporabnik()
    uporabnik.izbrisi_dneve()
    shrani_stanje(uporabnik)
    bottle.redirect("/")

bottle.run(debug=True, reloader=True)

