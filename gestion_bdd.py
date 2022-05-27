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


class BDD():
    
    def __init__(self, bdd_file):
        self.file_path = bdd_file
        self.active_pokemons = []

        with open(self.file_path, 'r') as f:
            try: # initialise la bdd en l'ouvrant
                self.data = json.load(f)
            except json.decoder.JSONDecodeError: # si le fichier est vide, on initialise data à une liste vide
                self.data = []

        
        with open('pokedex.json', 'r') as f:
            # récupérer le pokedex https://github.com/fanzeyi/pokemon.json/blob/master/pokedex.json
            self.pokedex = json.load(f) # pokedex est une liste de dictionnaire, 1 pokemon par dictionnaire


        with open('types.json', 'r') as f:
            # récuperer les types
            self.types = json.load(f) # types est une liste de dictionnaire contenant tous les types et leurs faiblesses
    


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

        

    # ajoute des pokemons randoms
    # format de la bdd:
    # [ {joueur: nomdujoueur1, pokemon1:{pokemon1}, pokemon2:{pokemon2}, pokemon3:{pokemon3}},
    # {joueur: nomdujoueur2, pokemon1:{pokemon1}, pokemon2:{pokemon2}, pokemon3:{pokemon3}} ]
    def random_pokemon(self):
        return random.choice(self.pokedex)
    
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
                self.active_pokemons.append(pok_liste[keyname])

            self.data.append(pok_liste)
            


    # mise à jour de la bdd
    def update(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f)


    # supprimer un joueur 1 ou 2 de la bdd
    # player = 1 ou 2
    def suppr(self, player):
        self.data.pop(player-1)
    

    # modifie un élément de la bdd
    # player = 1 ou 2
    # change = nouvelle valeur
    # field = key, subfield = key de la key si besoin
    def modifier(self, player, pokemon, change, field, subfield=False):
        if subfield != False:
            self.data[player-1][pokemon][field].update({subfield:change})
            # print(self.data[player-1][pokemon][field])
        else:
            self.data[player-1][pokemon].update({field:change})
        
    

    # ajouter les pokemons du joueur perdant
    def victory(self, player_winner, player_loser):
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

        # à la fin on supprime le joueur perdant
        num_loser = self.data.index(loser)+1
        self.suppr(num_loser)


    # restaurer les HP d'un pokemon
    def restaurer_HP(self, player, pokemon):
        player_data = self.data[player-1][pokemon]
        poke_id = player_data["id"]
        print("ID -----------", poke_id)
        for pok in self.pokedex:
            if pok["id"] == poke_id:
                print("POKID --------", pok["id"])
                print("PLAYER HP --- ", player_data["base"]["HP"], "--- POKE HP ---", pok["base"]["HP"])
            # arrive pas à récupérer les HP de base des pokemons



    # fuite -> la partie s'arrête et les joueurs gardent leur pokemons
    def fuite(self, player):
        for pokemon in range(1, len(self.data[player-1])):
            self.restaurer_HP(player, "pokemon"+str(pokemon))
            print(self.data[player-1]["pokemon"+str(pokemon)])



    ############# Marche pas
    def save_player(self, player):
        player_data = self.data[player-1]

        for key in range(1,len(player_data)):
            keyname = "pokemon"+str(key)
            poke_id = player_data[keyname]["id"]

            # on pourrait garder en mémoire la liste des pokemons actuellement sur la partie mais j'ai pas réussi à le faire
            # pour quelque raison ça bug ??
            for poked in self.active_pokemons:
                if poked["id"] == poke_id:
                    print(poked)
                    print(poked["base"]["HP"])
                    self.modifier(player, keyname, poked["base"]["HP"], "base", "HP")

        # print(pokedex)
        




# Set up

pokebdd = BDD('bdd.json')

pokebdd.suppr(1)
pokebdd.active_pokemons=[]

pokebdd.ajout_joueur("joueur1")
pokebdd.update()
# pokebdd.affichage()


print("\n########################################\n")

# actions

pokebdd.modifier(player=1, pokemon="pokemon3", change=0, field='base', subfield='HP')
pokebdd.update()
# pokebdd.victory(1,2)
# pokebdd.fuite(1)
pokebdd.affichage(1)
pokebdd.fuite(1)
# pokebdd.affichage(player=1)
# print(pokebdd.active_pokemons)

# pokebdd.restaurer_HP(player=1, pokemon="pokemon3")

print("\n########################################\n")

# pokebdd.save_player(1)
pokebdd.update()
pokebdd.affichage()