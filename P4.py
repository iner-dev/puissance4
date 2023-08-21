import iaf

def Normal_map(): # carte de jeu de base
    return [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]

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

def print_map(l_map): # print le format map dans la console
    for o in l_map:
        print(o)

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

def select(map): # permet de choisir au joueur ou vas t'il placer
    import ion
    end = False
    ret = 42
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
            coup = iaf.getcoup(ia.calcul(iaf.map_to_ia(local_map)))
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
