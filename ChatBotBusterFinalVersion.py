import json
import tkinter as tk
from tkinter import font, messagebox
from nltk.corpus import wordnet as wn
import random
import nltk
nltk.download('wordnet')


def load_data(filename='C:\\Users\\smara_9yjfm5z\\Downloads\\chatgpt.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', '-'))
    return list(synonyms)


def calculate_similarity_score(text1, text2):
    words1 = text1.lower().split()
    words2 = text2.lower().split()

    synonym_matches = 0

    for word2 in words2:
        synonym_found = False
        for word1 in words1:
            if word2 == word1 or word2 in get_synonyms(word1):
                synonym_found = True
                break
        if synonym_found:
            synonym_matches += 1

    if len(words2) > 0:
        similarity_score = (synonym_matches / len(words2)) * 100
    else:
        similarity_score = 0

    return similarity_score


def display_random_question():
    global current_entry
    current_entry = random.choice(questions_and_answers)
    question_var.set(current_entry['question'])


def on_calculate_similarity():
    user_answer1 = text_input.get("1.0", tk.END).strip()
    user_answer2 = text_input2.get("1.0", tk.END).strip()
    max_sim_first = 0
    max_sim_second = 0
    if user_answer1 and user_answer2:
        for answer in current_entry['chatgpt_answers']:
            if calculate_similarity_score(user_answer1, answer) > max_sim_first:
                max_sim_first = calculate_similarity_score(user_answer1, answer)
            if calculate_similarity_score(user_answer2, answer) > max_sim_second:
                max_sim_second = calculate_similarity_score(user_answer2, answer)

        similarity_percentage.config(text=f"GPT-generated scores:\nAnswer 1: {max_sim_first:.2f}%\nAnswer 2: {max_sim_second:.2f}%\nHuman-generated scores:\nAnswer 1: {100-max_sim_first:.2f}%\nAnswer 2: {100-max_sim_second:.2f}%")

    else:
        messagebox.showinfo("Error", "Please enter both answers before calculating similarity.")


root = tk.Tk()
root.title("GPT checker")
root.configure(bg='white')

# Define fonts
app_font = font.Font(family="Poppins", size=10)
title_font = font.Font(family="Poppins", size=14, weight="bold")
root.option_add("*Font", app_font)

question_var = tk.StringVar(root)
tk.Label(root, textvariable=question_var, font=title_font, wraplength=400).pack(pady=(20, 0))

text_input_label = tk.Label(root, text="Enter your first text:", font=title_font)
text_input_label.pack(pady=(20, 0))

text_input = tk.Text(root, height=10)
text_input.pack()

text_input_label2 = tk.Label(root, text="Enter your second text:", font=title_font)
text_input_label2.pack(pady=(20, 0))

text_input2 = tk.Text(root, height=10)
text_input2.pack()

rephrase_button = tk.Button(root, text="Calculate GPT-generated scores", command=on_calculate_similarity)
rephrase_button.pack(pady=10)

similarity_percentage = tk.Label(root, text="GPT-generated scores will be shown here.", font=title_font)
similarity_percentage.pack(pady=(20, 0))

questions_and_answers = load_data()
display_random_question()

root.mainloop()

