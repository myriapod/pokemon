from random import randrange


# EXEMPLE BDD pokémon 
# {
#     "id": 26,
#     "name": [
#       "french": "Raichu"
#     ],
#     "type": [
#       "Electric"
#     ],
#     "base": {
#       "HP": 60,
#       "Attack": 90,
#       "Defense": 55,
#       "Sp. Attack": 90,
#       "Sp. Defense": 80,
#       "Speed": 110
#     }
# } 



class Dresseur (): 

    #nom, liste de pokemon=pokédex, pokémon au combat, liste de pokemon KO
    def __init__(self, dresseur, pokedex, pokemon, pokemon_ko ):
        self.nom=dresseur
        self.pokedex=pokedex # c'est un dictionnaire copié à partir de la BBD des pokémon  
        self.pokemon=Pokemon.name # pokémon actif au combat 
        self.ko=pokemon_ko # c'est un dictionnaire
        self.fuite=False 
 

    # Méthode de tirage aléatoire des 3 pokémons dans la BDD qui constitueront le pokédex 


    # Méthode tirage aléatioire du pokémon qui partira au combat 


    # Méthode changement de Pokémon (à finir)
    def change (): 
        print("changement de pokémon")
        #changement du pokémon actif (Pokemon.name)

    # Méthode essai de fuite du dresseur 
    def essayer_de_fuir (self): 
        ra=randrange(100)
        if ra < 25 : 
            self.fuite = True 
        else : 
            self.fuite = False 
    


class Pokemon ():

    # Caractéristique du pokémon 
    def __init__(self,id, name, type, base):
        self.name=name
        self.id=id 
        self.type=type  # Attention type est une liste dans un dictionnaire (pokedex) qu'il faudra parcourir 
        self.base=base # Attention base est un dictionnaire dans un dictionnaire (pokedex) il faudra utilisé la clé
        self.combat=True 


    # Méthode attaque (prendre en compte son type et le type de l'adversaire)
    # Si le type du pokemon attaqué et dans les faiblesses du pokemon attaquant, on applique la resolution des dégats avec "Sp. ATTACK"
    def attaque (): 
        print("attaque") # en attendant de faire cette méthode 


    # Méthode ko : 
    def ko (self, base): 
        if base ["HP"] <= 0 : 
            self.combat=False 
            Dresseur.change 

    

class Combat(): 

    # def __init__(self):
    #     self.dresseurs= [liste des dresseurs]
        

    # Méthode qui compare les speed des deux pokémons qui vont combattre, le plus rapide commence 
    # def qui_commence (): 
       

    # Méthode déroulement partie 
    def partie (dresseur): 
        # print affichage caractérisique du pokémon qui combat et celui de l'adversaire 
        print("Dresseur", dresseur,"que souhaitez-vous faire ?")
        print("1) Attaquer")
        print("2) Changer de pokémon")
        print("3) Essayer de fuir le combat")
        choix=input()
        if choix == 1 : 
            Pokemon.attaque 
        elif choix == 2 : 
            Dresseur.change
        elif choix == 3 : 
            Dresseur.fuite 
        else :
            print("Saisie erronée") 
            Combat.partie 
        # affichage résultat 

    # Méthode affichage vainqueur : annonce du vainqueur de la partie changement dictionnaire perdant perd tous ses pokémons

        



