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

# récupérer le pokedex
# https://github.com/fanzeyi/pokemon.json/blob/master/pokedex.json
with open('pokedex.json', 'r') as f:
    pokedex = json.load(f)
# pokedex is a list of dictionnaries containing all of the pokemons

# récuperer les types
with open('types.json', 'r') as f:
    types = json.load(f)
# types is a list of dictionnaries containing all of the types and their weaknesses

class BDD():
    # initialise la bdd en l'ouvrant
    def __init__(self, bdd_file):
        self.file_path = bdd_file

        with open(self.file_path, 'r') as f:
            try:
                self.data = json.load(f)
            except json.decoder.JSONDecodeError:
                self.data = []
    
    # affiche la bdd dans le terminal:
    # - toute la bdd
    # - player=1 ou player=2 pour un joueur en particulier
    def affichage(self, player=False):
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
    def random_pokemon(self, pokedex):
        return random.choice(pokedex)
    
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
                pok_liste[keyname] = self.random_pokemon(pokedex)

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
            self.data[player-1][pokemon][field][subfield] = change
        else:
            self.data[player-1][pokemon][field] = change
    

    # fuite -> suppression du joueur dans la bdd?
    def fuite(self, player):
        self.suppr(player)

    # add another player's pokemons
    def victory(self, player_winner, player_loser):
        winner = self.data[player_winner-1]
        loser = self.data[player_loser-1]
        # on récupère le dictionnaire de pokemon1, 2 et 3 de loser
        # on les rajoutes à pokemon 5, 4 et 6 de winner

        winners_poke = len(winner)-1
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


    # sauvegarde d'un joueur dans la bdd --> restaurer les HP de ses pokemons
    def save_player(self, player):
        player_data = self.data[player-1]

        for key in range(1,len(player_data)):
            keyname = "pokemon"+str(key)
            poke_id = player_data[keyname]["id"]

            # on pourrait garder en mémoire la liste des pokemons actuellement sur la partie mais j'ai pas réussi à le faire
            # pour quelque raison ça bug ??
            for pokemon in pokedex:
                if pokemon["id"] == poke_id:
                    full_HP = pokemon["base"]["HP"]
                    self.modifier(player, keyname, full_HP, "base", "HP")

        # print(pokedex)
        




# Set up

pokebdd = BDD('bdd.json')
pokebdd.suppr(player=1)
pokebdd.suppr(player=1)

pokebdd.ajout_joueur("joueur1")
pokebdd.ajout_joueur("joueur2")
pokebdd.update()
pokebdd.affichage(1)


print("\n########################################\n")

# actions

pokebdd.modifier(player=1, pokemon="pokemon2", change=0, field='base', subfield='HP')
# pokebdd.victory(2,1)
# pokebdd.fuite(1)
pokebdd.affichage(1)
# pokebdd.affichage(player=1)

print("\n########################################\n")

pokebdd.save_player(1)
pokebdd.update()
pokebdd.affichage(1)