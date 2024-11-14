import string
import random
import secrets

buchstaben_list = []

string_list = string.printable[0:-4]

for i in string_list:
    buchstaben_list.append(i)

class Key:

    def __init__(self, key: str):

        self.key_list = None
        self.key = key
        self.end = secrets.token_urlsafe(2)

        self.key_change = key
        self.end_change = self.end

        random.seed(key)

        self.random_buchstaben = buchstaben_list.copy()
        random.shuffle(self.random_buchstaben)

    def __getitem__(self, item):
        return self.random_buchstaben[item]

    def getitem(self, item):
        return self.random_buchstaben.index(item)

    def shuffle(self, end: str = None):

        if end is not None:
            self.end_change = end

        random.seed(f"{self.key_change} {self.end_change}")

        self.key_change = self.key_change + str(random.random())

        temp_list = buchstaben_list.copy()
        random.shuffle(temp_list)

        print(temp_list)

        self.random_buchstaben = temp_list.copy()

    def reset(self):
        self.key_change = self.key
        self.end_change = self.end


key = Key(input("Was soll der Key sein? "))

def crypt(text: str) -> str:

    key.reset()

    verschluselt = []

    text = text.lower()
    random.seed(key.key)

    for i in text:

        key.shuffle()

        if random.random() <= 0.5:
            i = i.lower()
        else:
            i = i.upper()

        index = string.printable.index(i)

        last = key[index]

        verschluselt.append(last)

    verschluselt.append(key.end)

    return "".join(verschluselt)


def encrypt(text: str) -> str:

    key.reset()

    entschluselt = []

    random.seed(key.key)

    for i in text[:-3]:

        key.shuffle(text[-3:])

        index = key.getitem(i)

        last = buchstaben_list[index]

        entschluselt.append(last)

    return "".join(entschluselt).lower()


message  = input("Was soll Ent/Verschlüsselt werden?: ")

x = crypt(message)

print("Verschlüßelt: ", x)

x = encrypt(x)

print("Entschlüßelt: ", x)
