######################
## class_Pokemon.py ##
######################


# définition de la classe Pokemon
class Pokemon():

    # On initialise les variables
    def __init__(self, name, type, base):

        # Definition des attributs 
        # cf détail BDD à cause des listes de dic et dic ds dic
        self.name = name
        self.type = type
        self.HP = PV
        self.Attack = Attack
        self.Defense = Defense
        self.Sp_attack = Sp_attack
        self.Sp_defense = Sp_defense
        self.Speed = Speed

    # Fonction attaque!
    def attaque(self, Pokemon_2):
        
        # On affiche les informations du combat
        print("##### LE COMBAT COMMENCE! #####")
        print(f"\n{self.name}")
        print("TYPE ", self.type)
        print("PV ", self.HP)
        print("\nVERSUS")
        print(f"\n{Pokemon_2.name}")
        print("TYPE ", Pokemon_2.type)
        print("PV ", Pokemon_2.HP)
        
    # Qui a le Pokemon le plus rapide?
    def joueur_1_rapide(self, pokemon_2):
        if self.Speed > Pokemon_2.Speed:
            return True
        return False
    # variable intermediaire "depart"

    # On détermine qui commence la partie

    # On continue le combat tant qu'il reste des HP au deux Pokemons
        while (self.HP > 0) and (Pokemon_2.HP > 0):
            
            # Tour du premier joueur 
            # Affiche la santé en HP des 2 Pokemons
            print(f"\n{self.name}\t\tHP\t{self.HP}")
            print(f"{Pokemon_2.name}\t\tHP\t{Pokemon_2.HP}\n")

            # On encourage le pépère qui va au charbon
            print(f"A l'attaque {self.name}!")

            # Soustraction des "HP" du pokemon adverse a celle de l'"ATTACK" du pokemon attaquant
            Pokemon_2.HP -= self.Attack
            
            # Considération des avantages et faiblesses
            # si le pokemon attaqué est dans les faiblesses du pokemon attaquant
            # on soustrait "SP.DEFENSE" du pokemon attaqué a l"ATTACK" du pokemon attanquant <= Pas sur de comprendre
            
            # snippet de types.json 
            {"name":"Grass","immunes":[],"weaknesses":["Fire","Grass","Poison","Flying","Bug","Dragon","Steel"],"strengths":["Water","Ground","Rock"]}
            
            # Condition et syntaxe bidon, à bosser:
            if name in types.json weaknesses is True:
            
                pokemon_2.HP -= self.Sp_defense
            
            # Vérifier si le joueur opposant a pris la fuite?

            # Tour du second joueur 
            # Affiche la santé en HP des 2 Pokemons
            print(f"\n{self.name}\t\tHP\t{self.HP}")
            print(f"{Pokemon_2.name}\t\tHP\t{Pokemon_2.HP}\n")