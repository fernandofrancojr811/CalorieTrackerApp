# NutriStrong: Calorie Tracker Web App

NutriStrong is a web application that allows users to track their daily calorie intake, manage their nutrition, and keep a journal of their meals. It provides a user-friendly interface for adding food items, specifying serving sizes, and viewing daily nutrition totals.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)

## Features

- **Calorie Tracking:** Users can input food items and serving sizes to get detailed nutritional information, including calories, protein, carbs, sugar, and fat.

- **Meal Journal:** The app allows users to maintain a journal of their meals, categorized into breakfast, lunch, and dinner. Each journal entry includes the date, food item, and calories.

- **Daily Nutrition Totals:** NutriScope calculates and displays daily nutrition totals, helping users keep track of their daily intake of calories, protein, carbs, sugar, and fat.

- **Reset Daily Totals:** Users have the option to reset their daily nutrition totals to start tracking a new day.

## Technologies Used

- **Flask:** The web application is built using the Flask web framework, providing a backend for handling requests and serving HTML templates.

- **HTML/CSS:** The user interface is designed using HTML and styled with CSS for a clean and modern look.

- **Python:** Python is used for server-side logic, including data storage, calculation of daily totals, and handling journal entries.

- **Bootstrap:** The Bootstrap CSS framework is used to enhance the visual appearance and responsiveness of the web app.

- **GitHub:** The project is hosted on GitHub for version control and collaboration.

## Getting Started

To run NutriStrong locally on your machine, follow these steps:

1. Clone the repository to your local machine:

git clone https://github.com/fernandofrancojr811/nutriscopes.git
Navigate to the project directory:

cd nutriscopes
Install the required dependencies:

pip install -r requirements.txt
Set up your Nutritionix API credentials:

Replace app_id and app_key in the app.py file with your Nutritionix API credentials.
Run the application:

python app.py
Access the application in your web browser at http://localhost:5000.

Usage
Enter a food item and serving size to get nutritional information.

Select a meal category (breakfast, lunch, or dinner) and add food items to your journal.

View and edit your journal entries.

Reset daily nutrition totals to start tracking a new day.





