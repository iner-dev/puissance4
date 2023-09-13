import P4
import iaf


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

def main(): # menu principale
    iaf.mass_print([
        "---------------------",
        "     puissance 4",
        "      by Iner",
        "---------------------",
        "  que veut tu faire",
        "1 - entrainer l'ia",
        "2 - une partie",
        "3 - recuperer la save",
        "---------------------"
    ])
    rep1 = eval(input("> "))
    print("---------------------")
    if rep1 == 1 :
        print("et combien d'itérations")
        print("---------------------")
        rep2 = eval(input("> "))
        iaf.mass_print([
            "---------------------",
            "quelle type d'afichage",
            "1 - Best",
            "2 - avancement",
            "3 - DT",
            "---------------------",
        ])
        rep3 = eval(input("> "))
        print("---------------------")
        rep_poss = {
            1 : "Best",
            2 : "/100",
            3 : "DT"
        }
        iaf.train(rep2,1000,rep_poss.get(rep3))
    elif rep1 == 2 :
        iaf.mass_print([
            "1 - PVP",
            "2 - PVE",
            "---------------------"
        ])
        rep2 = int(input("> "))
        rep_type = {
            1 : "PVP",
            2 : "PVE"
        }
        P4.Normal_party(rep_type.get(rep2),P4.Normal_map(), iaf.IA( iaf.getsave()[1][1]))
    else : 
        print(iaf.getsave()[1][1])

main()