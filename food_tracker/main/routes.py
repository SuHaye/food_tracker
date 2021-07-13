from flask import Blueprint, render_template, request, redirect, url_for 

from food_tracker.models import Food
from food_tracker.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


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

    # linked to hidden input
    food_id = request.form.get('food-id')

    if food_id:
        # updates existing food if it is there
        food = Food.query.get(food_id)
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
    food = Food.query.get(food_id)
    db.session.delete(food)
    db.session.commit()

    return redirect(url_for('main.add'))



@main.route('/edit_food/<int:food_id>')
def edit_food(food_id):
    # sets food and imports it into add.html
    food = Food.query.get(food_id)
    # list of all foods in database
    foods = Food.query.all()
    return render_template('add.html', food=food, foods=foods)


@main.route('/view')
def view():
    return render_template('view.html')