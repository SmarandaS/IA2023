from nltk.corpus import wordnet as wn
import random
import tkinter as tk
from tkinter import font, filedialog
import nltk
nltk.download('wordnet')


def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', '-'))
    return list(synonyms)

def get_hypernyms(word):
    hypernyms = set()
    for syn in wn.synsets(word):
        for hypernym in syn.hypernyms():
            hypernym_lemma = hypernym.name().split('.')[0].replace('_', '-')
            hypernyms.add(hypernym_lemma)
    return list(hypernyms)

def load_text_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            text_input.delete(1.0, tk.END)
            text_input.insert(tk.END, file.read())


def replace_with_synonyms():
    original_text = text_input.get("1.0", tk.END)
    words = original_text.split()
    new_text = []

    for word in words:
        if len(word) > 3:
            synonyms = get_synonyms(word)

            if synonyms:
                 synonym = random.choice(synonyms)
                 new_text.append(synonym)

            else:
                new_text.append(word)
        else:
            new_text.append(word)

    modified_text.delete(1.0, tk.END)
    modified_text.insert(tk.END, ' '.join(new_text))

def replace_with_hypernyms():
    original_text = text_input.get("1.0", tk.END)
    words = original_text.split()
    new_text = []

    for word in words:
        if len(word) > 3:

            hypernyms = get_hypernyms(word)
            if hypernyms:
                hypernym = random.choice(hypernyms)
                new_text.append(hypernym)
            else:
                new_text.append(word)
        else:
            new_text.append(word)

    modified_text.delete(1.0, tk.END)
    modified_text.insert(tk.END, ' '.join(new_text))


root = tk.Tk()
root.title("Wordnet Rephrase Interface")
root.configure(bg='white')

app_font = font.Font(family="Poppins", size=10)
title_font = font.Font(family="Poppins", size=14, weight="bold")
root.option_add("*Font", app_font)

text_input_label = tk.Label(root, text="Enter your text or load from a file:", font=title_font)
text_input_label.pack(pady=(20, 0))

text_input = tk.Text(root, height=10)
text_input.pack()

load_file_button = tk.Button(root, text="Load Text File", command=load_text_file)
load_file_button.pack(pady=5)


rephrase_button = tk.Button(root, text="Rephrase text using synonyms", command=replace_with_synonyms)
rephrase_button.pack(pady=10)

rephrase_button2 = tk.Button(root, text="Rephrase text using hypernyms", command=replace_with_hypernyms)
rephrase_button2.pack(pady=10)


modified_text_label = tk.Label(root, text="Modified Text:", font=title_font)
modified_text_label.pack(pady=(20, 0))

modified_text = tk.Text(root, height=10)
modified_text.pack()

root.mainloop()
