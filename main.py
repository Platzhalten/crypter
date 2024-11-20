import string
import random
import secrets
import FreeSimpleGUI as sg

from settings import get_settings as get_settings

buchstaben_list = []

string_list = string.printable[0:-4]

for i in string_list:
    buchstaben_list.append(i)

class Key:

    def __init__(self, key: str):

        self.key_list = None
        self.key = key

        self.last_save_token = secrets.token_urlsafe(1)[0]
        random.seed(f"{self.key[::2]} {self.last_save_token}")
        self.save_key_range = random.choice(get_settings(["crypt", "save_key_bytes_range"]))


        self.save_key = secrets.token_urlsafe(self.save_key_range) + self.last_save_token
        self.key_change = key
        self.save_key_change = self.save_key

        random.seed(key)

        self.random_buchstaben = buchstaben_list.copy()
        random.shuffle(self.random_buchstaben)

    def __getitem__(self, item):
        return self.random_buchstaben[item]

    def getitem(self, item):
        return self.random_buchstaben.index(item)

    def shuffle(self, save_key: str = None):

        if save_key is not None:
            self.save_key_change = save_key

        random.seed(f"{self.key_change} {self.save_key_change}")

        self.key_change = self.key_change + str(random.random())

        temp_list = buchstaben_list.copy()
        random.shuffle(temp_list)

        self.random_buchstaben = temp_list.copy()

    def reset(self):
        self.key_change = self.key
        self.save_key_change = self.save_key

    def newsaveKey(self):
        self.last_save_token = secrets.token_urlsafe(1)[0]
        random.seed(f"{self.key[::2]} {self.last_save_token}")
        self.save_key_range = random.choice(get_settings(["crypt", "save_key_bytes_range"]))

        self.save_key = secrets.token_urlsafe(self.save_key_range) + self.last_save_token


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

    verschluselt.append(key.save_key)

    key.newsaveKey()

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

layout = [[sg.T("Enter the Key here"), sg.Input(key="key-key"), sg.Button(button_text="Enter", key="key-enter")],
          [sg.T("Decrypt              "), sg.InputText(key="dec-text", disabled=True), sg.Button(button_text="Enter", key="dec-enter", disabled=True)],
          [sg.T("Decrypted           "), sg.Input(key="dec-text2", disabled=True)],
          [sg.T("Encrypt              "), sg.Input(key="enc-text", disabled=True), sg.Button(button_text="Enter", key="enc-enter", disabled=True)],
          [sg.T("Encrypted           "), sg.Input(key="enc-text2", disabled=True)]]

w = sg.Window(title="gf", layout=layout)

while True:

    e, v = w.read()

    if e is None:
        w.close()
        break


    if e == "key-enter":
        key = Key(v["key-key"])


        for i in ["enc-text", "enc-enter", "enc-text2", "dec-text", "dec-text2", "dec-enter"]:
            w[i].update(disabled=False)

        w["key-key"].update(password_char="*", disabled=True)

        w["key-enter"].update(disabled=True)


    if e == "enc-enter":
        wert = encrypt(v["enc-text"])
        w["enc-text2"](wert)

    if e == "dec-enter":
        wert = crypt(v["dec-text"])

        w["dec-text2"](wert)
