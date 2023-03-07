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
        for b in range(inputs):
            ret[0][b-1].append(rd.random())
    for a in range(len(shema[0:])):
        ret.append([])
        for b in range(shema[a]):
            ret[a].append([])
            for c in range(shema[a]):
                ret[a][b-1].append(rd.random())
    return ret
    
    

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


x = [
    [
     [0.6777980373282536, 0.2923926191547276, 0.9225279491060656, 0.788280734910441, 0.7425638851376677, 0.643867096718091, 0.7825596737373496], 
     [0.5799543031473333, 0.9927523627598179, 0.7994746924851498, 0.5286339224658078], 
     [0.3737853631449374], 
     [0.003161661016414241, 0.8199266660485346, 0.9542211104620457], 
     [], 
     []
    ],[
     [0.8084921372634503, 0.9455080105580985, 0.09372713407608235, 0.8910759093640697, 0.28263868699760364, 0.9768943848084133], 
     [0.03141203999861164, 0.9530118077655403, 0.45402049971263814], 
     []
    ],[
     [0.4133280839846123, 0.4227781785902808, 0.8177121105201011, 0.8184489069208591, 0.9299930863791673, 0.8661186878194075], 
     [0.1267709985381552, 0.445099673935628, 0.7506557975383288], 
     []
    ],[    
    ]
    ]

print(randparms(2,[3,3,3]))