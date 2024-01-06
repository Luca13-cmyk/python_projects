from flask import Flask, request, jsonify
import pickle
import pandas as pd
import sklearn

app = Flask(__name__)

rede_neural = pickle.load(open('rede_neural_finalizado.sav', 'rb'))

# @app.route("/")
# def home():
#     return "Home"
#https://medium.com/swlh/how-to-host-your-flask-app-on-pythonanywhere-for-free-df8486eb6a42

@app.route("/get-result")
def get_result():

    income = request.args.get("income")
    age = request.args.get("age")
    loan = request.args.get("loan")
    novo_registro = [[float(income), float(age), float(loan)]]

    result = rede_neural.predict(novo_registro)

    resp = {
        "result": pd.Series(result).to_json(orient="values")
    }

    return jsonify(resp), 200


@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    # http://127.0.0.1:5000/get-user/12?extra=luca
    return jsonify(user_data), 200


if __name__ == "__main__":
    app.run(debug=True)