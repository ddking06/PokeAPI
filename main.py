import requests

base_url = "https://pokeapi.co/api/v2/"

def main():
    pk_name = input("Enter the name of a Pokémon: ").lower()

    pk_dict = get_pokemon_data(pk_name)

    if pk_dict:
        display_info(pk_dict)

def get_pokemon_data(pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_info = response.json()
        return pokemon_info
    elif response.status_code == 404:
        print("Pokemon not found.")
    else:
        print(f"Failed to retrieve data {response.status_code}")

def get_ability_info(ability_name):
    url = f"{base_url}/ability/{ability_name}"
    response = requests.get(url)
    if response.status_code == 200:
        ability_info = response.json()
        for a in ability_info["effect_entries"]:
            if a["language"]["name"] == "en":
                return a["effect"]
    else: 
        print(f"Failed to retrieve ability. {response.status_code}")

def display_info(data):
    print(f"Name: {data['name']}\n")
    print(f"Id: {data['id']}\n")
    print(f"Height: {data['height']/10}m\n")
    print(f"Weight: {data['weight']/10}kg\n")
    for a in data["abilities"]:
        effect = get_ability_info(a['ability']['name'])
        if effect:
            effect = effect.replace("\n", " ")
        print(f"Ability name: {a['ability']['name']} - {effect}\nHidden: {a['is_hidden']}")
        print("")

if __name__ == "__main__":
    main()