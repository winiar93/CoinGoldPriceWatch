import redis
from redis.commands.json.path import Path

client = redis.Redis(host='localhost', port=6379, db=0)

jane = {
     'name': "Jane", 
     'Age': 33, 
     'Location': "Chawton"
   }

client.json().set('person:1', Path.rootPath(), jane)

result = client.json().get('person:1')
print(result)
