import random as rd
import time as t

# PC / NumWorks
executed_on = "PC"

#     puissance 4
#      by Iner

#       ____  
#      /    \ 
#      \-73-/ 
#       \78/  
#        --   
#       /69\  
#      /-82-\ 
#      \____/ 


def Normal_map():
    return [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]

def tabs_multiply(tab1,tab2):
    ret = []
    if type(tab1) == int :
        tab1 = [tab1]
    if type(tab2) == int :
        tab2 = [tab2]
    if len(tab1)>len(tab2):
        while len(tab1)>len(tab2):
            tab2 = tab2 + tab2
    for i in range(len(tab1)):
        ret.append(tab1[i]*tab2[i])
    return ret

def sigmaoide(tab1):
    ret = 0
    for i in tab1:
        ret = i + ret
    ret = 1 / (1 + 5 ** (-((4) / len(tab1)) * ret + 2))
    return ret

def randparms(inputs, shema, out):
    ret = []
    
    # Ajouter la première couche de poids
    ret.append([[rd.random() for _ in range(inputs)] for _ in range(shema[0])])
    
    # Ajouter les couches de poids suivantes
    for i in range(1, len(shema)):
        ret.append([[rd.random() for _ in range(shema[i-1])] for _ in range(shema[i])])
    
    # Ajouter les couches de poids finale
    for i in range(i, i + out):
        ret.append([[rd.random() for _ in range(shema[i-1])] for _ in range(out)])
        
    return ret

def place(player, line, Local_map):
    y = len(Local_map) - 1  # -1 car les indices commencent à 0
    while y >= 0 and Local_map[y][line] != 0:  # Vérifier que y est dans les limites de map
        y = y - 1
        if y < 0:
            line = line + 1
            y = len(Local_map) - 1
            if line >= len(Local_map[0]):
                line = 0
    if y >= 0:  # Si y est valide, mettre à jour la valeur de la liste
        Local_map[y][line] = player
        return [line,y]

Patern_list = [
    [0,1],
    [1,0],
    [1,1],
    [1,-1],
]

def test_pos(x,y,player,tab):
    ret = False
    for i in range(4):
        patern = Patern_list[i]
        tx = x 
        ty = y
        another = True
        num = 0
        while another == True and tx >= 0 and tx <= (len(tab[0])-1) and ty >= 0 and ty <= (len(tab)-1):
            if tab[ty][tx] == player:
                num = num + 1
                ty = ty + patern[0]
                tx = tx + patern[1]
            else:
                another = False
        another = True
        tx = x 
        ty = y 
        while another == True and tx >= 0 and tx <= (len(tab[0])-1) and ty >= 0 and ty <= (len(tab)-1):
            if tab[ty][tx] == player:
                num = num + 1
                ty = ty - patern[0]
                tx = tx - patern[1]
            else:
                another = False
        num = num - 1
        if num >= 4 :
            ret = True
    
    return ret

class neurone:
    def __init__(self,parametres):
        self.parametres = parametres
    
    def calcul(self,input):
        return(sigmaoide(tabs_multiply(self.parametres,input)))
    
    def variation(self,Coef):
        for i in range(len(self.parametres)):
            self.parametres[i-1] = self.parametres[i-1] + ((rd.random()-0.5)*Coef*2)

class IA:
    def __init__(self,parametres):
        self.neurones = [] 
        for i in range(len(parametres)):
            self.neurones.append([])
            for o in range(len(parametres[i])):
                neu = parametres[i][o]
                self.neurones[i].append(neurone(neu))
    
    def calcul(self,input):
        save = [input]
        for a in range(len(self.neurones)-1):
            save.append([])
            for b in range(len(self.neurones[a])):
                save[a+1].append(self.neurones[a][b].calcul(save[a]))
        return (save[len(save)-1][0])
    
    def variation(self,coef):
        for i in self.neurones : 
            for o in i :
                o.variation(coef)

    def compil(self):
        ret = []
        for i in range(len(self.neurones)):
            i = i - 1 
            ret.append([])
            for o in self.neurones[i]:
                ret[i].append(o.parametres)
        return ret

