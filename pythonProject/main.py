from flask import Flask
import requests
from openpyxl import Workbook

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


app_id = "8bc7b25a"
app_key = "dd56c0e7590da1e3f54f9269de8b9588"

# Replace with your Nutritionix host domain and API endpoint
host_domain = "https://trackapi.nutritionix.com"
endpoint = "/v2/search/instant"  # Adjust the endpoint based on the API documentation

def get_calories(food_item):
    # Construct the complete API URL with the "query" parameter
    api_url = f"{host_domain}{endpoint}?query={food_item}&appId={app_id}&appKey={app_key}"
    response = requests.get(api_url)

    # Parse the API response to extract calories
    try:
        data = response.json()
        first_hit = data['hits'][0]['fields']
        calories = first_hit["nf_calories"]  # Replace with the actual field name for calories
        return calories
    except (KeyError, ValueError, IndexError):
        print(f"Could not get calories for {food_item}")
        return 0

def save_to_spreadsheet(date, time, meal_type, food_items, total_calories, notes):
    wb = Workbook()
    ws = wb.active
    ws.append(["Date", "Time", "Meal Type", "Food Items", "Total Calories", "Notes"])
    ws.append([date, time, meal_type, ', '.join(food_items), total_calories, notes])
    wb.save("calorie_journal.xlsx")

def main():
    total_calories = 0
    food_items = []

    while True:
        food = input("Enter a food item (or 'done' to finish): ")

        if food.lower() == 'done':
            break

        calories = get_calories(food)
        total_calories += calories
        food_items.append(food)
        print(f"Calories in {food}: {calories}")

    date = input("Enter the date (e.g., YYYY-MM-DD): ")
    time = input("Enter the time of consumption (e.g., HH:MM AM/PM): ")
    meal_type = input("Enter the meal type (e.g., Breakfast, Lunch, Dinner): ")
    notes = input("Enter any notes (optional): ")

    save_to_spreadsheet(date, time, meal_type, food_items, total_calories, notes)
    print(f"Total calories for {date}: {total_calories}")

if __name__ == "__main__":
    main()
    app.run(debug =True)