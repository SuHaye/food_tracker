from flask import Blueprint, render_template, request, redirect, url_for 

from food_tracker.models import Food, Log
from food_tracker.extensions import db


from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    logs = Log.query.order_by(Log.date.desc()).all()

    log_dates = []
    
    for log in logs: # Calculates totals, outter loop over each log in database
        proteins = 0
        carbs = 0
        fats = 0 
        calories = 0 

        for food in log.foods: #Loop over each food in the log and update values
            proteins += food.proteins
            carbs += food.carbs
            fats += food.fats
            calories += food.calories

        log_dates.append({ #pin values to dictionary and send to 'log_dates' list
            'log_date' : log,
            'proteins' : proteins,
            'carbs' : carbs,
            'fats' : fats,
            'calories' : calories
        })

    return render_template('index.html', log_dates=log_dates)

@main.route('/create_log', methods=['POST'])
def create_log():
    date = request.form.get('date') # Grabs the date of when created
    log = Log(date=datetime.strptime(date, '%Y-%m-%d')) # Decide format of data
    
    # Adds log model to database with user data
    db.session.add(log)
    db.session.commit()


    return redirect(url_for('main.view', log_id=log.id))


@main.route('/add')
def add():
    # list of all foods in database
    foods = Food.query.all()

    return render_template('add.html', foods=foods, food=None)


# Linked to form that's submited, this method is ran when submitted
@main.route('/add', methods=['POST'])
def add_post():
    # defines where each variable is grabbed from in form
    food_name = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbs = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    # linked to hidden input for updating food when editting
    food_id = request.form.get('food-id')

    if food_id:
        # updates existing food if it is there
        food = Food.query.get_or_404(food_id)
        food.name = food_name
        food.proteins = proteins
        food.carbs = carbs
        food.fats = fats

    else:
        # creates instance of food model 
        new_food = Food(
            name=food_name,
            proteins=proteins,
            carbs=carbs,
            fats=fats
        )
        db.session.add(new_food) #pushes instance of food model
    db.session.commit()      #into the database
    
    # redirects user to this page when submitted
    return redirect(url_for('main.add'))


@main.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    # finds where id equals in database and removes
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()

    return redirect(url_for('main.add'))


@main.route('/edit_food/<int:food_id>')
def edit_food(food_id):
    # sets food and imports it into add.html
    food = Food.query.get_or_404(food_id)
    # list of all foods in database
    foods = Food.query.all()
    return render_template('add.html', food=food, foods=foods)


@main.route('/view/<int:log_id>')
def view(log_id):
    # Grabbing data values to display on html pages
    log = Log.query.get_or_404(log_id)
    foods = Food.query.all()

    # Calculate total macro/micronutrients for the selected day
    totals = {
        'protein' : 0,
        'carbs' : 0,
        'fats' : 0,
        'calories' : 0
    }
    
    for food in log.foods:
        totals['protein'] += food.proteins # '+=' updates values
        totals['carbs'] += food.carbs
        totals['fats'] += food.fats
        totals['calories'] += food.calories

    return render_template('view.html', foods=foods, log=log, totals=totals)


@main.route('/add_food_to_log/<int:log_id>', methods=['POST'])
def add_food_to_log(log_id):
    log = Log.query.get_or_404(log_id)

    selected_food = request.form.get('food-select')  # Grab food from dropdown labeled 'food-select'
    food = Food.query.get_or_404(int(selected_food)) # Queries equivilent food to the food_id
    
    log.foods.append(food) # Adds selected food to log model in database
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))



@main.route('/remove_food_from_log/<int:log_id>/<int:food_id>')
def remove_food_from_log(log_id, food_id):
    log = Log.query.get(log_id)
    food = Food.query.get(food_id)
    # Removes food from database
    log.foods.remove(food)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))
