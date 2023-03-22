import random as rd


map = [
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

def place(player, line, map):
    y = len(map) - 1  # -1 car les indices commencent à 0
    while y >= 0 and map[y][line] != 0:  # Vérifier que y est dans les limites de map
        y = y - 1
        if y < 0:
            line = line + 1
            y = len(map) - 1
            if line >= len(map[0]):
                line = 0
    if y >= 0:  # Si y est valide, mettre à jour la valeur de la liste
        map[y][line] = player

Patern_list = [
    [0,1],
    [1,0],
    [1,1],
    [1,-1],
]

def test_pos(x,y,player,tab):
    for i in range(4):
        patern = Patern_list[i]
        tx = x 
        ty = y
        another = True
        num = 0
        while another == True and tx >= 0 and tx <= len(tab[0]) and ty >= 0 and ty <= len(tab):
            if tab[ty][tx] == player:
                num = num + 1
                ty = ty + patern[0]
                tx = tx + patern[1]
            else:
                another = False
        another = True
        tx = x 
        ty = y 
        while another == True and tx >= 0 and tx <= len(tab[0]) and ty >= 0 and ty <= len(tab):
            if tab[ty][tx] == player:
                num = num + 1
                ty = ty - patern[0]
                tx = tx - patern[1]
            else:
                another = False
        num = num - 1
        return num

class neurone:
    def __init__(self,parametres):
        self.parametres = parametres
    
    def calcul(self,input):
        return(sigmaoide(tabs_multiply(self.parametres,input)))

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
        for a in range(len(self.neurones)):
            save.append([])
            for b in range(len(self.neurones[a])):
                save[a+1].append(self.neurones[a][b].calcul(save[a]))
        return (save[-1][0])

def setsave():
    with open("save.txt", "r") as f:
        save = f.read()
        if not save:
            save = randparms(42,[3,3,3],1)
        else:
            save = eval(save)
    return save

def party(p1,p2):
    if type(p1) == "IA" and type(p2) == "IA":
        
