import tkinter as tk
from tkinter import *
import json


root = tk.Tk()

current_score = 0

current_question_index = 0

#öppnar JSON filen "questions.json"
with open("questions.json", encoding="utf-8") as f:
    data = json.load(f)
    

# Gör så att man bara kan klicka i ett svarsalternativ
def update_checkbuttons(option):
    if(option == 1):
        option2.set(0)
        option3.set(0)
        option4.set(0)
    elif(option == 2):
        option1.set(0)
        option3.set(0)
        option4.set(0)
    elif(option == 3):
        option1.set(0)
        option2.set(0)
        option4.set(0)
    elif(option == 4):
        option1.set(0)
        option2.set(0)
        option3.set(0)

#funktionen för knappen till nästa fråga
def next_question():
    save_answer()
    global current_question_index
    if current_question_index < len(data["questions"])-1:
        current_question_index +=1
        show_question()

#Deklarerar de olika texterna för de olika knapparna
def show_question():
    global current_question_index
    question_data = data["questions"][current_question_index]
    question_text = question_data["question"]
    option1_text = question_data["1"]
    option2_text = question_data["2"]
    option3_text = question_data["3"]
    option4_text = question_data["4"]

    #Initierar texten för de olika svaralternativen
    question_label.config(text=question_text)
    button1.config(text=option1_text, variable=option1, command=lambda: update_checkbuttons(1))
    button2.config(text=option2_text, variable=option2, command=lambda: update_checkbuttons(2))
    button3.config(text=option3_text, variable=option3, command=lambda: update_checkbuttons(3))
    button4.config(text=option4_text, variable=option4, command=lambda: update_checkbuttons(4))

    #Återställ valda alternativ baserat på user_answer
    option1.set(1 if question_data["user_answer"] == option1_text else 0)
    option2.set(1 if question_data["user_answer"] == option2_text else 0)
    option3.set(1 if question_data["user_answer"] == option3_text else 0)
    option4.set(1 if question_data["user_answer"] == option4_text else 0)

#funktion för knapp till föregående fråga
def previous_question():
    save_answer()
    global current_question_index
    if current_question_index > 0:
        current_question_index -=1
        show_question()

#funktion körs igång när man klickar på end_quiz så räknar den alla rätta svar
def end_quiz_popup():
    save_answer()
    score()
    with open("answers.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    popup()

#funktion som sparar alternativen
def save_answer():
    question_data = data["questions"][current_question_index]
    if option1.get() == 1:
        question_data["user_answer"] = question_data["1"]
    elif option2.get() == 1:
        question_data["user_answer"] = question_data["2"]
    elif option3.get() == 1:
        question_data["user_answer"] = question_data["3"]
    elif option4.get() == 1:
        question_data["user_answer"] = question_data["4"]
    else:
        question_data["user_answer"] = ""

#Funktion som sparar poäng om user:answer = question_answer
def score():
    global current_score
    current_score = 0
    for question in data["questions"]:
        if question["user_answer"] == question["correctanswer"]:
            current_score += 1

#funktion till slutprogrammet
def popup():
    global button_end_quiz
    global label
    global label_score
    popupwindow = Toplevel(root)
    popupwindow.title("Resultat")
    popupwindow.geometry("500x400")
    label = tk.Label(popupwindow, text="Detta är ditt slutgiltiga resultat", font=("Arial", 18))
    label_score = tk.Label(popupwindow, text=f"Rättsvar:{current_score} av 19", font=("Arial", 18))
    label.pack(padx=20, pady=20)
    label_score.pack(padx=20, pady=20)
    button_end_quiz = tk.Button(popupwindow, text="Avsluta", font=("Arial", 15),command=root.destroy)
    button_end_quiz.pack()
    popupwindow.mainloop()

option1=tk.IntVar()
option2=tk.IntVar()
option3=tk.IntVar()
option4=tk.IntVar()


root.geometry("600x700")
root.title("Körkortsprov")

#En gubbe som kör bil :)
label= tk.Label(root, text=""" 
__
~( @\   ]
__________]_[__/_>_____
/  ____ \ <>            |  ____  ]
=\_/ __ \_\_________|_/ __ \__D
______(__)_____________(__)____
""", font=("Arial", 10))
label.pack()

question_label = tk.Label(root, text="", font=("Arial", 12))
question_label.pack(padx=10, pady=10)

#Knapp1
button1 = tk.Checkbutton(root, font=("Arial", 10),variable=option1, command=lambda:update_checkbuttons(1))
button1.pack(padx=10, pady=10)

#Knapp2
button2 = tk.Checkbutton(root, font=("Arial", 10),variable=option2, command=lambda:update_checkbuttons(2))
button2.pack(padx=10, pady=10)

#Knapp3
button3 = tk.Checkbutton(root, font=("Arial", 10),variable=option3, command=lambda:update_checkbuttons(3))
button3.pack(padx=10, pady=10)

#Knapp4
button4 = tk.Checkbutton(root, font=("Arial", 10),variable=option4, command=lambda:update_checkbuttons(4))
button4.pack(padx=10, pady=10)

#Tillbaka-knapp
button = tk.Button(root, text="<-", font=("Arial", 10),command=previous_question)
button.pack(padx=10, pady=10)

#Framåt-knapp
button = tk.Button(root, text="->", font=("Arial", 10),command=next_question)
button.pack(padx=10, pady=10)

#Avsluta-knapp
button_end = tk.Button(root, text="Avsluta", font=("Arial", 10), command=end_quiz_popup)
button_end.pack(padx=10,pady=10)

show_question()
root.mainloop()
