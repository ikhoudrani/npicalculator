import tkinter as tk
import requests

def calculate_expression():
    try:
        expression = entry.get()
        response = requests.post("http://localhost:8000/calculate", json={"expression": expression})
        response.raise_for_status() 
        result.set(f"Résultat : {response.json().get('result')}")
    except requests.RequestException as e:
        result.set(f"Erreur: {e}")

def append_to_expression(symbol):
    entry.insert(tk.END, symbol)

root = tk.Tk()
root.title("Calculatrice NPI")
root.geometry("400x500")

# Configuration de la grille
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

entry = tk.Entry(root)
entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

result = tk.StringVar()
result_label = tk.Label(root, textvariable=result)
result_label.grid(row=1, column=0, columnspan=4, sticky="nsew")

def delete_last_char():
    entry.delete(len(entry.get())-1, tk.END)

# Ajout des boutons
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), (' ', 5, 1), ('Del', 5, 2), ('+', 5, 3)
]

for (text, row, column) in buttons:
    if text == "Del":
        button = tk.Button(root, text=text, command=delete_last_char)
    else:
        button = tk.Button(root, text=text, command=lambda t=text: append_to_expression(t))
    button.grid(row=row, column=column, sticky="nsew")


calculate_button = tk.Button(root, text="Calculer", command=calculate_expression)
calculate_button.grid(row=6, column=0, columnspan=4, sticky="nsew")

# Poids pour redimensionnement
for i in range(7):
    root.rowconfigure(i, weight=1)

root.mainloop()
