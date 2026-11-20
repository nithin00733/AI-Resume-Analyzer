import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re

# --------------------------------
# SKILLS DATABASE
# --------------------------------

SKILLS_DATABASE = [
    "python", "java", "c", "c++", "sql",
    "html", "css", "javascript",
    "machine learning", "deep learning",
    "artificial intelligence", "ai",
    "git", "github", "django", "flask",
    "data structures", "oop", "tkinter",
    "pandas", "numpy", "data analysis"
]


# --------------------------------
# SKILL DETECTION
# --------------------------------

def detect_skills(resume):
    found = []

    for skill in SKILLS_DATABASE:
        escaped_skill = re.escape(skill)
        escaped_skill = escaped_skill.replace(r"\ ", r"\s+")

        pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"

        if re.search(pattern, resume, re.IGNORECASE):
            found.append(skill)

    return found


# --------------------------------
# RESUME ANALYSIS
# --------------------------------

def analyze_resume():

    resume = resume_text.get("1.0", tk.END).strip()

    if not resume:
        messagebox.showwarning(
            "Warning",
            "Please enter your resume text."
        )
        return

    found_skills = detect_skills(resume)

    missing_skills = [
        skill for skill in SKILLS_DATABASE
        if skill not in found_skills
    ]

    total_skills = len(SKILLS_DATABASE)
    score = (len(found_skills) / total_skills) * 100

    # Build report
    result = f"""
RESUME ANALYSIS REPORT
{'=' * 40}

Keyword Coverage: {score:.1f}%

Skills Detected: {len(found_skills)}
Skills in Database: {total_skills}

{'=' * 40}
DETECTED SKILLS
{'=' * 40}
"""

    if found_skills:
        for skill in found_skills:
            result += f"\n  + {skill.title()}"
    else:
        result += "\n  No matching skills detected."

    result += f"""

{'=' * 40}
OPTIONAL SKILL SUGGESTIONS
{'=' * 40}
"""

    if missing_skills:
        for skill in missing_skills[:8]:
            result += f"\n  - {skill.title()}"
    else:
        result += "\n  No additional database skills to suggest."

    result += f"""

{'=' * 40}
FEEDBACK
{'=' * 40}

This report measures keyword coverage only.
It does not measure overall resume quality.

Include relevant skills only when you genuinely
have those skills.
"""

    output_box.configure(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result.strip())
    output_box.configure(state="disabled")

    score_label.config(
        text=f"Keyword Coverage: {score:.1f}%"
    )


# --------------------------------
# CLEAR FUNCTION
# --------------------------------

def clear_resume():

    resume_text.delete("1.0", tk.END)

    output_box.configure(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.configure(state="disabled")

    score_label.config(
        text="Keyword Coverage: --"
    )


# --------------------------------
# MAIN WINDOW
# --------------------------------

root = tk.Tk()
root.title("AI Resume Analyzer - Version 2")
root.geometry("900x750")
root.minsize(700, 600)
root.configure(bg="#f2f5f9")


# --------------------------------
# STYLING
# --------------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Title.TLabel",
    font=("Arial", 22, "bold"),
    background="#f2f5f9",
    foreground="#183153"
)

style.configure(
    "Action.TButton",
    font=("Arial", 11, "bold"),
    padding=10
)


# --------------------------------
# HEADER
# --------------------------------

title = ttk.Label(
    root,
    text="RESUME KEYWORD ANALYZER",
    style="Title.TLabel"
)
title.pack(pady=(20, 10))

subtitle = ttk.Label(
    root,
    text="Analyze resume text and identify technical skills",
    background="#f2f5f9",
    font=("Arial", 10)
)
subtitle.pack(pady=(0, 15))


# --------------------------------
# RESUME INPUT
# --------------------------------

input_frame = tk.LabelFrame(
    root,
    text=" Resume Text ",
    font=("Arial", 11, "bold"),
    bg="#f2f5f9",
    padx=10,
    pady=10
)
input_frame.pack(
    fill="both",
    padx=25,
    pady=10
)

resume_text = scrolledtext.ScrolledText(
    input_frame,
    height=10,
    font=("Arial", 11),
    wrap=tk.WORD
)
resume_text.pack(
    fill="both",
    expand=True
)


# --------------------------------
# BUTTONS
# --------------------------------

button_frame = tk.Frame(
    root,
    bg="#f2f5f9"
)
button_frame.pack(pady=10)

analyze_btn = ttk.Button(
    button_frame,
    text="Analyze Resume",
    command=analyze_resume,
    style="Action.TButton"
)
analyze_btn.pack(
    side="left",
    padx=8
)

clear_btn = ttk.Button(
    button_frame,
    text="Clear Resume",
    command=clear_resume,
    style="Action.TButton"
)
clear_btn.pack(
    side="left",
    padx=8
)


# --------------------------------
# SCORE DISPLAY
# --------------------------------

score_label = tk.Label(
    root,
    text="Keyword Coverage: --",
    font=("Arial", 14, "bold"),
    bg="#f2f5f9",
    fg="#183153"
)
score_label.pack(pady=10)


# --------------------------------
# RESULT DISPLAY
# --------------------------------

result_frame = tk.LabelFrame(
    root,
    text=" Analysis Results ",
    font=("Arial", 11, "bold"),
    bg="#f2f5f9",
    padx=10,
    pady=10
)
result_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)

output_box = scrolledtext.ScrolledText(
    result_frame,
    height=12,
    font=("Consolas", 10),
    wrap=tk.WORD,
    state="disabled"
)
output_box.pack(
    fill="both",
    expand=True
)


# --------------------------------
# RUN APPLICATION
# --------------------------------

root.mainloop()