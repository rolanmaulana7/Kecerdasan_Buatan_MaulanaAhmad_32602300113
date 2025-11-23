import tkinter as tk
from tkinter import messagebox

# ====================== Fuzzy Functions ======================

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    return 0

def fuzzify(food, service):
    food_bad = triangular(food, 0, 0, 5)
    food_good = triangular(food, 5, 10, 10)

    service_poor = triangular(service, 0, 0, 5)
    service_excellent = triangular(service, 5, 10, 10)

    return food_bad, food_good, service_poor, service_excellent

def inference(food_bad, food_good, service_poor, service_excellent):
    rule1 = max(service_poor, food_bad)  # Low
    rule2 = min(service_excellent, food_good)  # High
    return rule1, rule2

def defuzzification(rule_low, rule_high):
    values = [i for i in range(0, 21)]
    numerator = 0
    denominator = 0

    for tip in values:
        low = min(rule_low, triangular(tip, 0, 0, 10))
        high = min(rule_high, triangular(tip, 10, 20, 20))
        membership = max(low, high)

        numerator += membership * tip
        denominator += membership

    return numerator / denominator if denominator != 0 else 0

def fuzzy_tip_system(food, service):
    food_bad, food_good, service_poor, service_excellent = fuzzify(food, service)
    rule_low, rule_high = inference(food_bad, food_good, service_poor, service_excellent)
    tip = defuzzification(rule_low, rule_high)
    return tip

# ====================== GUI Application ======================

def calculate_tip():
    try:
        food = float(entry_food.get())
        service = float(entry_service.get())

        if not (0 <= food <= 10 and 0 <= service <= 10):
            messagebox.showerror("Error", "Nilai harus antara 0 dan 10")
            return

        tip = fuzzy_tip_system(food, service)
        result_label.config(text=f"Tip: {tip:.2f}%")

    except ValueError:
        messagebox.showerror("Error", "Input harus berupa angka!")

# ====================== Window Setup ======================

window = tk.Tk()
window.title("Fuzzy Tip Calculator")
window.geometry("320x220")

label_food = tk.Label(window, text="Food Quality (0-10)")
label_food.pack()
entry_food = tk.Entry(window)
entry_food.pack()

label_service = tk.Label(window, text="Service Quality (0-10)")
label_service.pack()
entry_service = tk.Entry(window)
entry_service.pack()

button = tk.Button(window, text="Hitung Tip", command=calculate_tip)
button.pack(pady=10)

result_label = tk.Label(window, text="Tip: -", font=("Arial", 14))
result_label.pack()

window.mainloop()
