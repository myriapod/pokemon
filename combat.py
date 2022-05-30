import random
import gestion_bdd as bdd
import copy
import re


class Pokemon ():
    def __init__(self, player, pokemon): # player = 1 ou 2, pokemon vient de sa liste de pokemons prise dans la bdd
        self.nom=pokebdd.get_name(player, pokemon) # récupère le nom français
        self.id=pokebdd.get_id(player,pokemon)
        self.type=pokebdd.get_type(player,pokemon)  # Attention type est une liste dans un dictionnaire (pokedex) qu'il faudra parcourir 
        self.base=pokebdd.get_base(player,pokemon) # Attention base est un dictionnaire dans un dictionnaire (pokedex) il faudra utilisé la clé
        self.faiblesses=pokebdd.get_faiblesses(player,pokemon) # Une liste avec toutes les faiblesses pour chaque type
        
        self.choisi=False # si c'est le pokemon qui combat ou non

    
    # Méthode qui vérifie si le pokemon au combat n'est pas ko : 
    def verif_ko (self): 
        if self.base["HP"] < 0 : 
            return False
        return True




class Dresseur (): 
    def __init__(self, joueur, liste_pokemons): # joueur = 1 ou 2, liste_pokemons obtenue avec bdd
        
        self.nom=list(liste_pokemons.values())[joueur-1][0] # nom du joueur
        
        temp=copy.deepcopy(list(liste_pokemons.values())[joueur-1])
        self.list_pokemon=temp[1:] # liste des objets Pokemon du joueur

        self.liste_pokemon_accessible = self.list_pokemon.copy() # la liste des pokemons aptes au combat

        self.starter_pokemon = random.choice(self.list_pokemon) # on choisi le pokemon qui commence au hasard
        self.starter_pokemon.choisi = True
            

    def essayer_de_fuir(self): 
        # une chance sur 4 de s'enfuir
        ra=random.randrange(100)
        if ra < 25 : 
            return True
        else:
            print("Fuite ratée")
            return False


    def pokemon_pas_ok(self): # modifie la liste des pokemons accessible
        for pokemon in self.liste_pokemon_accessible:
            if pokemon.verif_ko() == False: # si le pokemon est ko on l'enlève
                self.liste_pokemon_accessible.remove(pokemon)
                pokemon.choisi = False

            elif pokemon.choisi == True:
                if len(self.liste_pokemon_accessible) > 1: # s'il reste plus que un pokemon accessible, on enlève le pokemon actuellement choisi
                    self.liste_pokemon_accessible.remove(pokemon)
                    pokemon.choisi = False
                else: # sinon il est impossible de changer
                    print("Impossible de changer de pokemon, il ne vous en reste plus qu'un.")
        
        # on met la liste des pokemons accessbile à true
        for pokemon in self.liste_pokemon_accessible:
            pokemon.choisi = True
            
        


