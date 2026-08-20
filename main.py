import requests
import database
import customtkinter as ctk
from PIL import Image
from io import BytesIO

app = ctk.CTk()
app.geometry("1200x800")
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

#Register Frame
register_user_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
register_user_title = ctk.CTkLabel(
    register_user_frame,
    text = "Register:",
    font=arial_font
)
register_user_title.pack(pady=20)

def register_user():
    global current_user_id

    new_username = register_username_entry.get()
    new_password = register_password_entry.get()
    
    created_new_user = database.create_user(new_username, new_password)

    if created_new_user:
        current_user_id = created_new_user
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

def search_ability_button():
    logged_in_frame.forget()
    search_ability_frame.pack(fill="both", expand = True)

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

search_ability_btn = ctk.CTkButton(
    logged_in_frame,
    text = "Search for a ability",
    command = search_ability_button
)
search_ability_btn.pack(pady=20)

look_favourite_button = ctk.CTkButton(
    logged_in_frame,
    text = "Look at favourited pokemon"
)
look_favourite_button.pack(pady=20)

log_out_btn = ctk.CTkButton(
    logged_in_frame,
    text = "Logout",
    command = log_out_button
)
log_out_btn.pack(pady=20)

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

def go_to_frame(current_frame, target_frame):
    current_frame.pack_forget()
    target_frame.pack(fill="both", expand = True)

def create_back_button(parent, current_frame, target_frame):
    return ctk.CTkButton(
        parent,
        text = "Back",
        command = lambda: go_to_frame(current_frame, target_frame)
    )

def check_pk_exists():
    global current_pokemon

    pokemon_name = search_bar_entry.get()
    pk_dict = get_pokemon_data(pokemon_name)

    if pk_dict:
        search_bar_entry.delete(0, "end")
        
        current_pokemon = pk_dict

        display_pk_info_title.configure(
            text = pk_dict["name"].title()
        )

        height_label.configure(
            text = f"Height: {pk_dict['height'] / 10} m"
        )

        weight_label.configure(
            text = f"Weight: {pk_dict['weight'] / 10} kg"
        )

        types = [t["type"]["name"].title() for t in pk_dict["types"]]

        types_label.configure(
            text = f"Types: {', '.join(types)}"
        )

        abilities = [
            a["ability"]["name"].title()
            for a in pk_dict["abilities"]
        ]

        abilities_label.configure(
            text = f"Abilities: {', '.join(abilities)}"
        )

        description = get_pokemon_description(
            pk_dict["name"]
        )

        description_label.configure(
            text=description
        )

        sprite_url = pk_dict["sprites"]["other"]["official-artwork"]["front_default"]

        response = requests.get(sprite_url)

        pil_image = Image.open(BytesIO(response.content))

        ctk_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size = (300, 300)
        )

        sprite_label.configure(
            image = ctk_image,
            text = ""
        )

        sprite_label.image = ctk_image

        add_favourite_button = ctk.CTkButton(
            button_frame,
            text="Favourite!",
            command=add_to_fav
        )
        add_favourite_button.pack(side="left", pady=5, padx=10)

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
display_pk_info_title = ctk.CTkLabel(
    display_pk_info_frame,
    text="",
    font=arial_font
)
display_pk_info_title.pack(pady=20)

info_frame = ctk.CTkFrame(
    display_pk_info_frame,
    fg_color="red"
    )
info_frame.pack(side="left", padx=50, pady=20)

image_frame = ctk.CTkFrame(
    display_pk_info_frame,
    fg_color="red"
    )

image_frame.pack(side="left", padx=50, pady=20)

button_frame = ctk.CTkFrame(
    display_pk_info_frame,
    fg_color="red"
)
button_frame.pack(side="bottom", pady=10)

height_label = ctk.CTkLabel(
    info_frame,
    text=""
)
height_label.pack(pady=5)

weight_label = ctk.CTkLabel(
    info_frame,
    text=""
)
weight_label.pack(pady=5)

types_label = ctk.CTkLabel(
    info_frame,
    text=""
)
types_label.pack(pady=5)

abilities_label = ctk.CTkLabel(
    info_frame,
    text="",
    wraplength=400
)
abilities_label.pack(pady=5)

sprite_label = ctk.CTkLabel(
    image_frame,
    text= ""
)
sprite_label.pack(padx=10)

description_frame = ctk.CTkFrame(
    display_pk_info_frame,
    fg_color="red"
)

description_frame.pack(
    side="left",
    pady=20
)

description_frame_title = ctk.CTkLabel(
    description_frame,
    text = "Description:",
    font = arial_font
)
description_frame_title.pack(pady=20)

description_label = ctk.CTkLabel(
    description_frame,
    text = "",
    wraplength=350,
    justify = "left"
)
description_label.pack(pady=20)

