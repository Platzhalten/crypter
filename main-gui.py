import FreeSimpleGUI as sg

layout = [[sg.T("fwfa")]]


w = sg.Window(title="MAGIE", layout=layout)

while True:

    e, v = w.read()

    if e is None:
        w.close()
        break

