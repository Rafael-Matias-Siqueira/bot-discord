import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['db-bot']

users = db['usuario']


def criar_usuario(user_id, name):
    if users.find_one({"_id": user_id}):
        return False

    users.insert_one({
        "_id": int(user_id),
        "name": name,
        "xp": 0,
        "dinheiro": 0
    })

    print("salvou no banco")
    return True

def pegar_usuario(user_id):
    return users.find_one({
        "_id": int(user_id),
    })

def pegar_dinheiro(user_id):
    user_id = int(user_id)
    users.update_one(
        {
            "_id": user_id},
            {
            "$inc":{
                "dinheiro": 100
            }},
            upsert=True
        )
    usuario = users.find_one({"_id": user_id})
    return usuario["dinheiro"]

