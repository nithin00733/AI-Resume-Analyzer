import tkinter as tk
from tkinter import scrolledtext, messagebox

skills_database = [
    "python", "java", "c++", "sql",
    "html", "css", "javascript",
    "machine learning", "ai",
    "git", "github"
]

def analyze_resume():
    resume = resume_text.get("1.0", tk.END).lower()

    if not resume.strip():
        messagebox.showwarning("Warning", "Please enter resume text.")
        return

    found_skills = []

    for skill in skills_database:
        if skill in resume:
            found_skills.append(skill)

    score = min(len(found_skills) * 10, 100)

    missing_skills = [
        skill for skill in skills_database
        if skill not in found_skills
    ]

    result = f"Resume Score: {score}/100\n\n"

    result += "Detected Skills:\n"
    for skill in found_skills:
        result += f"✔ {skill}\n"

    result += "\nSuggested Skills:\n"
    for skill in missing_skills[:5]:
        result += f"✖ {skill}\n"

    result += "\nFeedback:\n"

    if score >= 70:
        result += "Excellent Resume!"
    elif score >= 40:
        result += "Good Resume. Add more technical skills."
    else:
        result += "Needs Improvement."

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)


root = tk.Tk()
root.title("AI Resume Analyzer")
root.geometry("800x600")

title = tk.Label(
    root,
    text="AI Resume Analyzer",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

resume_label = tk.Label(
    root,
    text="Paste Resume Text Below:"
)
resume_label.pack()

resume_text = scrolledtext.ScrolledText(
    root,
    width=80,
    height=15
)
resume_text.pack(pady=10)

analyze_btn = tk.Button(
    root,
    text="Analyze Resume",
    font=("Arial", 12),
    command=analyze_resume
)
analyze_btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(
    root,
    width=80,
    height=15
)
output_box.pack(pady=10)

root.mainloop()
