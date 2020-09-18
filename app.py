from flask import Flask, jsonify
from flasgger import Swagger
import json

app = Flask(__name__)

swagger = Swagger(app)

@app.route('/lunch', methods=('GET',))
def lunch():
    """
    Reads recipes and ingredients data and returns JSON with available recipes.
    Ingredients past their use-by are excluded. Recipes with ingredients before 
    their use-by but past their best-before are placed at the bottom of the list.
    ---

    definitions: 
        Recipe:
            type: object
            properties:
                title:
                    type: string
                ingredients:
                    type: array
                    items:
                        type: string

    responses:
        200:
            description: A list of available recipes
            schema:
                recipes:
                    type: array
                    items:
                        $ref: '#/definitions/Recipe'

    """
    #Read json data

    #Remove ingredients past their use-by

    #Determine what recipes can be made, and whether they are past best before date

    #Return recipe list

    return jsonify({"Hello":"World"})

app.run(debug=True)
