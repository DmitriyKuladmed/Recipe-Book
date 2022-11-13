from flask import Flask, request, redirect
from flask_sqlalchemy import *
from flask import render_template
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipe.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(30), nullable=True)
    cooking_time = db.Column(db.String(10), nullable=False)
    time_type = db.Column(db.String(12), nullable=False)
    description = db.Column(db.Text)
    key = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Recipe %r>' %self.id


@app.route('/')
@app.route('/recipes')
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


@app.route('/recipes/<int:id>')
def recipe_detail(id):
    recipe = Recipe.query.get(id)
    return render_template("recipe_detail.html", recipe=recipe)


@app.route('/favorites/<int:id>')
def favorites_detail(id):
    recipe = Recipe.query.get(id)
    return render_template("favorite_detail.html", recipe=recipe)


@app.route('/recipes/<int:id>/add-to-favorites')
def add_to_favorites(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.key == False:
        recipe.key = True

    try:
        db.session.commit()
        return redirect('/recipes')

    except:
        return 'При добавлении рецепта в Избранное произошла ошибка'


@app.route('/favorites')
def favorite():
    list = []
    recipes = Recipe.query.all()
    for i in recipes:
        if i.key == True:
            list.append(i)
    return render_template("favorites.html", recipes=list)


@app.route('/favorites/<int:id>/delete')
def favorite_delete(id):
    recipe = Recipe.query.get_or_404(id)

    try:
        recipe.key = False
        db.session.commit()
        return redirect('/favorites')

    except:
        return 'При удалении рецепта произошла ошибка'


@app.route('/recipes/<int:id>/delete')
def recipe_delete(id):
    recipe = Recipe.query.get_or_404(id)

    try:
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/recipes')

    except:
        return 'При удалении рецепта произошла ошибка'


@app.route('/recipes/<int:id>/update', methods=['POST', 'GET'])
def recipe_update(id):
    recipe = Recipe.query.get(id)
    if request.method == 'POST':
        recipe.recipe_name = request.form['recipe_name']
        recipe.cooking_time = request.form['cooking_time']
        recipe.time_type = request.form['time_type']
        recipe.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/recipes')
        except:
            return 'При обновлении рецепта произошла ошибка'
    else:
        recipe = Recipe.query.get(id)
        return render_template("recipe_update.html", recipe=recipe)


@app.route('/create-recipe', methods=['POST', 'GET'])
def createRecipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        cooking_time = request.form['cooking_time']
        time_type = request.form['time_type']
        description = request.form['description']

        recipe = Recipe(recipe_name=recipe_name, cooking_time=cooking_time, time_type=time_type, description=description)

        try:
            db.session.add(recipe)
            db.session.commit()
            return redirect('/')

        except:
            return 'При создании рецепта произошла ошибка'
    else:
        return render_template("create-recipe.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)