import json
import random
import copy


class BDD():
    
    def __init__(self, bdd_file):
        self.file_path = bdd_file # on demande en paramètre le chemin vers le fichier bdd pour être le plus souple possible
        self.reset = True # par défaut on réinitialise la bdd à la fin d'une partie

        with open(self.file_path, 'r') as f:
            try: # initialise la bdd en l'ouvrant
                self.data = json.load(f).copy()
            except json.decoder.JSONDecodeError: # si le fichier est vide, on initialise data à une liste vide
                self.data = []

        
        with open('pokedex.json', 'r') as f:
            # récupérer le pokedex https://github.com/fanzeyi/pokemon.json/blob/master/pokedex.json
            self.pokedex = json.load(f) # pokedex est une liste de dictionnaire, 1 pokemon par dictionnaire
            

        with open('types.json', 'r') as f:
            # récuperer les types
            self.types = json.load(f).copy() # types est une liste de dictionnaire contenant tous les types et leurs faiblesses
    

    # mise à jour de la bdd (écriture dans le fichier .json)
    def update(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f) # on ecrit self.data dans bdd.json



    def affichage(self, player=False):
        # affiche la bdd dans le terminal:
        # - toute la bdd
        # - player=1 ou player=2 pour un joueur en particulier
        if player != False:
            for key in self.data[int(player-1)]:
                print(key, " - ", self.data[int(player-1)][key])
        else:
            for entry in self.data:
                print('\n')
                for key in entry:
                    print(key, " - ", entry[key])

    
    
    def suppr(self, player):
        # supprimer un joueur 1 ou 2 de la bdd (par rapport à leur position dans la liste des dictionnaires de la bdd)
        # player = 1 ou 2
        self.data.pop(player-1)


    def reset_bdd(self): # reset total de la bdd
        self.reset = True
        while len(self.data) != 0:
            self.suppr(1)

    
    def modifier(self, player, pokemon, change, field, subfield=False):
        # modifie un élément de la bdd
        # player = 1 ou 2
        # pokemon = pokemon[i]
        # change = nouvelle valeur
        # field = key, subfield = key de la key si besoin

        if subfield != False:
            self.data[player-1][pokemon][field].update({subfield:change})
        else:
            self.data[player-1][pokemon].update({field:change})
        self.update()
        

    def restaurer_HP(self, player, pokemon): # restaurer les HP d'un pokemon
        player_data = self.data[player-1][pokemon]
        poke_id = player_data["id"]

        for pok in self.pokedex:
            if pok["id"] == poke_id:
                self.modifier(player, pokemon, pok["base"]["HP"], "base", "HP") 
                # on modifie les HP du pokemon du joueur par ceux trouvés dans le pokedex.json


    
    ######## Mise en place de la partie

    def random_pokemon(self):
        # ajoute des pokemons randoms
        # format de la bdd: bdd[1-1]["pokemon1"]["name"]["french"] -> nom français
        # [ {joueur: nomdujoueur1, pokemon1:{pokemon1- {name:{english name, french: nom}}}, pokemon2:{pokemon2}, pokemon3:{pokemon3}},
        # {joueur: nomdujoueur2, pokemon1:{pokemon1}, pokemon2:{pokemon2}, pokemon3:{pokemon3}} ]
        
        copy_pokedex = copy.deepcopy(self.pokedex) # il y a besoin de copier en deepcopy le pokedex pour que les pokemons qu'on y choisit aléatoire puisse être modifiés indépendemment
        return random.choice(copy_pokedex)
    

    def ajout_joueur(self, player):
        existe = False
        for joueur in self.data:
            # on vérifie que le joueur n'existe pas déjà
            if joueur["player"] == player:
                existe = True
                print(f'Joueur {player} déjà existant.')
        
        if existe == False: # si le joueur n'existe pas
            pok_liste = {"player":player}
            for i in range(3): # on lui attribue 3 pokemons au hasard
                keyname = "pokemon"+str(i+1) # pokemon1, pokemon2, pokemon3
                pok_liste[keyname] = self.random_pokemon()

            self.data.append(pok_liste) # on rajoute la liste des pokemons à la bdd

        
    def debut_de_la_partie(self, player1, player2):
        if self.reset == True: # s'il y a besoin de reset
            self.reset_bdd()
        
        # si un des joueurs existe déjà (a le même nom qu'un des joueurs dans la bdd), il ne sera pas créé
        self.ajout_joueur(player1)
        self.ajout_joueur(player2)
        self.update() # on inscrit le début de la partie dans la bdd




    ### méthodes pour faciliter le script combat
    
    def get_name(self, player, pokemon): # récupère le nom d'un pokemon
        return self.data[player-1][pokemon]["name"]["french"]
    
    def get_id(self, player, pokemon): # récupère l'id d'un pokemon
        return self.data[player-1][pokemon]["id"]
    
    def get_type(self, player, pokemon): # récupère les types d'un pokemon
        return self.data[player-1][pokemon]["type"]

    def get_base(self, player, pokemon): # récupère les bases d'un pokemon (HP notamment)
        return self.data[player-1][pokemon]["base"]

    def get_faiblesses(self, player, pokemon): # donne les faiblesses d'un pokemon
        types_pokemon = self.data[player-1][pokemon]["type"]
        faiblesses = []
        for types in types_pokemon:
            for entry in self.types: # à partir de la bdd types.json
                if entry["name"] == types:
                    faiblesses+=entry["weaknesses"]
        return faiblesses







    ######### fin de partie (deux fins possibles : la victoire ou la fuite)

    def victoire(self, player_winner, player_loser): # le joueur gagnant récupère tous les pokemons du perdant et le perdant est supprimé de la bdd
        winner = self.data[player_winner-1]
        loser = self.data[player_loser-1]
        # on récupère le dictionnaire de pokemon1, 2 et 3 de loser
        # on les rajoutes à winner et ils deviennent pokemon 5, 4 et 6

        winners_poke = len(winner)
        losers_poke = len(loser)
        
        # on copie les pokemons du joueur perdant dans une liste
        to_add = []
        for k in range(1,losers_poke):
            poke_lost = "pokemon"+str(k)
            to_add.append(loser[poke_lost])
        
        # ajouter les pokemons chez le joueur vainqueur
        for i in range(winners_poke, losers_poke+winners_poke-1):
            keyname = "pokemon"+str(i)
            winner[keyname] = to_add[i-winners_poke]

        # à la fin on supprime de la bdd le joueur perdant
        num_loser = self.data.index(loser)+1
        self.suppr(num_loser)
        self.update()


    def fuite(self): # fuite -> la partie s'arrête et les joueurs gardent leur pokemons
        # on restaure les hp des pokemons des deux joueurs
        for player in range(1,3):
            for pokemon in range(1, len(self.data[player-1])):
                self.restaurer_HP(player, "pokemon"+str(pokemon))
                print(self.data[player-1]["pokemon"+str(pokemon)])


    def save_player(self, player): # si on sauvegarde le joueur dans la bdd, on restaure les hp de ses pokemons
        self.reset = False # on ne reset pas la bdd
        for i in range(1,len(self.data[player-1])):
            self.restaurer_HP(player, "pokemon"+str(i))
        self.update()