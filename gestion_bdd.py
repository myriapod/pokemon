# - script qui reçoit des infos du script combat
# - importer la bdd pokemon
# - script lit et écrit dans bdd.txt
# -- début de la partie-- 
# def creation entrée
# def récuperer les pokemons full hp
# -- fin de la partie --
# def victoire
# (joueur gagnant récupère les 3 pokemons)
# def defaite (suppr du joueur de la bdd)

import json
import random
import copy


class BDD():
    
    def __init__(self, bdd_file):
        self.file_path = bdd_file
        self.reset = True

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
            json.dump(self.data, f)


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

    
    # supprimer un joueur 1 ou 2 de la bdd
    # player = 1 ou 2
    def suppr(self, player):
        self.data.pop(player-1)
    

    # modifie un élément de la bdd
    # player = 1 ou 2
    # pokemon = pokemon[i]
    # change = nouvelle valeur
    # field = key, subfield = key de la key si besoin
    def modifier(self, player, pokemon, change, field, subfield=False):
        if subfield != False:
            self.data[player-1][pokemon][field].update({subfield:change})

        else:
            self.data[player-1][pokemon].update({field:change})

        self.update()
        
    # restaurer les HP d'un pokemon
    def restaurer_HP(self, player, pokemon):
        player_data = self.data[player-1][pokemon]
        poke_id = player_data["id"]

        for pok in self.pokedex:
            if pok["id"] == poke_id:
                self.modifier(player, pokemon, pok["base"]["HP"], "base", "HP")


    
    ######## Mise en place de la partie

    # ajoute des pokemons randoms
    # format de la bdd: bdd[1-1]["pokemon1"]["name"]["french"] -> nom français
    # [ {joueur: nomdujoueur1, pokemon1:{pokemon1- {name:{english name, french: nom}}}, pokemon2:{pokemon2}, pokemon3:{pokemon3}},
    # {joueur: nomdujoueur2, pokemon1:{pokemon1}, pokemon2:{pokemon2}, pokemon3:{pokemon3}} ]
    def random_pokemon(self):
        # il y a besoin de copier en deepcopy le pokedex pour que les pokemons qu'on y choisit aléatoire puisse être modifiés indépendemment
        copy_pokedex = copy.deepcopy(self.pokedex)
        return random.choice(copy_pokedex)
    
    def ajout_joueur(self, player):
        existe = False
        for joueur in self.data:
            # on vérifie que le joueur n'existe pas déjà
            if joueur["player"] == player:
                existe = True
                print(f'Joueur {player} déjà existant.')
        
        if existe == False:
            pok_liste = {"player":player}
            for i in range(3):
                keyname = "pokemon"+str(i+1)
                pok_liste[keyname] = self.random_pokemon()

            self.data.append(pok_liste)

        


    def debut_de_la_partie(self, player1, player2):
        print("RESET=", self.reset)
        if self.reset == True:
            for i in range(len(self.data)):
                self.suppr(1)
        
        self.ajout_joueur(player1)
        self.ajout_joueur(player2)
        self.update()




    ### méthodes pour faciliter le script combat
    # récupère le nom d'un pokemon
    def get_name(self, player, pokemon):
        return self.data[player-1][pokemon]["name"]["french"]

    # récupère l'id d'un pokemon
    def get_id(self, player, pokemon):
        return self.data[player-1][pokemon]["id"]
    
    def get_type(self, player, pokemon):
        return self.data[player-1][pokemon]["type"]

    def get_base(self, player, pokemon):
        return self.data[player-1][pokemon]["base"]

    # donne les faiblesses d'un pokemon
    def get_faiblesses(self, player, pokemon):
        types_pokemon = self.data[player-1][pokemon]["type"]
        faiblesses = []
        for types in types_pokemon:
            for entry in self.types:
                if entry["name"] == types:
                    faiblesses+=entry["weaknesses"]
        return faiblesses







    ######### fin de partie (deux fins possibles : la victoire ou la fuite)

    # le joueur gagnant récupère tous les pokemons du perdant et le perdant est supprimé de la bdd
    def victoire(self, player_winner, player_loser):
        winner = self.data[player_winner-1]
        loser = self.data[player_loser-1]
        # on récupère le dictionnaire de pokemon1, 2 et 3 de loser
        # on les rajoutes à pokemon 5, 4 et 6 de winner

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


    # fuite -> la partie s'arrête et les joueurs gardent leur pokemons
    def fuite(self):
        # on restaure les hp des pokemons des deux joueurs
        for player in range(1,3):
            for pokemon in range(1, len(self.data[player-1])):
                self.restaurer_HP(player, "pokemon"+str(pokemon))
                print(self.data[player-1]["pokemon"+str(pokemon)])


    # si on sauvegarde le joueur dans la bdd, on restaure les hp de ses pokemons
    def save_player(self, player):
        self.reset = False
        for i in range(1,len(self.data[player-1])):
            self.restaurer_HP(player, "pokemon"+str(i))

        




"""# Set up
pokebdd = BDD('bdd.json')
i=0
while i<3:
    i+=1
    pokebdd.debut_de_la_partie("joueur1", "joueur2")

    # pokebdd.affichage()
    # pokebdd.faiblesses(1, "pokemon1")


    print(f"\n################## tour {i} ######################\n")

    # actions

    pokebdd.modifier(player=1, pokemon="pokemon2", change=0, field='base', subfield='HP')
    pokebdd.modifier(player=1, pokemon="pokemon3", change=0, field='base', subfield='HP')
    pokebdd.victoire(1,2)
    # pokebdd.fuite(1)
    pokebdd.affichage(1)
    # pokebdd.fuite(1)
    # pokebdd.affichage(player=1)
    # print(pokebdd.active_pokemons)

    # pokebdd.restaurer_HP(player=1, pokemon="pokemon2")

    # print("\n########################################\n")

    if i%2==0:
        pokebdd.save_player(1)"""