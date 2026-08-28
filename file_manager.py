import json

with open("users.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)


with open("books.json", "r",encoding = "utf-8") as file:
    data_1 = json.load(file)


users = {user["id"] : user
         for user in data_1}

print(users)
