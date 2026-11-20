
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import re
from datetime import datetime


# -------------------- COLOUR THEME --------------------

BG = "#F3F5FB"
NAVY = "#172554"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
GREEN = "#059669"
ORANGE = "#EA580C"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"


# -------------------- SKILL DATABASE --------------------

SKILLS = {
    "Python": [r"\bpython\b"],
    "Java": [r"\bjava\b"],
    "C": [r"\bc\b"],
    "C++": [r"\bc\+\+\b"],
    "SQL": [r"\bsql\b"],
    "HTML": [r"\bhtml\b"],
    "CSS": [r"\bcss\b"],
    "JavaScript": [r"\bjavascript\b"],
    "Machine Learning": [r"\bmachine learning\b"],
    "Deep Learning": [r"\bdeep learning\b"],
    "Artificial Intelligence": [
        r"\bartificial intelligence\b", r"\bai\b"
    ],
    "Git": [r"\bgit\b"],
    "GitHub": [r"\bgithub\b"],
    "Django": [r"\bdjango\b"],
    "Flask": [r"\bflask\b"],
    "Data Structures": [r"\bdata structures?\b"],
    "OOP": [r"\boop\b", r"\bobject oriented programming\b"],
    "Tkinter": [r"\btkinter\b"],
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "Data Analysis": [r"\bdata analysis\b"],
    "NLP": [r"\bnlp\b", r"\bnatural language processing\b"],
    "Scikit-learn": [r"\bscikit.learn\b", r"\bsklearn\b"],
    "TensorFlow": [r"\btensorflow\b"],
    "PyTorch": [r"\bpytorch\b"],
    "REST API": [r"\brest api\b", r"\brestful api\b"],
    "MongoDB": [r"\bmongodb\b"],
    "MySQL": [r"\bmysql\b"],
    "PostgreSQL": [r"\bpostgresql\b"],
    "Linux": [r"\blinux\b"]
}


# -------------------- MAIN APPLICATION --------------------

