import datetime;
import curses;
import json;

KUUKAUDET = {
    1: "Tammikuu",
    2: "Helmikuu",
    3: "Maaliskuu",
    4: "Huhtikuu",
    5: "Toukokuu",
    6: "Kesäkuu",
    7: "Heinäkuu",
    8: "Elokuu",
    9: "Syyskuu",
    10: "Lokakuu",
    11: "Marraskuu",
    12: "Joulukuu"
}

KUUKAUSIPAIVAT = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

VIIKONPAIVAT = {
    1: "Maanantai",
    2: "Tiistai",
    3: "Keskiviikko",
    4: "Torstai",
    5: "Perjantai",
    6: "Lauantai",
    7: "Sunnuntai"
}

class Kalenteri():
    def __init__(self):
        
        self.stdscr = curses.initscr()
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
        
        self.vuosi = datetime.date.today().isocalendar()[0]
        self.kuukausi = datetime.date.today().month
        self.viikko = datetime.date.today().isocalendar()[1]
        self.viikonpaiva = datetime.date.today().isocalendar()[2]
        self.paiva = datetime.date.today().day
        
        self.vuosiTanaan = datetime.date.today().isocalendar()[0]
        self.kuukausiTanaan = datetime.date.today().month
        self.viikkoTanaan = datetime.date.today().isocalendar()[1]
        self.viikonpaivaTanaan = datetime.date.today().isocalendar()[2]
        self.paivaNumeroTanaan = datetime.date.today().day
        
        self.mode = "viikko" # viikko tai kuukausi    
        self.selectedPaiva = datetime.date.today().isocalendar()[2]
        self.selectedX = 0
        self.selectedY = 0
        
        self.maxX = 0
        
        self.kirjoitusPaalla = False
        self.user_input = ""
        
        f = open("./muistutukset.json", "r")
        self.muistiinPanot = json.load(f)
    
        self.render()
    
    def run(self):
        
        while True:
            key = self.stdscr.getch()
            if (key == 111):
                self.renderOhje()
            else:
                self.kasittelePainallus(key, self.mode)
                self.render()
    
    # renderöi oikea näkymä riippuen modesta
    def render(self):
        if (self.mode == "viikko"):
            return self.renderViikkoNakyma()
        elif (self.mode == "kuukausi"):
            return self.renderKuukausiNakyma()        
                    
    def renderViikkoNakyma(self):
        
        self.stdscr.clear()
    
        self.stdscr.addstr(1, 0, f"{self.vuosi} - {self.getKuukausi(self.viikko)} - Viikko {self.viikko}", curses.color_pair(4))
        self.stdscr.addstr(2, 0, f"{self.getPaivaNumero(1, self.viikko)}. Maanantai", self.getViikonPaivaVari(1))
        self.stdscr.addstr(3, 0, f"{self.getPaivaNumero(2, self.viikko)}. Tiistai", self.getViikonPaivaVari(2))
        self.stdscr.addstr(4, 0, f"{self.getPaivaNumero(3, self.viikko)}. Keskiviikko", self.getViikonPaivaVari(3))
        self.stdscr.addstr(5, 0, f"{self.getPaivaNumero(4, self.viikko)}. Torstai", self.getViikonPaivaVari(4))
        self.stdscr.addstr(6, 0, f"{self.getPaivaNumero(5, self.viikko)}. Perjantai", self.getViikonPaivaVari(5))
        self.stdscr.addstr(7, 0, f"{self.getPaivaNumero(6, self.viikko)}. Lauantai", self.getViikonPaivaVari(6))
        self.stdscr.addstr(8, 0, f"{self.getPaivaNumero(7, self.viikko)}. Sunnuntai", self.getViikonPaivaVari(7))
        
        self.stdscr.addstr(2, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 1)}", curses.color_pair(3))
        self.stdscr.addstr(3, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 2)}", curses.color_pair(3))
        self.stdscr.addstr(4, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 3)}", curses.color_pair(3))
        self.stdscr.addstr(5, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 4)}", curses.color_pair(3))
        self.stdscr.addstr(6, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 5)}", curses.color_pair(3))
        self.stdscr.addstr(7, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 6)}", curses.color_pair(3))
        self.stdscr.addstr(8, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 7)}", curses.color_pair(3))
        
        self.stdscr.addstr(10, 0, f"o: Ohje", curses.color_pair(5))
        
            
        self.stdscr.refresh()
        
    def renderKuukausiNakyma(self):
        self.stdscr.clear()
        
        self.stdscr.addstr(1, 0, f"{self.vuosi} - {KUUKAUDET[self.kuukausi]}", curses.color_pair(4))
        self.stdscr.addstr(2, 0, f"Ma", curses.color_pair(4))
        self.stdscr.addstr(2, 5, f"Ti", curses.color_pair(4))
        self.stdscr.addstr(2, 10, f"Ke", curses.color_pair(4))
        self.stdscr.addstr(2, 15, f"To", curses.color_pair(4))
        self.stdscr.addstr(2, 20, f"Pe", curses.color_pair(4))
        self.stdscr.addstr(2, 25, f"La", curses.color_pair(4))
        self.stdscr.addstr(2, 30, f"Su", curses.color_pair(4))
        

        # kuukauden ensimmäisen päivän viikonpäivä
        ekaViikonpaiva = datetime.date(self.vuosi, self.kuukausi, 1).weekday()
       
        x = 0 # viikko
        y = ekaViikonpaiva #"[1-8]"
        
        self.maxX = 0
        vikanViikonPaivat = 0
        
        viikkoMaara = ((KUUKAUSIPAIVAT[self.kuukausi] - ekaViikonpaiva) // 7)
        if ((KUUKAUSIPAIVAT[self.kuukausi] - ekaViikonpaiva) % 7 > 0):
            viikkoMaara += 1
            vikanViikonPaivat = (KUUKAUSIPAIVAT[self.kuukausi] - ekaViikonpaiva) % 7
        
        if (self.selectedX == 0):
            if (self.selectedY < ekaViikonpaiva):
                self.selectedY = ekaViikonpaiva
            
        if (self.selectedX == viikkoMaara - 1):
            if (self.selectedY > vikanViikonPaivat + 1):
                self.selectedY = 0

        ## renderöi päivä numerot
        for i in range(1, KUUKAUSIPAIVAT[self.kuukausi] + 1):
            
            if (y == 7):
                y = 0
                x += 1
                self.maxX = max(self.maxX, x)
                
            if (self.selectedX == x and self.selectedY == y):
                self.stdscr.addstr(3 + x, y * 5, f"{i}", curses.color_pair(6))
                self.selectedPaiva = y
                self.paiva = i
                pvm_obj = datetime.date(self.vuosi, self.kuukausi, i)
                self.viikko = int(pvm_obj.isocalendar()[1])
            elif (self.vuosi == self.vuosiTanaan and self.kuukausi == self.kuukausiTanaan and self.paivaNumeroTanaan == i):
                self.stdscr.addstr(3 + x, y * 5, f"{i}", curses.color_pair(5))
            else:    
                self.stdscr.addstr(3 + x, y * 5, f"{i}", self.getPaivaVari(self.vuosi, self.kuukausi, i))
            
            y += 1
        
        muistutukset = self.haeKuukaudenMuistutukset()
        for i in range(len(muistutukset)):
            self.stdscr.addstr(3 + i, 8 * 5, f"{muistutukset[i]['paiva']}. Päivä {muistutukset[i]['muistutus']}", curses.color_pair(3))
         
        self.stdscr.addstr(10, 0, f"o: Ohje", curses.color_pair(5))
       
    ## renderöi uusi muistutus näkymä  
    def renderUusiMuistutus(self):
        self.stdscr.clear()
        self.kirjoitusPaalla = True
        curses.noecho()
        self.stdscr.addstr(1, 0, f"Lisää uusi muistutus", curses.color_pair(4))
        self.stdscr.addstr(2, 0, f"{str(datetime.date.fromisocalendar(self.vuosi, self.viikko, self.selectedPaiva + 1))}", curses.color_pair(3))
        self.stdscr.addstr(3, 0, f"{self.user_input}", curses.color_pair(1))
        
        def onMerkki(key):
            return (ord('a') <= key <= ord('z') or
                    ord('A') <= key <= ord('Z') or
                    ord('0') <= key <= ord('9') or
                    key == ord('.') or
                    key == ord(','))
        
        key = self.stdscr.getch()
        if key == 10:  # enter
            self.kirjoitusPaalla = False
            if (self.mode == "viikko"):
                self.lisaaMuistutus(vuosi = self.vuosi, 
                                    viikko = self.viikko, 
                                    viikonpaiva = self.selectedPaiva,
                                    muistutus = self.user_input)
            elif (self.mode == "kuukausi"):
                self.lisaaMuistutus(paivamaara = str(datetime.date(self.vuosi, self.kuukausi, self.paiva)),
                                    muistutus = self.user_input)
            self.user_input = ""
            return self.render()
        elif key == 27:  # esq
            self.user_input = ""
        elif key == curses.KEY_BACKSPACE or key == 8 or key == curses.KEY_DC:
            self.user_input = self.user_input[:-1]
        else:
            if (onMerkki(key)) or key == 32: 
                # 32 space
                self.user_input += chr(key)
            
        return self.renderUusiMuistutus()    
    
    def renderOhje(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 0, f"Viikkonäkymä:", curses.color_pair(7))
        self.stdscr.addstr(2, 0, f"Nuolinäppäimet: Vaihda päivää / viikkoa", curses.color_pair(4))
        self.stdscr.addstr(3, 0, f"tai W-A-S-D", curses.color_pair(4))
        self.stdscr.addstr(6, 0, f"Enter: Lisää muistutus", curses.color_pair(4))
        self.stdscr.addstr(7, 0, f"p: Poista muistutus", curses.color_pair(4))
        self.stdscr.addstr(8, 0, f"m: Vaihda näkymää", curses.color_pair(4))
        
        self.stdscr.addstr(1, 50, f"Kuukausinäkymä:", curses.color_pair(7))
        self.stdscr.addstr(2, 50, f"Vasen- ja oikeanuoli: vaihda kuukausi", curses.color_pair(4))
        self.stdscr.addstr(3, 50 ,f"W-A-S-D näppäimet: vaihda päivä", curses.color_pair(4))
        
        self.stdscr.addstr(10, 0, f"q: Sulje ohje", curses.color_pair(5))
        
        while True:
            key = self.stdscr.getch()
            if key == 113: # q: sulje ohje
                return self.render()
            
    def setEdellinenViikko(self):
        if (self.viikko == 1):
            if (self.onKarkausVuosi(self.vuosi - 1)):
                self.viikko = 53
            else:
                self.viikko = 52
                self.vuosi -= 1
        else: 
            self.viikko -= 1
            
    def setSeuraavaViikko(self):
        if self.viikko == 52 or (self.viikko == 53 and not self.onKarkausVuosi(self.vuosi)):
            self.viikko = 1
            self.vuosi +=  1
        else: 
            self.viikko += 1
            
    def setSeuraavaKuukausi(self):
        if (self.kuukausi == 12):
            self.kuukausi = 1
            self.vuosi += 1
        else:
            self.kuukausi += 1
            
    def setEdellinenKuukausi(self):
        if (self.kuukausi == 1):
            self.kuukausi = 12
            self.vuosi -= 1
        else:
            self.kuukausi -= 1
            
    def setSeuraavaViikonPaiva(self):
        if (self.selectedPaiva == 7):
            self.selectedPaiva = 1
        else: 
            self.selectedPaiva += 1
            
    def setEdellinenViikonPaiva(self):
        if (self.selectedPaiva == 1):
            self.selectedPaiva = 7
        else: 
            self.selectedPaiva -= 1
            
    def increaseX(self):
        if (self.selectedX == self.maxX):
            self.selectedX = 0
        else:
            self.selectedX += 1
    
    def decreaseX(self):
        if (self.selectedX == 0):
            self.selectedX = self.maxX
        else:
            self.selectedX -= 1
    
    def increaseY(self):
        if (self.selectedY == 6):
            self.selectedY = 0
        else:
            self.selectedY += 1
    
    def decreaseY(self):
        if (self.selectedY == 0):
            self.selectedY = 6
        else:
            self.selectedY -= 1
 
    def getPaivaNumero(self, viikonpaiva: int, viikkoNumero: int):
        return str(datetime.date.fromisocalendar(self.vuosi, viikkoNumero, viikonpaiva)).split("-")[2]
    
    # Alkavan viikon kuukausi
    def getKuukausi(self, viikkoNumero:int):
        kuukausiNumero = int(str(datetime.date.fromisocalendar(self.vuosi, viikkoNumero, 1)).split("-")[1])
        return KUUKAUDET[kuukausiNumero]
            
    def kasittelePainallus(self, eventName, mode):
        match eventName:
            case 452: # vasen nuoli
                self.setEdellinenViikko() if mode == "viikko" else self.setEdellinenKuukausi()
            case 454: # oikea nuoli
                self.setSeuraavaViikko() if mode == "viikko" else self.setSeuraavaKuukausi()
            case 450: # ylänuoli
                self.setEdellinenViikonPaiva() 
            case 456: # alanuoli
                self.setSeuraavaViikonPaiva() 
            case 10: # enter
                self.renderUusiMuistutus()
            case 112: # p
                print(f"Poistetaan muistutus {self.vuosi, self.viikko, self.selectedPaiva}")
                self.poistaMuistutus(self.vuosi, self.viikko, self.selectedPaiva + 1)
                self.render()
            case 109: # m
                self.mode = "kuukausi" if self.mode == "viikko" else "viikko"
                self.render()
            case 97: # a
                self.decreaseY() if mode == "kuukausi" else self.setEdellinenViikko()
            case 100: # d 
                self.increaseY() if mode == "kuukausi" else self.setSeuraavaViikko() 
            case 119: # w
                self.decreaseX() if mode == "kuukausi" else self.setEdellinenViikonPaiva()
            case 115: # s
                self.increaseX() if mode == "kuukausi" else self.setSeuraavaViikonPaiva()
            
    def lisaaMuistutus(self, vuosi=None, viikko=None, viikonpaiva=None, paivamaara=None, muistutus: str = None):
        """1.Vaihtoehto vuosi, viikko, viikonpaiva ja muistutus \n
           2.Vaihtoehto paivamaara ja muistutus """
        if paivamaara == None:
            paivamaara = str(datetime.date.fromisocalendar(vuosi, viikko, viikonpaiva))
            self.muistiinPanot[paivamaara] = muistutus
            with open("./muistutukset.json", "w") as f:
                json.dump(self.muistiinPanot, f, indent=4)
        else:
            self.muistiinPanot[paivamaara] = muistutus
            with open("./muistutukset.json", "w") as f:
                json.dump(self.muistiinPanot, f, indent=4)
            
    def poistaMuistutus(self, vuosi, viikko, viikonpaiva):
        paivamaara = str(datetime.date.fromisocalendar(vuosi, viikko, viikonpaiva))
        if (paivamaara not in self.muistiinPanot): return
        self.muistiinPanot.pop(paivamaara)
        with open("./muistutukset.json", "w") as f:
            json.dump(self.muistiinPanot, f, indent=4)
    
    def haeMuistutus(self, vuosi, viikko, viikonpaiva) -> str:
        paivamaara  = str(datetime.date.fromisocalendar(vuosi, viikko, viikonpaiva))
        if (paivamaara in self.muistiinPanot):
            return self.muistiinPanot[paivamaara]
        else:
            return "-"
    
    def haeKuukaudenMuistutukset(self) -> list:
        paivaLukumaara = KUUKAUSIPAIVAT[self.kuukausi]
        muistutukset = []
        for i in range(1, paivaLukumaara + 1):
            paivamaara = str(datetime.date(self.vuosi, self.kuukausi, i))
            if (paivamaara in self.muistiinPanot):
                muistutukset.append({
                    "paiva": int(paivamaara.split("-")[2]),
                    "muistutus": self.muistiinPanot[paivamaara]
                })
                
        return sorted(muistutukset, key=lambda x: x["paiva"])
        
        
        
    # väri viikkonäkymään
    def getViikonPaivaVari(self, viikonpaiva: int):
        if (self.selectedPaiva == viikonpaiva):
            return curses.color_pair(2)
        elif (self.vuosi == self.vuosiTanaan and self.kuukausi == self.kuukausiTanaan and self.viikko == self.viikkoTanaan and self.viikonpaivaTanaan == viikonpaiva):
            return curses.color_pair(5)
        else:
            return curses.color_pair(1)

    # väri kuukausinäkymään
    def getPaivaVari(self, vuosi, kuukausi, paiva):
        pvm = datetime.datetime(vuosi, kuukausi, paiva).strftime("%Y-%m-%d")
        if (pvm in self.muistiinPanot):
            return curses.color_pair(3)
        else:
            return curses.color_pair(1)
        
    def onKarkausVuosi(self, vuosi) -> bool:
        return (vuosi % 4 == 0 and vuosi % 100 != 0) or (vuosi % 400 == 0)
           
def main(stdscr):
    kalenteri = Kalenteri()
    kalenteri.run()
    
curses.wrapper(main)
        
        