favourite_status_label = ctk.CTkLabel(
    button_frame,
    text=""
)
favourite_status_label.pack(pady=5)

# Search for ability frame
def check_ab_exists():
    global current_ability

    ability = search_ab_bar_entry.get()
    ab_dict = get_ability_info(ability)

    if ab_dict:
        current_ability = ab_dict
        ability_frame_title.configure(
            text=ability.title()
        )
        ability_information.configure(
            text = ab_dict
        )

        search_ability_frame.forget()
        ability_frame.pack(fill = "both", expand = True)

search_ability_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
search_ability_title = ctk.CTkLabel(
    search_ability_frame,
    text = "Ability Search",
    font = arial_font
)
search_ability_title.pack(pady=10)

search_ab_bar_entry = ctk.CTkEntry(
    search_ability_frame,
    width = 250,
    placeholder_text="Ability Name"
)
search_ab_bar_entry.pack(pady=20)

search_ab_button = ctk.CTkButton(
    search_ability_frame,
    text = "Search!",
    command = check_ab_exists
)
search_ab_button.pack(pady=20)

# Display pokemon ability frame
ability_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
ability_frame_title = ctk.CTkLabel(
    ability_frame,
    text=""
)
ability_frame_title.pack(pady=10)

ability_information = ctk.CTkLabel(
    ability_frame,
    text = "",
    wraplength=700
)
ability_information.pack(pady=10)

# Look at favourites frame
def open_favourite_pokemon(pokemon_name):
    search_bar_entry.delete(0, "end")
    search_bar_entry.insert(0, pokemon_name)

    favourites_frame.pack_forget()
    check_pk_exists()

def load_favourites():
    if current_user_id in (None, 0):
        return

    for widget in scrollable_favourites.winfo_children():
        widget.destroy()

    favourites = database.get_user_favourites(
        current_user_id
    )
    for favourite in favourites:

        pokemon_name = favourite[0]

        pokemon_button = ctk.CTkButton(
            scrollable_favourites,
            text=pokemon_name.title(),
            command=lambda name=pokemon_name:
                open_favourite_pokemon(name)
        )
        pokemon_button.pack(
            fill="x",
            padx=10,
            pady=5
        )

def show_favourites():
    if current_user_id in (None, 0):

        favourite_status_label.configure(
            text="You must be logged in."
        )

        return

    load_favourites()
    logged_in_frame.pack_forget()

    favourites_frame.pack(
        fill="both",
        expand=True
    )

look_favourite_button.configure(
    command = show_favourites
)
favourites_frame = ctk.CTkFrame(
    app,
    fg_color="red"
)
favourites_title = ctk.CTkLabel(
    favourites_frame,
    text="Favourite Pokemon",
    font=arial_font
)

favourites_title.pack(pady=10)

scrollable_favourites = ctk.CTkScrollableFrame(
    favourites_frame, width=400, height=400
)

scrollable_favourites.pack(
    fill="both", expand=True, padx=20, pady=20
)

# Defining all back buttons
login_back_button = create_back_button(
    log_in_frame,
    log_in_frame,
    main_menu_frame
)
login_back_button.pack(pady=10)

register_back_button = create_back_button(
    register_user_frame,
    register_user_frame,
    main_menu_frame
)
register_back_button.pack(pady=10)

search_pk_back_button = create_back_button(
    search_pokemon_frame,
    search_pokemon_frame,
    logged_in_frame
)
search_pk_back_button.pack(pady=10)

pk_info_back = create_back_button(
    button_frame,
    display_pk_info_frame,
    search_pokemon_frame
)
pk_info_back.pack(side="right", pady=10)

search_ab_back_button = create_back_button(
    search_ability_frame,
    search_ability_frame,
    logged_in_frame
)
search_ab_back_button.pack(pady=10)

ability_back_button = create_back_button(
    ability_frame,
    ability_frame,
    search_ability_frame
)
ability_back_button.pack(pady=10)

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

# Retrieves pokemon species description
def get_pokemon_description(pokemon_name):
    url = f"{base_url}/pokemon-species/{pokemon_name}"

    response = requests.get(url)

    if response.status_code == 200:
        species_data = response.json()

        for entry in species_data["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                return entry["flavor_text"].replace("\n", " ").replace("\f", " ")

    return "No description available."

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

def add_to_fav():
    global current_pokemon

    if current_user_id == 0:
        favourite_status_label.configure(
            text="Must be logged in first."
        )
        return

    pk_name = current_pokemon["name"]

    success = database.add_fav_to_db(current_user_id, pk_name)

    if success:
        favourite_status_label.configure(
            text="Added to favourites!"
        )
    else:
        favourite_status_label.configure(
            text="Already in favourites."
        )

app.mainloop()