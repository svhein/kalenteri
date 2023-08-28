# for i in range(10000):
#     print(f"{i}", end="\r")
import calendar;
import datetime;
import keyboard;
import curses;
import json;

from curses.textpad import Textbox

cal = calendar.TextCalendar(calendar.SUNDAY)

# vasen nuoli
# ylänuoli
# oikea nuoli
# alanuoli
##
    
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


# VUOSI = datetime.date.today().isocalendar()[0]
# VIIKKO_NUMERO = datetime.date.today().isocalendar()[1]
# VIIKONPAIVA = datetime.date.today().isocalendar()[2]
# PAIVA_NUMERO = datetime.date.today().day

class Kalenteri():
    def __init__(self):
        
        self.stdscr = curses.initscr()
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        
        self.vuosi = datetime.date.today().isocalendar()[0]
        self.kuukausi = datetime.date.today().month
        self.viikko = datetime.date.today().isocalendar()[1]
        self.viikonpaiva = datetime.date.today().isocalendar()[2]
        self.paiva = datetime.date.today().day
        
        self.mode = "viikko" # viikko tai kuukausi    
        self.selectedPaiva = 1
        
        self.kirjoitusPaalla = False
        self.user_input = ""
        
        f = open("./muistutukset.json", "r")
        self.muistiinPanot = json.load(f)
        
        #debug
        self.latestEvent = ""
        self.loop1 = 0
        self.loop2 = 0
        
        self.render()
    
    def run(self):
        
        while True:
            self.loop1 += 1
            key = self.stdscr.getch()
            self.kasittelePainallus(key, self.mode)
            self.render()
                
                
                
        
    # def run(self):
    #     while True:
    #         self.loop1 += 1
    #         event = keyboard.read_event()
    #         if event.event_type == keyboard.KEY_DOWN:
    #             if (self.kirjoitusPaalla == False):
    #                 self.kasittelePainallus(event.name, self.mode)
    #                 if (event.name != "enter" or self.kirjoitusPaalla == False):
    #                     self.render()
    #             # elif (self.kirjoitusPaalla == True):
    #             #     self.kasittelePainallus(event.name, self.mode)
    #             #     self.renderUusiMuistutus()
                    
    def render(self):
        
        self.stdscr.clear()
    
        self.stdscr.addstr(1, 0, f"{self.vuosi} - {self.getKuukausi(self.viikko)} - Viikko {self.viikko}", curses.color_pair(4))
        self.stdscr.addstr(2, 0, f"{self.getPaivaNumero(1, self.viikko)}. Maanantai", self.getViikonPaivaVari(1))
        self.stdscr.addstr(3, 0, f"{self.getPaivaNumero(2, self.viikko)}. Tiistai", self.getViikonPaivaVari(2))
        self.stdscr.addstr(4, 0, f"{self.getPaivaNumero(3, self.viikko)}. Keskiviikko", self.getViikonPaivaVari(3))
        self.stdscr.addstr(5, 0, f"{self.getPaivaNumero(4, self.viikko)}. Torstai", self.getViikonPaivaVari(4))
        self.stdscr.addstr(6, 0, f"{self.getPaivaNumero(5, self.viikko)}. Perjantai", self.getViikonPaivaVari(5))
        self.stdscr.addstr(7, 0, f"{self.getPaivaNumero(6, self.viikko)}. Lauantai", self.getViikonPaivaVari(6))
        self.stdscr.addstr(8, 0, f"{self.getPaivaNumero(7, self.viikko)}. Sunnuntai", self.getViikonPaivaVari(7))
        self.stdscr.addstr(9, 0, f"")
        
        self.stdscr.addstr(2, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 1)}", curses.color_pair(3))
        self.stdscr.addstr(3, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 2)}", curses.color_pair(3))
        self.stdscr.addstr(4, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 3)}", curses.color_pair(3))
        self.stdscr.addstr(5, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 4)}", curses.color_pair(3))
        self.stdscr.addstr(6, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 5)}", curses.color_pair(3))
        self.stdscr.addstr(7, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 6)}", curses.color_pair(3))
        self.stdscr.addstr(8, 25, f"{self.haeMuistutus(self.vuosi, self.viikko, 7)}", curses.color_pair(3))
        
        self.stdscr.addstr(10, 0, f"Latest event {self.latestEvent}", curses.color_pair(4))
        
        self.stdscr.addstr(12, 0, f"Loop one {self.loop1}", curses.color_pair(4))
        self.stdscr.addstr(13, 0, f"Loop two {self.loop2}", curses.color_pair(4))

        self.stdscr.refresh()
            
    def renderUusiMuistutus(self):
        self.stdscr.clear()
        self.kirjoitusPaalla = True
        curses.noecho()
        self.stdscr.addstr(1, 0, f"Lisää uusi muistutus", curses.color_pair(4))
        self.stdscr.addstr(2, 0, f"{str(datetime.date.fromisocalendar(self.vuosi, self.viikko, self.selectedPaiva))}", curses.color_pair(4))
        self.stdscr.addstr(3, 0, f"{self.user_input}", curses.color_pair(4))
        
        self.stdscr.addstr(6, 0, f"Latest event {self.latestEvent}", curses.color_pair(4))

        
        self.stdscr.addstr(9, 0, f"Loop one {self.loop1}", curses.color_pair(4))
        self.stdscr.addstr(10, 0, f"Loop two {self.loop2}", curses.color_pair(4))

        def is_letter(key):
            return ord('a') <= key <= ord('z') or ord('A') <= key <= ord('Z')
        
        self.loop2 += 1
        key = self.stdscr.getch()
        if key == 10:  # enter
            self.kirjoitusPaalla = False
            self.lisaaMuistutus(self.vuosi, self.viikko, self.selectedPaiva, self.user_input)
            self.user_input = ""
            return self.render()
        elif key == 27:  # esq
            self.user_input = ""
        elif key == curses.KEY_BACKSPACE or key == 8 or key == curses.KEY_DC:
            self.user_input = self.user_input[:-1]
        else:
            if (is_letter(key)) or key == 32: 
                # 32 space
                self.user_input += chr(key)
            
        return self.renderUusiMuistutus()    

            
        
        
                
        
        
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
        self.getPaivaNumero()
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
    
    def getPaivaNumero(self, viikonpaiva: int, viikkoNumero: int):
        return str(datetime.date.fromisocalendar(self.vuosi, viikkoNumero, viikonpaiva)).split("-")[2]
    
    # Alkavan viikon kuukausi
    def getKuukausi(self, viikkoNumero:int):
        kuukausiNumero = int(str(datetime.date.fromisocalendar(self.vuosi, viikkoNumero, 1)).split("-")[1])
        return KUUKAUDET[kuukausiNumero]
            
    def kasittelePainallus(self, eventName, mode):
        self.latestEvent = eventName
        match eventName:
            case 452:
                self.setEdellinenViikko() if mode == "viikko" else self.setEdellinenKuukausi()
            case 454:
                self.setSeuraavaViikko() if mode == "viikko" else self.setSeuraavaKuukausi()
            case 450:
                self.setEdellinenViikonPaiva()
            case 456:
                self.setSeuraavaViikonPaiva()
            case 108:
                self.renderUusiMuistutus()
                if (self.mode == "viikko"):
                    # self.lisaaMuistutus(self.vuosi, self.viikko, self.selectedPaiva)
                    pass
            case 112:
                self.poistaMuistutus(self.vuosi, self.viikko, self.selectedPaiva)
                self.render()
                  
    def lisaaMuistutus(self, vuosi, viikko, viikonpaiva, muistutus: str):
        paivamaara = str(datetime.date.fromisocalendar(vuosi, viikko, viikonpaiva))
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
    
    def getViikonPaivaVari(self, viikonpaiva: int):
        if (self.selectedPaiva == viikonpaiva):
            return curses.color_pair(2)
        else:
            return curses.color_pair(1)
        
    def onKarkausVuosi(self, vuosi) -> bool:
        return (vuosi % 4 == 0 and vuosi % 100 != 0) or (vuosi % 400 == 0)
           
    # def setEdellinenViikonPaiva(self):
    #     if (self.viikonpaiva == 1):
    #         self.viikonpaiva = 7
    #     else: 
    #         self.viikonpaiva -= 1
            
    # def setSeuraavaViikonPaiva(self):
    #     if (self.viikonpaiva == 7):
    #         self.viikonpaiva = 1
    #     else: 
    #         self.viikonpaiva += 1
      
    
def main(stdscr):
    kalenteri = Kalenteri()
    kalenteri.run()
    
curses.wrapper(main)
        
        