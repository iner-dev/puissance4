

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

parms = 

def Normal_map(): # carte de jeu de base
    return [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]

def tabs_multiply(tab1,tab2): # multiplie les elements de la tab1 par ceux de la tab 2
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

def sigmaoide(tab1): # fait la fonction sigma puis sigmoid
    ret = 0
    for i in tab1:
        ret = i + ret
    ret = 1 / (1 + 5 ** (-((4) / len(tab1)) * ret + 2))
    return ret

def place(player, line, Local_map): #place un pion sur la map
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

def print_map(l_map): # print le format map dans la console
    for o in l_map:
        print(o)

Patern_list = [ # liste des paternes de detections de victoire
    [0,1],
    [1,0],
    [1,1],
    [1,-1],
]

def test_pos(x,y,player,tab): #test une position pour un joueur donné
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

class neurone: # les nerones des ia
    def __init__(self,parametres):
        self.parametres = parametres
    
    def calcul(self,input):
        return(sigmaoide(tabs_multiply(self.parametres,input)))

class IA: # les ia
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

    def compil(self):
        ret = []
        for i in range(len(self.neurones)):
            i = i - 1 
            ret.append([])
            for o in self.neurones[i]:
                ret[i].append(o.parametres)
        return ret

def map_to_ia(map): #transforme le format map : [[1,2],[3,4]] au format ia input : [1,2,3,4]
    ret = []
    for i in map :
        for o in i:
            ret.append(o)
    return ret

def read_log(log,type = "Normal"): # lis les log d'une partie
    local_map = Normal_map()
    joueur = 0
    tours = 0
    for i in log:
        joueur = joueur + 1
        if joueur % 2 == 1 :
            win = 1
            place(1,i,local_map)
            tours = tours + 1
        else:
            win = 2
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
    return [win,tours,log]


    with open("save.py", "w") as f:
        f.write(str(liste))

    with open("save.py", "r") as f:
        save = f.read()
        if not save: # save format is [[train evolve,time por mill],IA parms]
            save = [[1,7],[randparms(42,[30,20,10,5,3],1),randparms(42,[30,20,10,5,3],1),randparms(42,[30,20,10,5,3],1),randparms(42,[30,20,10,5,3],1),randparms(42,[30,20,10,5,3],1)]]
        else:
            save = eval(save)
    return save

def afiche(type,donnes=None): # afiche un element graphique
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

def mass_print(text):  # permet d'ecrire plein de choses
    for i in text : print(i) 

def select(map): # permet de choisir au joueur ou vas t'il placer
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

def Normal_party(type,map,ia = None): # execute une partie contre une ia ou en PVP
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

def main(): # menu principale
    mass_print([
        "---------------------",
        "     puissance 4",
        "      by Iner",
        "---------------------"
    ])
    mass_print([
        "1 - PVP",
        "2 - PVE",
        "---------------------"
    ])
    rep2 = input("> ")
    rep_type = {
        1 : "PVP",
        2 : "PVE"
    }
    Normal_party(rep_type.get(rep2),Normal_map(),IA(parms))

main()