class ResumeAnalyzer:

    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Analyzer | Professional Edition")
        self.root.geometry("1150x780")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.last_report = ""

        self.setup_style()
        self.create_interface()

    # -------------------- STYLE --------------------

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=30,
            fieldbackground=WHITE,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold")
        )

    # -------------------- INTERFACE --------------------

    def create_interface(self):

        # Main layout
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(self.main, bg=NAVY, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="RESUME",
            font=("Segoe UI", 23, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(anchor="w", padx=22, pady=(35, 0))

        tk.Label(
            sidebar,
            text="ANALYZER",
            font=("Segoe UI", 23, "bold"),
            bg=NAVY,
            fg="#60A5FA"
        ).pack(anchor="w", padx=22)

        tk.Frame(sidebar, bg="#334155", height=2).pack(
            fill="x", padx=20, pady=25
        )

        self.sidebar_item(sidebar, "  Dashboard", "#60A5FA")
        self.sidebar_item(sidebar, "  Skill Detection", "#A78BFA")
        self.sidebar_item(sidebar, "  Job Matching", "#34D399")
        self.sidebar_item(sidebar, "  Report Export", "#FBBF24")

        tk.Label(
            sidebar,
            text="PROJECT VERSION 3.0",
            font=("Segoe UI", 9, "bold"),
            bg=NAVY,
            fg="#94A3B8"
        ).pack(side="bottom", pady=25)

        # Main content
        content = tk.Frame(self.main, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        # Scrollable content area
        canvas = tk.Canvas(content, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            content, orient="vertical", command=canvas.yview
        )

        self.page = tk.Frame(canvas, bg=BG)

        self.page.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0), window=self.page, anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(
                canvas_window, width=e.width
            )
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            )
        )

        self.create_dashboard()

    def sidebar_item(self, parent, text, color):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=NAVY,
            fg=color,
            anchor="w"
        ).pack(fill="x", padx=22, pady=13)

    # -------------------- DASHBOARD --------------------

    def create_dashboard(self):

        # Heading
        header = tk.Frame(self.page, bg=BG)
        header.pack(fill="x", padx=30, pady=(28, 15))

        tk.Label(
            header,
            text="Resume Dashboard",
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Analyze your technical skills and compare them with a job description.",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=5)

        # Metric cards
        cards = tk.Frame(self.page, bg=BG)
        cards.pack(fill="x", padx=25, pady=12)

        self.metric_labels = {}

        metrics = [
            ("Detected Skills", "0", BLUE),
            ("Database Coverage", "0%", PURPLE),
            ("Job Match", "N/A", GREEN)
        ]

        for title, value, color in metrics:
            card = tk.Frame(
                cards,
                bg=WHITE,
                highlightbackground="#E2E8F0",
                highlightthickness=1
            )
            card.pack(
                side="left", fill="both", expand=True,
                padx=6, ipady=15
            )

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=MUTED
            ).pack(anchor="w", padx=15, pady=(8, 5))

            value_label = tk.Label(
                card,
                text=value,
                font=("Segoe UI", 23, "bold"),
                bg=WHITE,
                fg=color
            )
            value_label.pack(anchor="w", padx=15)

            self.metric_labels[title] = value_label

        # Resume input section
        self.create_section_title(
            self.page, "01  |  Resume Information"
        )

        resume_card = tk.Frame(self.page, bg=WHITE)
        resume_card.pack(fill="x", padx=30, pady=8)

        tk.Label(
            resume_card,
            text="Paste your resume content below",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.resume_text = ScrolledText(
            resume_card,
            height=10,
            font=("Consolas", 10),
            wrap="word",
            bg="#F8FAFC",
            fg=TEXT,
            relief="flat",
            padx=12,
            pady=12,
            insertbackground=TEXT
        )
        self.resume_text.pack(
            fill="x", padx=15, pady=(0, 15)
        )

        # Job description section
        self.create_section_title(
            self.page, "02  |  Job Description (Optional)"
        )

        jd_card = tk.Frame(self.page, bg=WHITE)
        jd_card.pack(fill="x", padx=30, pady=8)

        self.jd_text = ScrolledText(
            jd_card,
            height=5,
            font=("Consolas", 10),
            wrap="word",
            bg="#F8FAFC",
            fg=TEXT,
            relief="flat",
            padx=12,
            pady=12,
            insertbackground=TEXT
        )
        self.jd_text.pack(
            fill="x", padx=15, pady=15
        )

        # Action buttons
        button_frame = tk.Frame(self.page, bg=BG)
        button_frame.pack(fill="x", padx=30, pady=18)

        self.create_button(
            button_frame, "ANALYZE RESUME",
            BLUE, self.analyze_resume
        )

        self.create_button(
            button_frame, "LOAD SAMPLE",
            PURPLE, self.load_sample
        )

        self.create_button(
            button_frame, "EXPORT REPORT",
            GREEN, self.export_report
        )

        self.create_button(
            button_frame, "CLEAR ALL",
            ORANGE, self.clear_all
        )

        # Results section
        self.create_section_title(
            self.page, "03  |  Analysis Results"
        )

        result_card = tk.Frame(self.page, bg=WHITE)
        result_card.pack(fill="both", padx=30, pady=8)

        self.result_text = ScrolledText(
            result_card,
            height=13,
            font=("Consolas", 10),
            wrap="word",
            bg="#F8FAFC",
            fg=TEXT,
            relief="flat",
            padx=15,
            pady=15,
            state="disabled"
        )
        self.result_text.pack(
            fill="both", expand=True, padx=15, pady=15
        )

        # Footer
        tk.Label(
            self.page,
            text="Developed with Python and Tkinter | Version 3.0",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED
        ).pack(pady=20)

    # -------------------- UI HELPERS --------------------

    def create_section_title(self, parent, title):
        tk.Label(
            parent,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w", padx=30, pady=(20, 5))

    def create_button(self, parent, text, color, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=NAVY,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=13,
            pady=11,
            command=command
        )
        btn.pack(side="left", padx=5)

    # -------------------- SKILL DETECTION --------------------

    def detect_skills(self, text):
        detected = []

        for skill, patterns in SKILLS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected.append(skill)
                    break

        return detected

    # -------------------- ANALYSIS --------------------

    def analyze_resume(self):

        resume = self.resume_text.get(
            "1.0", tk.END
        ).strip()

        job_description = self.jd_text.get(
            "1.0", tk.END
        ).strip()

        if not resume:
            messagebox.showwarning(
                "Missing Resume",
                "Please paste your resume before analysing."
            )
            return

        resume_skills = self.detect_skills(resume)

        total_skills = len(SKILLS)

        coverage = (
            len(resume_skills) / total_skills
        ) * 100

        # Job description matching
        jd_skills = self.detect_skills(job_description)

        if jd_skills:
            matched_skills = [
                skill for skill in resume_skills
                if skill in jd_skills
            ]

            missing_job_skills = [
                skill for skill in jd_skills
                if skill not in resume_skills
            ]

            job_match = (
                len(matched_skills) / len(jd_skills)
            ) * 100

            job_match_display = f"{job_match:.1f}%"
        else:
            matched_skills = []
            missing_job_skills = []
            job_match = None
            job_match_display = "N/A"

        # Update metric cards
        self.metric_labels["Detected Skills"].config(
            text=str(len(resume_skills))
        )

        self.metric_labels["Database Coverage"].config(
            text=f"{coverage:.1f}%"
        )

        self.metric_labels["Job Match"].config(
            text=job_match_display
        )

        # Report generation
        report = self.generate_report(
            resume_skills,
            coverage,
            job_match,
            jd_skills,
            matched_skills,
            missing_job_skills
        )

        self.last_report = report

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, report)
        self.result_text.config(state="disabled")

        messagebox.showinfo(
            "Analysis Complete",
            "Your resume analysis is complete!"
        )

    # -------------------- REPORT GENERATION --------------------

    def generate_report(
        self, resume_skills, coverage, job_match,
        jd_skills, matched_skills, missing_job_skills
    ):

        report = []

        report.append("=" * 55)
        report.append("             RESUME ANALYSIS REPORT")
        report.append("=" * 55)

        report.append(
            f"\nGenerated: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        )

        report.append("\n\n1. DETECTED TECHNICAL SKILLS")
        report.append("-" * 40)

        if resume_skills:
            report.append(", ".join(resume_skills))
        else:
            report.append("No supported skills detected.")

        report.append("\n\n2. DATABASE COVERAGE")
        report.append("-" * 40)
        report.append(
            f"{len(resume_skills)} out of {len(SKILLS)} skills detected."
        )
        report.append(f"Coverage: {coverage:.1f}%")

        report.append("\n\n3. JOB DESCRIPTION MATCH")
        report.append("-" * 40)

        if jd_skills:
            report.append(
                f"Job description skills: {len(jd_skills)}"
            )
            report.append(
                f"Matched skills: {len(matched_skills)}"
            )
            report.append(
                f"Job match: {job_match:.1f}%"
            )

            report.append(
                "\nMatched: " +
                (", ".join(matched_skills) or "None")
            )

            report.append(
                "\nSkills to review: " +
                (", ".join(missing_job_skills) or "None")
            )
        else:
            report.append(
                "No job description skills provided."
            )

        report.append("\n\n4. ADDITIONAL SKILLS TO EXPLORE")
        report.append("-" * 40)

        additional_skills = [
            skill for skill in SKILLS
            if skill not in resume_skills
        ]

        report.append(
            ", ".join(additional_skills)
            if additional_skills else "All listed skills detected."
        )

        report.append("\n\n5. IMPORTANT NOTE")
        report.append("-" * 40)
        report.append(
            "This tool uses keyword and rule-based matching."
        )
        report.append(
            "Database coverage is not a measure of resume quality."
        )
        report.append(
            "Job match is based only on detected supported keywords."
        )
        report.append(
            "Detected keywords do not prove actual skill proficiency."
        )

        report.append("\n" + "=" * 55)
        report.append("                 END OF REPORT")
        report.append("=" * 55)

        return "\n".join(report)

    # -------------------- SAMPLE DATA --------------------

    def load_sample(self):

        self.resume_text.delete("1.0", tk.END)
        self.jd_text.delete("1.0", tk.END)

        sample_resume = """
NITHIN R
Computer Science and Engineering - Artificial Intelligence

CAREER OBJECTIVE
Motivated computer science student interested in Python
programming, Artificial Intelligence and Machine Learning.

TECHNICAL SKILLS
Python, Java, SQL, HTML, CSS, JavaScript
Machine Learning, Artificial Intelligence
Data Structures, OOP, Tkinter
Pandas, NumPy, Git, GitHub

PROJECTS
AI Resume Analyzer using Python and Tkinter.
Developed a desktop application for technical skill detection.

EDUCATION
B.E. Computer Science and Engineering (AI)
"""

        sample_jd = """
JOB ROLE: Python AI Intern

Required Skills:
Python, Machine Learning, Artificial Intelligence,
SQL, Pandas, NumPy, Git, Data Analysis,
Deep Learning, NLP, Scikit-learn.
"""

        self.resume_text.insert(
            tk.END, sample_resume
        )

        self.jd_text.insert(
            tk.END, sample_jd
        )

        messagebox.showinfo(
            "Sample Loaded",
            "Sample resume and job description loaded."
        )

    # -------------------- EXPORT REPORT --------------------

    def export_report(self):

        if not self.last_report:
            messagebox.showwarning(
                "No Report",
                "Please analyse a resume before exporting."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Analysis Report"
        )

        if filename:
            try:
                with open(
                    filename, "w", encoding="utf-8"
                ) as file:
                    file.write(self.last_report)

                messagebox.showinfo(
                    "Export Successful",
                    "Your report has been saved successfully."
                )

            except OSError as error:
                messagebox.showerror(
                    "Export Error", str(error)
                )

    # -------------------- CLEAR --------------------

    def clear_all(self):

        self.resume_text.delete("1.0", tk.END)
        self.jd_text.delete("1.0", tk.END)

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

        self.metric_labels["Detected Skills"].config(text="0")
        self.metric_labels["Database Coverage"].config(text="0%")
        self.metric_labels["Job Match"].config(text="N/A")

        self.last_report = ""


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":

    root = tk.Tk()
    app = ResumeAnalyzer(root)
    root.mainloop()
