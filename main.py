import requests
import database
import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x300")
app.title("Pokedex")
app.configure(fg_color='red')

# PokeAPI's link, removes repetition
base_url = "https://pokeapi.co/api/v2/"

current_user_id = None
current_pokemon = None
current_ability = None
arial_font = ('Arial', 30, 'bold')

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
    main_menu_frame.pack_forget()
    register_user_frame.pack(fill="both", expand = True)

def guest_pressed():
    global current_user_id
    current_user_id = 0
    main_menu_frame.pack_forget()
    logged_in_frame.pack(fill="both", expand = True)

def quit_program():
    app.destroy()

title = ctk.CTkLabel(
    main_menu_frame,
    text = "POKEDEX",
    font = arial_font
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
    font = arial_font
)

login_title.pack(pady=20)

def verify_user():
    global current_user_id

    username = username_entry.get()
    password = password_entry.get()
    
    user_id = database.verify_user(username, password)

    if user_id is not None:
        current_user_id = user_id
        log_in_frame.pack_forget()
        logged_in_frame.pack(fill="both", expand = True)
    else:
        incorrect_details_label.pack(pady=30)

incorrect_details_label = ctk.CTkLabel(
    log_in_frame,
    text = "Incorrect username or password",
    font = arial_font
)

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

#Register Frame
register_user_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
register_user_title = ctk.CTkLabel(
    register_user_frame,
    text = "Registe:",
    font=arial_font
)
register_user_title.pack(pady=20)

def register_user():
    global current_user_id

    new_username = register_username_entry.get()
    new_password = register_password_entry.get()
    
    created_new_user = database.create_user(new_username, new_password)

    if created_new_user:
        current_user_id = create_new_user
        register_user_frame.pack_forget()
        logged_in_frame.pack(fill="both", expand = True)
    else:
        username_already_exists.pack(pady=20)

register_username_entry = ctk.CTkEntry(
    register_user_frame,
    width = 250,
    placeholder_text="Username"
)
register_username_entry.pack(pady=5)

register_password_entry = ctk.CTkEntry(
    register_user_frame,
    width = 250,
    placeholder_text="Password",
    show = "*"
)
register_password_entry.pack(pady=5)

register_button = ctk.CTkButton(
    register_user_frame,
    text = "Register!",
    command = register_user
)
register_button.pack(pady=20)

username_already_exists = ctk.CTkLabel(
    register_user_frame,
    text = "Sorry, username provided already exists.",
    font = arial_font
)

# Logged/Guest in Frame
logged_in_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)

logged_in_title = ctk.CTkLabel(
    logged_in_frame,
    text = "Main menu",
    font = arial_font
)
logged_in_title.pack(pady=10)

def search_pokemon_button():
    logged_in_frame.pack_forget()
    search_pokemon_frame.pack(fill="both", expand = True)

def log_out_button():
    global current_user_id
    current_user_id = None
    logged_in_frame.pack_forget()
    main_menu_frame.pack(fill = "both", expand = True)

search_pk_button = ctk.CTkButton(
    logged_in_frame,
    text = "Search for a pokemon",
    command = search_pokemon_button
)
search_pk_button.pack(pady=20)

search_ability_button = ctk.CTkButton(
    logged_in_frame,
    text = "Search for a ability"
)
search_ability_button.pack(pady=20)

add_pokemon_to_fav_button = ctk.CTkButton(
    logged_in_frame,
    text = "Add a pokemon to favourites"
)
add_pokemon_to_fav_button.pack(pady=20)

look_favourite_button = ctk.CTkButton(
    logged_in_frame,
    text = "Look at favourited pokemon"
)
look_favourite_button.pack(pady=20)

log_out_button = ctk.CTkButton(
    logged_in_frame,
    text = "Logout",
    command = log_out_button
)
log_out_button.pack(pady=20)

# Search for Pokemon Frame
search_pokemon_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
search_pokemon_title = ctk.CTkLabel(
    search_pokemon_frame,
    text = "Pokedex Search",
    font = arial_font
)
search_pokemon_title.pack(pady=10)

def check_pk_exists():
    global current_pokemon
    pokemon_name = search_bar_entry.get()
    pk_dict = get_pokemon_data(pokemon_name)

    if pk_dict:
        current_pokemon = pk_dict
        search_pokemon_frame.pack_forget()
        display_pk_info_frame.pack(fill="both", expand = True)
    else:
        error_searching_label.pack(pady=20)


error_searching_label = ctk.CTkLabel(
    search_pokemon_frame,
    text = "Sorry, details entered don't match anything on the system. Please check your spelling.",
    font = arial_font
)
search_bar_entry = ctk.CTkEntry(
    search_pokemon_frame,
    width = 250,
    placeholder_text="Pokemon Name"
)
search_bar_entry.pack(pady=20)

search_button = ctk.CTkButton(
    search_pokemon_frame,
    text = "Search!",
    command = check_pk_exists
)
search_button.pack(pady=20)

#Display pokemon info frame
display_pk_info_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)

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