class Combat(): 

    def __init__(self, joueur1, joueur2): # joueur1 et joueur2 sont des objets dresseurs
        self.depart=True
        self.tours = 0 # pour compter le nombre de tours
        
        self.joueur1=joueur1
        self.joueur2=joueur2
        
        # par défaut le joueur 1 joue en premier, self.depart changera si le speed du pokemon du joueur2 est meilleur
        self.ordre_tour=[self.joueur1, self.joueur2]
        
        # au premier tour leur pokemon choisi est leur starter
        self.j1_pokemon_choisi=self.joueur1.starter_pokemon
        self.j2_pokemon_choisi=self.joueur2.starter_pokemon
        
        self.liste_pokemon_choisis=[self.j1_pokemon_choisi, self.j2_pokemon_choisi]

        self.victoire = 0
    
    
    def affichage(self): # affichage des pokemons sur la partie pour chaque joueur
        print("\n--------------------------------")
        print(f'Joueur 1: {self.joueur1.nom}')
        print(f'>> Pokemons de {self.joueur1.nom} :')
        for p in self.joueur1.list_pokemon:
            print(f'{p.nom} - HP: {p.base["HP"]}, TYPE: {p.type}, FAIBLESSES: {p.faiblesses}')
        print(f'>> Pokemon actif: {self.liste_pokemon_choisis[0].nom}, HP: {self.liste_pokemon_choisis[0].base["HP"]}, TYPE: {self.liste_pokemon_choisis[0].type}, FAIBLESSES: {self.liste_pokemon_choisis[0].faiblesses}\n')
        
        print("      ----------------------      ")
        
        print(f'Joueur 2: {self.joueur2.nom}')
        print(f'>> Pokemons de {self.joueur2.nom} :')
        for p in self.joueur2.list_pokemon:
            print(f'{p.nom} - HP: {p.base["HP"]}, TYPE: {p.type}, FAIBLESSES: {p.faiblesses}')
        print(f'>> Pokemon actif: {self.liste_pokemon_choisis[1].nom}, HP: {self.liste_pokemon_choisis[1].base["HP"]}, TYPE: {self.liste_pokemon_choisis[1].type}, FAIBLESSES: {self.liste_pokemon_choisis[1].faiblesses}')
        print("--------------------------------\n")


    # Méthode qui compare les speed des deux pokémons qui vont combattre, le plus rapide commence 
    def qui_commence(self):
        if self.j1_pokemon_choisi.base["Speed"] < self.j2_pokemon_choisi.base["Speed"]:
          	self.depart=False
        
     
    def attaque (self, j):
        pokemon_qui_attaque = self.liste_pokemon_choisis[j]

        if j == 0: # en fonction de qui joue, on définit le pokemon qui défend
        	pokemon_qui_defend = self.liste_pokemon_choisis[1]
        else:
          	pokemon_qui_defend = self.liste_pokemon_choisis[0]
            
        print(f"\nA l'attaque {pokemon_qui_attaque.nom}!\n")
        
        attaque_hp = int(pokemon_qui_attaque.base["Attack"]*0.25) # calcul des dégats de base

        # check s'il y a des faiblesses trouvées
        faiblesse_trouvee = False             
        cherche_faiblesse = True
        while cherche_faiblesse:
            for poke_type in pokemon_qui_attaque.type:
                if poke_type in pokemon_qui_defend.faiblesses:
                    # s'il y a des faiblesses, l'attaque fait autant de dégats que prévu
                    pokemon_qui_defend.base["HP"] -= attaque_hp
                    cherche_faiblesse = False
                    faiblesse_trouvee = True
            cherche_faiblesse = False

        if faiblesse_trouvee == False: # si on ne trouve pas de dégats, l'attaque fait moins mal
            pokemon_qui_defend.base["HP"] -= int(attaque_hp*0.25)
        
        # si le pokemon est mit ko par l'attaque
        if pokemon_qui_defend.verif_ko() == False:
            print(f"{pokemon_qui_defend.nom} est KO !")
            # en fonction du tour, on enlève le pokemon ko de la liste des pokemons accessibles et on fait changer de pokemon
            if j == 0:
                self.ordre_tour[1].liste_pokemon_accessible.remove(pokemon_qui_defend)
                self.changer_de_pokemon(1)
                
            else:
                self.ordre_tour[0].liste_pokemon_accessible.remove(pokemon_qui_defend)
                self.changer_de_pokemon(0)

        # si tous les pokemons sont mis ko par l'attaque alors la liste des pokemons accessibles est vide
        if j == 0:
            if len(self.ordre_tour[1].liste_pokemon_accessible) == 0:
                print("Victoire du joueur 1")
                return 1
        else:
            if len(self.ordre_tour[0].liste_pokemon_accessible) == 0:
                print("Victoire du joueur 2")
                return 2

        return 0
            

    def changer_de_pokemon(self, j):
        # on vérifie de garder que les pokemons ok dans la liste des pokemons accessibles.
        self.ordre_tour[j].pokemon_pas_ok()

        if len(self.ordre_tour[j].liste_pokemon_accessible) == 0:
            print("Impossible de changer de Pokemon !")
        else: # on choisit un pokemon au hasard parmi la liste des pokemons accessbiles
            self.liste_pokemon_choisis[j]=random.choice(self.ordre_tour[j].liste_pokemon_accessible)

        # on met à choisi = False les autres pokemons
        for pokemon in self.ordre_tour[j].list_pokemon:
            if pokemon != self.liste_pokemon_choisis[j]:
                pokemon.choisi == False
        


    def partie(self): # déroulement de la partie
        self.qui_commence() # on définit qui commence par rapport à leur vitesse
        
        if self.depart == True : # on initialise les indices de tour
            j=0
        else : 
            j=1
        
        while True:
            print(f'>>>> Tour {self.tours+1} <<<<')
            self.affichage() # on affiche les pokemons des deux joueurs
            print("Dresseur", self.ordre_tour[j].nom,"que souhaitez-vous faire ?")
            print("1) Attaquer")
            print("2) Changer de pokémon")
            print("3) Essayer de fuir le combat")
            choix=int(input("Rentrez votre choix: "))

            if choix == 1 : 
                self.victoire = self.attaque(j)

                # si l'attaque est celle qui fait gagner
                if self.victoire == 1: # le joueur 1 gagne sur le joueur 2
                    pokebdd.victoire(1, 2)
                    self.fin_de_la_partie()
                    break

                elif self.victoire == 2: # le joueur 2 gagne sur le joueur 1
                    pokebdd.victoire(2, 1)
                    self.fin_de_la_partie()
                    break

            elif choix == 2 : 
                self.changer_de_pokemon(j)

            elif choix == 3 : 
                if self.ordre_tour[j].essayer_de_fuir() == True : 
                    print("Fuite réussie, le combat est terminé !")
                    self.victoire = -1
                    self.fin_de_la_partie()
                    break
            
            # on change le tour
            if j==0:
              j=1
            else:
              j=0

            self.tours += 1
    


    def fin_de_la_partie(self):
        # gestion de la fin de la partie et affichage de fin
        print("\n############ Fin de la partie #############")
        print(f"La partie a durée {self.tours} tours.")

        if self.victoire > 0:
            print(f"Le gagnant est le joueur {self.victoire}, {self.ordre_tour[1].nom}")
        elif self.victoire < 0:
            print(f"Le combat s'est terminé en une fuite du joueur {self.ordre_tour[1].nom}")

        print("\nVoulez-vous enregistrer les résultats des joueurs?")
        j1 = input("Pour le joueur 1: (oui/non)")
        j2 = input("Pour le joueur 2: (oui/non)")

        # initialisation du conteur pour savoir quel(s) joueur(s) sont réinitialisés
        reset = 0

        if re.match('(?i)oui|o|yes|y', j1):
            pokebdd.save_player(1)
            print("Les résultats du joueur1 ont été sauvegardés dans la bdd.")
        else: # si on rentre autre chose que oui, on supprime le joueur
            reset = 1

        if re.match('(?i)oui|o|yes|y', j2):
            pokebdd.save_player(2)
            print("Les résultats du joueur2 ont été sauvegardés dans la bdd.")
        else: # si on rentre autre chose que oui, on supprime le joueur
            reset += 2

        # en fonction de la valeur du reset, on supprime les lignes qu'il faut dans la bdd
        if reset == 3:
            pokebdd.suppr(1)
            pokebdd.suppr(1)
        elif reset == 1:
            pokebdd.suppr(1)
        elif reset == 2:
            pokebdd.suppr(2)

        





    
