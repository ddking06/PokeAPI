import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_data(pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name}"
    response = requests.get(url)
    print(response)

pk_name = input("Enter the name of a Pokémon: ").lower()

get_pokemon_data(pk_name)