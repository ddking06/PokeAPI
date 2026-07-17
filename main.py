import requests
import database
import customtkinter as ctk

app = ctk.CTk()
app.geometry("2000x1500")
app.title("Pokedex")
app.configure(fg_color='red')

# PokeAPI's link, removes repetition
base_url = "https://pokeapi.co/api/v2/"

# Main menu frame
main_menu_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)

main_menu_frame.pack(
    fill = "both",
    expand = True
)

# Prompts users to login and displays menu
def log_in_pressed():
    main_menu_frame.pack_forget()
    log_in_frame.pack(fill="both", expand = True)

def register_pressed():
    create_new_user()

def guest_pressed():
    logged_in()

def quit_program():
    app.destroy()

title = ctk.CTkLabel(
    main_menu_frame,
    text = "POKEDEX",
    font = ("Arial", 30, "bold")
    )
title.pack(pady=20)

login_button = ctk.CTkButton(
    main_menu_frame, 
    text = "Login",
    command = log_in_pressed
)
login_button.pack(pady=10)

register_button = ctk.CTkButton(
    main_menu_frame,
    text = "Register",
    command = register_pressed
)
register_button.pack(pady=10)

guest_button = ctk.CTkButton(
    main_menu_frame,
    text = "Continue as guest",
    command = guest_pressed
)
guest_button.pack(pady=10)

quit_button = ctk.CTkButton(
    main_menu_frame,
    text = "Quit",
    command = quit_program
)
quit_button.pack(pady=10)

# Log in Frame
log_in_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)

login_title = ctk.CTkLabel(
    log_in_frame,
    text = "Login",
    font = ('Arial', 30, 'bold')
)

login_title.pack(pady=20)

def verify_user():
    username = username_entry.get()
    password = password_entry.get()
    user_id = database.verify_user(username, password)

    if user_id is not None:
        logged_in(user_id)
    else:
        print("Invalid username or password")

def back_to_main():
    log_in_frame.pack_forget()
    main_menu_frame.pack(fill="both", expand=True)

username_entry = ctk.CTkEntry(
    log_in_frame,
    width = 250,
    placeholder_text="Username"
)
username_entry.pack(pady=5)

password_entry = ctk.CTkEntry(
    log_in_frame,
    width = 250,
    placeholder_text="Password",
    show = "*"
)
password_entry.pack(pady=5)

check_login_button = ctk.CTkButton(
    log_in_frame,
    text = "Login",
    command = verify_user
)
check_login_button.pack(pady=10)

back_button = ctk.CTkButton(
    log_in_frame,
    text = "Back",
    command = back_to_main
)
back_button.pack(pady=10)

def create_new_user():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    created_new_user = database.create_user(username, password)

    if created_new_user:
        logged_in(created_new_user)
    else:
        return
    
def logged_in(user_id=0):
    while True:
        display_main_menu()
        try:
            choice = int(input())

            if not(1 <= choice <= 5):
                print("Please enter a numer between 1 and 3")
                continue
        except ValueError:
            print("Please enter a valid number.")

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
            add_to_fav(user_id)

        elif choice == 4:
            pass

        elif choice == 5:
            break

        else:
            print("Please enter a valid option")
            continue
    return

def display_main_menu():
    print("1- Search for a pokemon")
    print("2- Search for an ability")
    print("3- Add a pokemon to favourites")
    print("4- Look at favourited pokemons")
    print("5- Logout")

def display_login_options():
    print("Please choose one of the following options: ")
    print("1- Login")
    print("2- Register")
    print("3- Search without logging in")
    print("4- Quit")

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

def add_to_fav(user_id):
    if user_id == 0:
        print("You must be logged in to see this feature.\n")
        return
    
    while True:
        pk = input("Please enter the name of the pokemon to add to your favourites: ")

        url = f"{base_url}/pokemon/{pk}"
        response = requests.get(url)
        
        if response.status_code == 200:
            database.add_fav_to_db(user_id, pk)
            return
        else:
            print("Pokemon not found.")
            continue

app.mainloop()