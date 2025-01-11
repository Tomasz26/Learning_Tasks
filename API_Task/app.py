from flask import Flask, render_template, request, redirect
import requests
import json
import csv

app = Flask(__name__)
csv_filename = "exchange_rates.csv"

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]['rates']
ask = {}

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        
        writer.writerow(["currency", "code", "bid", "ask"])

        for rate in rates:
            writer.writerow([rate['currency'], rate['code'], rate['bid'], rate['ask']])
            ask[rate['currency']] = {
                'ask': rate['ask']}
     
print(ask)

@app.route('/money', methods=['GET', 'POST'])
def message():
   if request.method == 'GET':
        print("We received GET")
        return render_template("money.html")
   
   elif request.method == 'POST':
        print("We received POST")
        currency_code = (request.form.get('currency'))
        quantity = float((request.form.get('quantity')))
       
        ask_rate = ask[currency_code]['ask']  
        total_price = ask_rate * quantity  
        result_message = f"You need to pay {total_price} PLN"

        print(f"calculated total price: {total_price} PLN")

        return render_template("money.html", result_message=result_message)

if __name__ == "__main__":
    app.run(debug=True)