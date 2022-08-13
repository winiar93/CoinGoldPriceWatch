from flask import Flask, render_template
from rejson import Client, Path
import redis
import pandas as pd

try:
    client = Client(host='rejson', port=6379, decode_responses=True)
    print("connected to redis")
except Exception as e:
    print(f"{e}")

app = Flask(__name__)

headings = ("Mint", "Coin type", "Price")

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

def get_redis_data():
    tmp_data_list = []
    keys_list = client.keys()
    for k in keys_list:
        tmp_data_list.append(client.jsonget(k, Path.rootPath()))
    
    df = pd.DataFrame(tmp_data_list)
    df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Go to coin</a>')
    df['Price'] = df['Price'].astype(float)
    df.sort_values(by=['Price'], inplace=True)


    table = df.to_html(index=False, escape=False)
    return table



@app.route('/')
def hello():
    table = get_redis_data()
    return render_template("table.html", table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)