def map_to_ia(map):
    ret = []
    for i in map :
        for o in i:
            ret.append(o)
    return ret

def party_training(p1,p2,map):
    local_map = list(map)
    win = 0
    log = []
    turns = 0
    while win == 0:
        coup = int(p1.calcul(map_to_ia(local_map))*7)
        if coup == 7 : coup = 6
        log.append(coup)
        pos = place(1,coup,local_map)
        if test_pos(pos[0],pos[1],1,local_map): 
            win = 1 
            break

        coup = int(p2.calcul(map_to_ia(local_map))*7)
        if coup == 7 : coup = 6
        log.append(coup)
        pos = place(2,coup,local_map)
        if test_pos(pos[0],pos[1],2,local_map) : win = 2

        turns = turns + 2

        if turns >= 42 :
            win = None
            break
        
    return [win,log]

def print_map(l_map):
    for o in l_map:
        print(o)

def read_log(log,type = "Normal"):
    local_map = Normal_map()
    joueur = 0
    tours = 0
    for i in log[1]:
        joueur = joueur + 1
        if joueur % 2 == 1 :
            place(1,i,local_map)
            tours = tours + 1
        else:
            place(2,i,local_map)
        if type == "Normal":
            print("-------------------")
            print_map(local_map)
    if type == "Normal" or type == "minimal" or type == "DT":
        print("-------------------")
        print("J",log[0],"win at",tours,"turns")
        if type == "DT":
            print(log)
        print("-------------------")
    return [log[0],tours,log[1]]

def setsave(liste):
    with open("save.py", "w") as f:
        f.write(str(liste))

def getsave():
    with open("save.py", "r") as f:
        save = f.read()
        if not save: # save format is [[train evolve,time por mill],IA parms]
            save = [[1,7],randparms(42,[30,20,10,5,3],1)]
        else:
            save = eval(save)
    return save

def afiche(type,donnes=None):
    import kandinsky as ky
    if type == "/100":
        ky.fill_rect(10,10,300,100,ky.color(0,0,0))
        ky.fill_rect(12,12,int(donnes[0]*296),96,ky.color(255-int(donnes[0]*255),int(donnes[0]*255),0))
    elif type == "map":
        ky.fill_rect(49,19,210,180,ky.color(0,0,0))
        for i in range(len(donnes[0])):
            for o in range(len(donnes[0][i])):
                color_tab = {
                    0 : ky.color(255,255,255),
                    1 : ky.color(0,255,0),
                    2 : ky.color(0,0,255)
                }
                ky.fill_rect(o*30+50,i*30+20,28,28,color_tab.get(donnes[0][i][o]))
    elif type == "curseur":
        ky.fill_rect(50,5,210,10,ky.color(255,255,255))
        ky.fill_rect(donnes[0]*30+30,5,10,10,ky.color(0,0,0))

def train(iteration,deep = 1000,readlog_see = "None"):
    time_por_mill = save[0][1]
    start_time = int(t.time())
    for i in range(iteration):
        save = getsave()
        ia = IA(save[1])
        variantes = [] # [[l'ia variante,log lu,autres donnes -> [la palace de l'ia mere]],...]
        tours = 43
        id = -1
        coef = 1/save[0][0]
        modif = save[0][0]
        if readlog_see != "None" and executed_on == "PC" : print("iteration =",i+1)
        if readlog_see == "/100" and executed_on == "PC" : print(100*i/iteration,"%")
        if executed_on == "NumWorks" and readlog_see == "/100" :afiche("/100",[i/iteration])
        time_remain = (iteration-i)*deep*time_por_mill/1000
        if readlog_see == "/100" and executed_on == "PC" : print("time remain =",int(time_remain/3600),"h",int(time_remain/60)%60,"and",int(time_remain)%60,"S")
        if readlog_see != "None" and executed_on == "PC" : print("---------------------")
        for o in range(deep):
            o = o - 1
            variantes.append([IA(save[1])])
            variantes[o][0].variation(coef)
            if rd.random() >= 0.5:
                result = party_training(ia,variantes[o][0],Normal_map())
                iap = 1
            else :
                result = party_training(variantes[o][0],ia,Normal_map())
                iap = 2
            variantes[o].append(read_log(result,readlog_see))
            variantes[o].append([iap])

            if variantes[o][1][1] < tours:
                tours = variantes[o][1][1]
                if variantes[o][1][0] != None :
                    id = o
        if id == -1 or variantes[id][1][0] == variantes[id][2][0] :
            selected = ia
        else :
            selected = variantes[id][0]
            modif = modif + 1
        time_por_mill = (int(t.time())-start_time())/iteration
        setsave([[modif,time_por_mill],selected.compil()])
        if id != -1 and readlog_see == "Best":
            read_log([variantes[id][1][0],variantes[id][1][2]])

