import requests
import database

# PokeAPI's link, removes repetition
base_url = "https://pokeapi.co/api/v2/"

# Prompts users to login and displays menu
def main():
    print("---------------WELCOME TO THE POKEDEX---------------")
    display_login_options()
    choice = int(input())

    while choice > 3 or choice < 1:
        display_login_options
        choice = int(input())

    if choice == 1:
        pass
    elif choice == 2:
        create_new_user()

    elif choice == 3:
        pass

def create_new_user():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    created_new_user = database.create_user(username, password)

    if created_new_user:
        logged_in()
    else:
        main()
    
def logged_in(user_id):
    display_main_menu()
    choice = int(input())

    while choice > 3 or choice < 1:
        display_main_menu
        choice = int(input())

    if choice == 1:
        pk_name = input("Enter the name of a Pokémon: ").lower()
        pk_dict = get_pokemon_data(pk_name)

        if pk_dict:
            display_info(pk_dict)

    elif choice == 2:
        pk_ability = input("Enter the name of the ability: ").lower()
        abi = get_ability_info(pk_ability)

        if abi:
            print(f"{abi}\n")
    
    elif choice == 3:
        print("Goobye!")

    else:
        print("Please enter a valid option")

def display_main_menu():
    print("1- Search for a pokemon")
    print("2- Search for an ability")
    print("3- Quit")

def display_login_options():
    print("Please choose one of the following options: ")
    print("1- Login")
    print("2- Register")
    print("3- Search without logging in")

# Retrieves data by requesting the entered pokemon name and displays a reasonable message if retrieval failed
# else returns the information as a dictionary
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

# Retrieves ability information from user input, only returns the ability in english
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

# Uses get_pokemon_data() and uses the dictionary returned to filter and display relevant information.
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