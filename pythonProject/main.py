from flask import Flask, request, render_template_string, session
import requests

app = Flask(__name__)
app.secret_key = 'Hu61F59IuQ'  # Replace with a strong, randomly generated key

# Replace with your Nutritionix API details
app_id = "8bc7b25a"
app_key = "dd56c0e7590da1e3f54f9269de8b9588"
host_domain = "https://trackapi.nutritionix.com"

# HTML template for the home page with updated modern styling
HOME_PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>NutriScope: Nutrition Tracker</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background-color: #f4f4f4;
        color: #333;
        font-family: 'Arial', sans-serif;
      }
      .container {
        max-width: 800px;
        margin-top: 50px;
        background: #fff;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
      }
      h1 {
        color: #007bff;
        font-size: 2.5rem;
      }
      .form-control, .btn {
        border-radius: 0;
      }
      .btn-primary {
        background-color: #007bff;
        border-color: #007bff;
      }
      .nutrition-info, .calorie-info {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 10px;
        margin-top: 15px;
      }
      .btn-warning {
        background-color: #ffc107;
        border-color: #ffc107;
      }
      .btn-danger {
        background-color: #dc3545;
        border-color: #dc3545;
      }
    </style>
  </head>
  <body>
    <div class="container text-center">
      <h1>NutriScope</h1>
      <p class="lead">Your Personal Calorie Tracker</p>
      <form method="post" action="/get-calories" class="mt-4">
          <div class="form-group">
              <input type="text" id="food" name="food" class="form-control" placeholder="Enter a food item...">
              <input type="text" id="serving_size" name="serving_size" class="form-control mt-2" placeholder="Enter serving size (e.g., 2 oz)">
          </div>
          <button type="submit" class="btn btn-primary btn-lg">Get Nutritional Info</button>
      </form>

      {% if nutrition_info %}
        <div class="nutrition-info alert alert-info mt-3">
          <h4>Nutritional Information for {{ food_item }}</h4>
          <p>Calories: {{ nutrition_info['calories'] }} kcal</p>
          <p>Protein: {{ nutrition_info['protein'] }} g</p>
          <p>Carbs: {{ nutrition_info['carbs'] }} g</p>
          <p>Sugar: {{ nutrition_info['sugar'] }} g</p>
          <p>Fat: {{ nutrition_info['fat'] }} g</p>
          <form method="post" action="/add-nutrients">
              <input type="hidden" name="calories" value="{{ nutrition_info['calories'] }}">
              <input type="hidden" name="protein" value="{{ nutrition_info['protein'] }}">
              <input type="hidden" name="carbs" value="{{ nutrition_info['carbs'] }}">
              <input type="hidden" name="sugar" value="{{ nutrition_info['sugar'] }}">
              <input type="hidden" name="fat" value="{{ nutrition_info['fat'] }}">
              <button type="submit" class="btn btn-warning btn-lg mt-2">Add to Daily Total</button>
          </form>
        </div>
      {% endif %}

      <div class="calorie-info alert alert-info mt-3">
        <p>Daily Total Calories: <strong>{{ daily_totals.calories }}</strong></p>
        <p>Daily Total Protein: <strong>{{ daily_totals.protein }}g</strong></p>
        <p>Daily Total Carbs: <strong>{{ daily_totals.carbs }}g</strong></p>
        <p>Daily Total Sugar: <strong>{{ daily_totals.sugar }}g</strong></p>
        <p>Daily Total Fat: <strong>{{ daily_totals.fat }}g</strong></p>
        <form method="post" action="/reset-totals">
            <button type="submit" class="btn btn-danger btn-lg">Reset Daily Totals</button>
        </form>
      </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    if 'daily_totals' not in session:
        session['daily_totals'] = {'calories': 0, 'protein': 0, 'carbs': 0, 'sugar': 0, 'fat': 0}
    return render_template_string(HOME_PAGE_TEMPLATE, daily_totals=session['daily_totals'])

def get_nutritional_data(food_query):
    api_url = f"{host_domain}/v2/natural/nutrients"
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': app_id,
        'x-app-key': app_key
    }
    data = {'query': food_query}

    response = requests.post(api_url, headers=headers, json=data)
    try:
        data = response.json()
        first_food = data['foods'][0]
        return {
            'calories': first_food.get("nf_calories", 0),
            'protein': first_food.get("nf_protein", 0),
            'carbs': first_food.get("nf_total_carbohydrate", 0),
            'sugar': first_food.get("nf_sugars", 0),
            'fat': first_food.get("nf_total_fat", 0)
        }
    except (KeyError, IndexError, ValueError):
        return None

@app.route('/get-calories', methods=['POST'])
def get_calories():
    food_item = request.form['food']
    serving_size = request.form['serving_size']
    full_query = f"{serving_size} of {food_item}" if serving_size else food_item
    nutrition_info = get_nutritional_data(full_query)
    return render_template_string(HOME_PAGE_TEMPLATE, food_item=full_query, nutrition_info=nutrition_info, daily_totals=session.get('daily_totals', {}))

@app.route('/add-nutrients', methods=['POST'])
def add_nutrients():
    if 'daily_totals' not in session:
        session['daily_totals'] = {'calories': 0, 'protein': 0, 'carbs': 0, 'sugar': 0, 'fat': 0}
    
    nutrients = {
        'calories': request.form.get('calories', type=float, default=0),
        'protein': request.form.get('protein', type=float, default=0),
        'carbs': request.form.get('carbs', type=float, default=0),
        'sugar': request.form.get('sugar', type=float, default=0),
        'fat': request.form.get('fat', type=float, default=0)
    }

    for nutrient, value in nutrients.items():
        session['daily_totals'][nutrient] += value
    
    session.modified = True

    return render_template_string(HOME_PAGE_TEMPLATE, daily_totals=session['daily_totals'])

@app.route('/reset-totals', methods=['POST'])
def reset_totals():
    session['daily_totals'] = {'calories': 0, 'protein': 0, 'carbs': 0, 'sugar': 0, 'fat': 0}
    return render_template_string(HOME_PAGE_TEMPLATE, daily_totals=session['daily_totals'])

if __name__ == '__main__':
    app.run(debug=True)
