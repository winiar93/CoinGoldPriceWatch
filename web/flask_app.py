from turtle import heading
from flask import Flask, render_template
from rejson import Client, Path
import redis
import pandas as pd

try:
    client = Client(host='localhost', port=6379, decode_responses=True)
    print("connected to redis")
except Exception as e:
    print(f"{e}")

app = Flask(__name__)

headings = ("Mint", "Coin type", "Price")

def get_redis_data():
    tmp_data_list = []
    keys_list = client.keys()
    for k in keys_list:
        tmp_data_list.append(client.json().get(k))
    



@app.route('/')
def hello():
    
    return render_template("table.html", headings=headings, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)