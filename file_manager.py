import json

with open("data/users.json", "r", encoding="utf-8") as file:
    user = json.load(file)

print(user)


with open("data/books.json", "r",encoding = "utf-8") as file:
    data_1 = json.load(file)


users = {user["id"] : user
         for user in data_1}

print(users)
