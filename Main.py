# for i in range(10000):
#     print(f"{i}", end="\r")
import calendar;
import datetime;
import keyboard;
import curses;

cal = calendar.TextCalendar(calendar.SUNDAY)

# vasen nuoli
# ylänuoli
# oikea nuoli
# alanuoli
    
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

class Calendar():
    def __init__(self):
        
        self.stdscr = curses.initscr()
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        
        self.vuosi = datetime.date.today().isocalendar()[0]
        self.kuukausi = datetime.date.today().month
        self.viikko = datetime.date.today().isocalendar()[1]
        self.viikonpaiva = datetime.date.today().isocalendar()[2]
        self.paiva = datetime.date.today().day
        
        self.mode = "viikko" # viikko tai kuukausi
        
        self.selectedPaiva = 1
        
        self.render()
        
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.kasittelePainallus(event.name, self.mode)
                self.render()
                
    def render(self):
        
            
        
            self.stdscr.addstr(1, 0, f"{self.vuosi} Viikko {self.viikko}")
            self.stdscr.addstr(2, 0, "Maanantai", None)
            self.stdscr.addstr(3, 0, "Tiistai")
            self.stdscr.addstr(4, 0, "Keskiviikko")
            self.stdscr.addstr(5, 0, "Torstai")
            self.stdscr.addstr(6, 0, "Perjantai")
            self.stdscr.addstr(7, 0, "Lauantai")
            self.stdscr.addstr(8, 0, "Sunnuntai")
            
            self.stdscr.refresh()
           
    def setEdellinenViikko(self):
        if (self.viikko == 1):
            self.viikko = 52
        else: 
            self.viikko -= 1
            
    def setSeuraavaViikko(self):
        if (self.viikko == 52):
            self.viikko = 1
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
            
            
    def kasittelePainallus(self, eventName, mode):
        match eventName:
            case "vasen nuoli":
                self.setEdellinenViikko() if mode == "viikko" else self.setEdellinenKuukausi()
            case "oikea nuoli":
                self.setSeuraavaViikko() if mode == "viikko" else self.setSeuraavaKuukausi()
            
    def getViikonPaivaVari(self):
        if ()
           
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
            
    
           

cal = Calendar()
        
        