def mass_print(text):
    for i in text : print(i) 

def select(map):
    import ion
    end = False
    ret = 7
    while end == False:
        afiche("map",[map])
        afiche("curseur",[ret])
        while True :
            if ion.keydown(ion.KEY_LEFT):
                ret = ret - 1
                if ret < 1 : ret = 7
                while ion.keydown(ion.KEY_LEFT): 
                    jsp = 1
                break
            elif ion.keydown(ion.KEY_RIGHT):
                ret = ret + 1
                if ret > 7 : ret = 1
                while ion.keydown(ion.KEY_RIGHT):
                    jsp = 1
                break
            elif ion.keydown(ion.KEY_OK):
                if ret > 7 : ret = 1
                while ion.keydown(ion.KEY_OK):
                    jsp = 1
                end = True
                break
    return ret

def Normal_party(type,map,ia = None):
    local_map = list(map)
    win = 0
    log = []
    turns = 0
    while win == 0:
        coup = select(local_map)
        coup = coup - 1
        if coup > 6 : coup = 6
        if coup < 0 : coup = 0
        log.append(coup)
        pos = place(1,coup,local_map)
        if test_pos(pos[0],pos[1],1,local_map): 
            win = 1 
            break

        if type == "PVP":
            coup = select(local_map)
            coup = coup - 1
            if coup > 6 : coup = 6
            if coup < 0 : coup = 0
        else:
            coup = int(ia.calcul(map_to_ia(local_map))*7)
            if coup == 7 : coup = 6
        log.append(coup)
        pos = place(2,coup,local_map)
        if test_pos(pos[0],pos[1],2,local_map) : win = 2

        turns = turns + 2

        if turns >= 42 :
            win = None
            break
    end = False
    ret = 7
    while end == False:
        afiche("map",[map])
        import ion
        while True :
            if ion.keydown(ion.KEY_OK):
                if ret > 7 : ret = 1
                while ion.keydown(ion.KEY_OK):
                    jsp = 1
                end = True
                break
    return [win,log]

def main():
    mass_print([
        "---------------------",
        "     puissance 4",
        "      by Iner",
        "---------------------",
        "  que veut tu faire",
        "1 - entrainer l'ia",
        "2 - une partie",
        "---------------------"
    ])
    rep1 = eval(input("> "))
    print("---------------------")
    if rep1 == 1 :
        print("et combien d'itérations")
        print("---------------------")
        rep2 = eval(input("> "))
        mass_print([
            "---------------------",
            "quelle type d'afichage",
            "1 - Best",
            "2 - avancement",
            "---------------------",
        ])
        rep3 = eval(input("> "))
        print("---------------------")
        rep_poss = {
            1 : "Best",
            2 : "/100"
        }
        train(rep2,1000,rep_poss.get(rep3))
    else:
        mass_print([
            "0 - PVP",
            "1 - PVE",
            "---------------------"
        ])
        rep2 = input("> ")
        rep_type = {
            1 : "PVP",
            2 : "PVE"
        }
        Normal_party(rep_type.get(rep2),Normal_map())

main()