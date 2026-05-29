# WebKuh

WebKuh is a Django web application for creating, managing, and sharing recipes.

The project was built as a personal portfolio project while learning Python, Django, HTML, CSS,
and web application development.
The main goal of the project is to practice real-world backend and frontend concepts through a functional
recipe management app.

## Features

- User registration, login, and logout
- Create, edit, and delete recipes
- Private and public recipes
- Recipe detail pages
- Image upload for recipes
- Ingredients connected to recipes
- Search recipes by title or description
- Sort recipes by newest or oldest
- Pagination
- Public recipe listing
- Owner-only permissions for editing and deleting recipes
- Responsive recipe card layout
- Basic UI styling with custom CSS

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite
- Git
- GitHub

## Project Structure

```text
webkuh/
├── accounts/
├── recipes/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Main App Logic

The application is built around recipes created by registered users.

Each recipe can contain:

- title
- description
- instructions
- preparation time
- image
- ingredients
- public/private status
- owner information
- creation and update timestamps

Users can manage only their own recipes, while public recipes can be viewed by other users.

## Installation and Local Setup

Clone the repository:

```bash
git clone https://github.com/PaxTecum37/webkuh.git
cd webkuh
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Current Status

The project is still in development.

Planned improvements include:

- recipe ratings
- comments
- improved filtering
- better public recipe discovery
- improved responsive design
- possible deployment version

## What I Learned

While building this project, I practiced:

- Django models, views, URLs, and templates
- User authentication
- Working with forms and formsets
- Handling image uploads
- Connecting related data with foreign keys
- Protecting user-owned content
- Creating public and private views
- Working with query parameters for search, sorting, and pagination
- Organizing CSS for a larger project
- Using Git and GitHub for version control

## Author

Created by Igor Vukančić [PaxTecum37](https://github.com/PaxTecum37)