#################################### main #####################################


# intialisation de la BDD
pokebdd = bdd.BDD('bdd.json')
    
# Initialisation des pokemons et ajout des joueurs
joueur1 = 1
joueur2 = 1
while joueur1 == joueur2:
    print("Entrez les noms des joueurs (ils doivent être différents) :")
    joueur1 = input("Joueur 1: ")
    joueur2 = input("Joueur 2: ")

pokebdd.debut_de_la_partie(joueur1, joueur2)

# on peut manuellement reset la partie si besoin
# pokebdd.reset = True

# création de la liste des pokemons (si un joueur existe déjà dans la bdd, on ne va pas lui créer de nouveaux pokemons)
liste_pokemons = {1:[joueur1], 2:[joueur2]}
for joueur in range(1,3): # de 1 à 2
    for pokemon in range(1,len(pokebdd.data[joueur-1])): # on commence à 1 car 1 c'est "player":joueur[1 à 2]
        name = "pokemon"+str(pokemon)
        poke_name = Pokemon(joueur, name)
        liste_pokemons[joueur].append(poke_name)
        # liste_pokemons est un dictionnaire de la forme:
        # { joueur1: [{pokemon1}, {pokemon2}, {pokemon3}], joueur2: [ {pokemon1}, {pokemon2}, {pokemon3} ]}

# création des objets dresseur à partir de leur liste de pokemons
joueur1 = Dresseur(1, liste_pokemons)
joueur2 = Dresseur(2, liste_pokemons)

# initiation du combat
combat = Combat(joueur1, joueur2)
# début de la partie
combat.partie()
