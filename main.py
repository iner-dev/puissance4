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
    for i in range(len(tab1)):
        ret.append(tab1[i]*tab2[i])
    return ret

def sigmaoide(tab1):
    ret = 0
    for i in tab1:
        ret = i + ret
    ret = 1/(1+5^(-((4)/(len(tab1)))*ret+2))
    return ret

def randparms(inputs,shema):
    ret = [[]]
    for a in range(shema[0]):
        ret[0].append([])
        for a in range(inputs):
            ret[0][a-1].append(rd.random())
    for a in range(len(shema[1:])):
        ret.append([])
        for b in range(shema[a+1]):
            ret[a].append([])
            for c in range(shema[a]):
                ret[a+1,b-1].append(rd.random())
    
    

class neurone:
    def __init__(self,parametres):
        self.parametres = parametres
    
    def calcul(self,input):
        return(sigmaoide(tabs_multiply(self.parametres,input)))

class ia:
    def __init__(self,parametres):
        self.ia = [] 
        for i in range(len(parametres)):
            self.ia.append([])
            for o in range(len(parametres[i])):
                neu = parametres[i][o]
                self.ia[i].append(neurone(neu))




print(randparms(2,[3,3,3]))