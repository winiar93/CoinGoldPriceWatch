from flask import Flask
from redis import Redis

app = Flask(__name__)
try:
    redis = Redis(host='redis://redis-master.default.svc.cluster.local', port=6379)
    print("connected to redis")
except Exception as e:
    print(f"{e}")

@app.route('/')
def hello():
    
    return f"""Hello World! \n 
    Canadian Maple Leaf - {str(redis.get('Canadian Maple Leaf'))} \n
    Krugerrands  - {str(redis.get('Krugerrands'))}  \n 
    Vienna Philharmonic - {str(redis.get('Vienna Philharmonic'))} \n
    Australian Kangaroo - {str(redis.get('Australian Kangaroo'))}
    
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)