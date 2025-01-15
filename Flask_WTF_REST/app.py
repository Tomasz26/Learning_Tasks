from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response

from forms import ToWatchForm
from models import towatch

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/towatchs/", methods=["GET", "POST"])
def towatchs_list():
    form = ToWatchForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            towatch.create(form.data)
            towatch.save_all()
        return redirect(url_for("towatchs_list"))

    return render_template("towatchs.html", form=form, towatchs=towatch.all(), error=error)


@app.route("/towatchs/<int:towatch_id>/", methods=["GET", "POST"])
def towatch_details(towatch_id):
    selected_towatch = towatch.get(towatch_id)
    form = ToWatchForm(data=selected_towatch)

    if request.method == "POST":
        if form.validate_on_submit():
            towatch.update(towatch_id, form.data)
        return redirect(url_for("towatchs_list"))
    return render_template("towatch.html", form=form, towatch_id=towatch_id)

@app.route("/towatchs/random", methods=["GET"])
def random_movie():
    movie = towatch.choose_random_movie()
    form = ToWatchForm()
    return render_template("towatchs.html", form = form, movie=movie, towatchs=towatch.all()) 

@app.route("/api/v1/towatchs/", methods=["GET"])
def towatchs_list_api_v1():
    return jsonify(towatch.all())

@app.route("/api/v1/towatchs/<int:towatch_id>/", methods=["GET"])
def get_towatch(towatch_id):
    selected_towatch = towatch.get(towatch_id)
    if not selected_towatch:
        abort(404)
    return jsonify({"selected_towatch": selected_towatch})

@app.route("/api/v1/towatchs/", methods=["POST"])
def create_towatch():
    if not request.json or not 'title' in request.json:
        abort(400)
    created_towatch = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'submit': True,
        'done': False
    }
    towatch.create(created_towatch)
    return jsonify({'towatchs': created_towatch}), 201

@app.route("/api/v1/towatchs/<int:towatch_id>", methods=['DELETE'])
def delete_towatch(towatch_id):
    result = towatch.delete(towatch_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/towatchs/<int:towatch_id>", methods=["PUT"])
def update_todo(towatch_id):
    selected_towatch = towatch.get(towatch_id)
    if not selected_towatch:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    selected_towatch = {
        'title': data.get('title', selected_towatch['title']),
        'description': data.get('description', selected_towatch['description']),
        'done': data.get('done', selected_towatch['done']),
        'id': data.get('id', selected_towatch['id'])
    }
    towatch.update(towatch_id, selected_towatch)
    return jsonify({'selected_towatch': selected_towatch})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)