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

autoboot_parms = {
    "iterations":1000,
    "nb_d'ia":1000,
    "type":"Best"
}

iaf.mass_print([
    "---------------------",
    "     puissance 4",
    "      auto boot ",
    "      by Iner",
    "---------------------",
    "this program is entirely",
    "automatic. did not act",
    "       please",
    "---------------------",
    "the initial settings are",
    f"iterations -> {autoboot_parms.get('''iterations''')}",
    f"number of AI -> {autoboot_parms.get('''nb_d'ia''')}",
    f"type -> {autoboot_parms.get('''type''')}",
    "---------------------",
])

iaf.train(autoboot_parms.get("iterations"),autoboot_parms.get("nb_d'ia"),autoboot_parms.get("type"))