# - script qui reçoit des infos du script combat
# - importer la bdd pokemon
# - script lit et écrit dans bdd.txt
# -- début de la partie-- 
# def creation entrée
# def récuperer les pokemons full hp
# -- cours de la partie --
# def pokemon battu (quand hp=0)
# -- fin de la partie --
# def victoire
# (joueur gagnant récupère les 3 pokemons)
# def defaite (suppr du joueur de la bdd)

import json

# récupérer le pokedex
with open('pokedex.json', 'r') as poke:
    pokedex = json.load(poke)

# pokedex is a list of dictionnaries containing all of the pokemons