# Recipe App - ZeroWaste Chef

A Django-based recipe management application where users can browse, create, and manage recipes with features like favorites, ratings, and category browsing.

## Features

- **User Authentication**: Register, login, and manage profiles
- **Recipe Management**: Create, edit, and delete recipes
- **Recipe Categories**: Browse recipes by category (Breakfast, Main Course, Desserts, etc.)
- **Favorites System**: Save and manage favorite recipes
- **Rating System**: Rate and review recipes
- **Responsive Design**: Modern, mobile-friendly interface
- **Image Support**: Upload and display recipe images
- **Search and Filter**: Find recipes easily

## Tech Stack

- **Backend**: Django 5.1+
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome
- **Image Processing**: Pillow

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd ReceipeApp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**
   ```bash
   python manage.py load_all_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

## Project Structure

```
ReceipeApp/
├── ReceipeApp/          # Django project settings
├── recipes/             # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL patterns
│   ├── forms.py         # Django forms
│   ├── templates/       # HTML templates
│   └── static/          # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## Available Management Commands

- `python manage.py add_breakfast_recipes` - Add breakfast recipes
- `python manage.py add_main_course_recipes` - Add main course recipes
- `python manage.py add_desserts_recipes` - Add dessert recipes
- `python manage.py add_drinks_recipes` - Add drink recipes
- `python manage.py add_pasta_recipes` - Add pasta recipes
- `python manage.py add_rice_recipes` - Add rice-based recipes
- `python manage.py add_snacks_recipes` - Add snack recipes
- `python manage.py add_soup_recipes` - Add soup recipes
- `python manage.py add_vegetarian_recipes` - Add vegetarian recipes
- `python manage.py assign_recipe_images` - Assign images to recipes
- `python manage.py assign_category_images` - Assign images to categories

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Acknowledgments

- Django documentation and community
- Bootstrap for the responsive design framework
- Font Awesome for the icons
- All contributors and users of this project
