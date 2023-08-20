import random as rd
import time as t
import P4
import parametres

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

def randparms(inputs, shema, out): # genere les parametres aleatoire d'une ia
    ret = []
    
    # Ajouter la première couche de poids
    ret.append([[rd.random() for _ in range(inputs)] for _ in range(shema[0])])
    
    # Ajouter les couches de poids suivantes
    for i in range(1, len(shema)):
        ret.append([[rd.random() for _ in range(shema[i-1])] for _ in range(shema[i])])
    
    # Ajouter les couches de poids finale
    ret.append([[rd.random() for _ in range(shema[i-2])] for _ in range(out)])
        
    return ret

class neurone: # les nerones des ia
    def __init__(self,parametres):
        self.parametres = parametres
    
    def calcul(self,input):
        return(sigmaoide(tabs_multiply(self.parametres,input)))
    
    def variation(self,Coef):
        for i in range(len(self.parametres)):
            self.parametres[i-1] = self.parametres[i-1] + ((rd.random()-0.5)*Coef*2)

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
        return (save[len(save)-1])
    
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

def getcoup(proba):
    Max = 0
    ret = 0
    for i in range(len(proba)):
        if Max < proba[i]: 
            Max = proba[i]
            ret = i + 1
    return ret

def map_to_ia(map): #transforme le format map : [[1,2],[3,4]] au format ia input : [1,2,3,4]
    ret = []
    for i in map :
        for o in i:
            ret.append(o)
    return ret

def party_training(p1,p2,map): # une partie d"entrainement
    local_map = list(map)
    log = []
    turns = 0
    while True:
        coup = getcoup(p1.calcul(map_to_ia(local_map)))
        if coup == 7 : coup = 6
        log.append(coup)
        pos = P4.place(1,coup,local_map)
        if P4.test_pos(pos[0],pos[1],1,local_map): 
            break

        coup = getcoup(p2.calcul(map_to_ia(local_map)))
        if coup == 7 : coup = 6
        log.append(coup)
        pos = P4.place(2,coup,local_map)
        if P4.test_pos(pos[0],pos[1],2,local_map) : break

        turns = turns + 2

        if turns >= 42 :
            break
        
    return log

def setsave(liste): #fait une sauvegarde
    with open("save.py", "w") as f:
        f.write(str(liste))

def getsave(): #recupere la sauvegarde ou en crée une nouvelle 
    with open("save.py", "r") as f:
        save = f.read()
        if not save: # save format is [[train evolve,time por mill],IA parms]
            save = [[1,10],[randparms(42,[30,20,10,5,3],7),randparms(42,[30,20,10,5,3],7),randparms(42,[30,20,10,5,3],7),randparms(42,[30,20,10,5,3],7),randparms(42,[30,20,10,5,3],7)]]
        else:
            save = eval(save)
    return save

def train(iteration,deep = 200,readlog_see = "None"): # une sequance d'entrainement
    time_por_mill = getsave()[0][1]
    for i in range(iteration):
        start_time = t.time()
        save = getsave()
        variantes = [] # [[l'ia variante,log lu,autres donnes -> [la palace de l'ia mere]],...]
        coef = 1/save[0][0]
        modif = save[0][0]
        if readlog_see != "None" and parametres.executed_on == "PC" : 
            print("iteration =",i+1) 
            print(100*i/iteration,"%")
        if parametres.executed_on == "NumWorks" and readlog_see == "/100" :P4.afiche("/100",[i/iteration])
        time_remain = (iteration-i)*deep*time_por_mill/1000
        if readlog_see != "None" and parametres.executed_on == "PC" : 
            print("time remain =",int(time_remain/3600),"h",int(time_remain/60)%60,"and",int(time_remain)%60,"S") 
            print("---------------------")
        for o in range(4):
            variantes.append(IA(save[1][o]))
            for p in range(int(deep/5)):
                p = p + 1
                variantes.append(variantes[o])
                variantes[o+p].variation(coef)
        champion = []
        for o in variantes:
            win = 0
            points = 0
            for p in range(9):
                try:
                    place = rd.randint(1,10)
                    if place == 1:
                        ret =  P4.read_log(party_training(o,variantes[rd.randint(0,len(variantes)-1)],P4.Normal_map()),readlog_see)
                    else : 
                        ret =  P4.read_log(party_training(variantes[rd.randint(0,len(variantes)-1)],o,P4.Normal_map()),readlog_see)
                    points = points + ret[1]
                    if ret[0]==place:
                        win = win + 1
                except:
                    win = win
            used = False
            for Q in range(len(champion)):
                Q = Q - 1
                if champion[Q][1] > win or champion[Q][2] < points:
                    champion.insert(Q-1,[o,win,points])
                    used = True
                    break
            if used == False:
                champion.insert(0,[o,win,points])
        modif = modif +1
        time_por_mill = (time_por_mill+t.time()-start_time)/2
        setsave([[modif,time_por_mill],[champion[0][0].compil(),champion[1][0].compil(),champion[2][0].compil(),champion[3][0].compil(),champion[4][0].compil()]])

def mass_print(text):  # permet d'ecrire plein de choses
    for i in text : print(i) 
