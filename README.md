# Pokédex Desktop Application

A desktop Pokédex application built with Python and CustomTkinter that allows users to search for Pokémon, view detailed information retrieved from the PokéAPI, and save favourite Pokémon to a local database.

This project was created to learn API integration, database management, GUI development, and user authentication while building a practical application.

## Features

- User registration and login system
- Secure password storage using bcrypt hashing
- Search for Pokémon using the PokéAPI
- View Pokémon information:
  - Name
  - Height
  - Weight
  - Types
  - Abilities
  - Official artwork
  - Pokédex description
- Save Pokémon to a favourites list
- View saved favourite Pokémon
- Guest mode support

## Technologies Used

- Python
- CustomTkinter
- SQLite
- PokéAPI
- bcrypt
- Requests
- Pillow (PIL)

## Skills Demonstrated

- REST API integration
- GUI development
- Database design and SQL
- User authentication
- Password hashing and security practices
- Data management
- Error handling
- Version control with Git and GitHub

## Project Structure

```text
PokeAPI/
├── main.py
├── database.py
├── pokedex.db
└── README.md
```

## Future Improvements

- Migrate from SQLite to PostgreSQL
- Host the database on a cloud service
- Remove favourite Pokémon functionality
- Advanced Pokémon filtering by type
- Search history
- Pokémon team builder
- Improved UI styling and themes

## Screenshots
### Welcome Screen
<img width="753" height="547" alt="image" src="https://github.com/user-attachments/assets/c23e3ccd-1900-4271-95cf-065aecf30e35" />

### Main Menu
<img width="753" height="547" alt="image" src="https://github.com/user-attachments/assets/f521a7ad-187a-496e-af14-b6719e3bfcb4" />

### Pokémon Information
<img width="753" height="547" alt="image" src="https://github.com/user-attachments/assets/b156257d-d169-4d22-9bfc-55297bb8ccf7" />

Displays detailed Pokémon information retrieved from the PokéAPI, including official artwork, description, types, abilities, height, and weight. Logged-in users can add Pokémon to their favourites.

### Favourites Page
<img width="753" height="547" alt="image" src="https://github.com/user-attachments/assets/c9092db3-b7df-49d3-9935-05a1f3b0add4" />

Shows all Pokémon saved by the current user. Each Pokémon is displayed as a clickable button that loads its full information page.

## Acknowledgements

- PokéAPI for providing free Pokémon data
- CustomTkinter for the modern Python GUI framework

## Author

David — Computer Science & Artificial Intelligence Student at Loughborough University.
