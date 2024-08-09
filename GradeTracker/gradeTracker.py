import tkinter as tk
from tkinter import messagebox
import os


class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}

    def add_grade(self, subject, grade):
        if subject in self.grades:
            self.grades[subject].append(grade)
        else:
            self.grades[subject] = [grade]

    def calculate_average(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return total / count if count != 0 else 0

    def to_string(self):
        grades_str = ';'.join([f"{subject}:{','.join(map(str, grades))}" for subject, grades in self.grades.items()])
        return f"{self.name}|{grades_str}"

    @staticmethod
    def from_string(data_str):
        parts = data_str.split("|")
        name = parts[0]
        student = Student(name)
        if len(parts) > 1:
            grade_data = parts[1].split(';')
            for subject_data in grade_data:
                subject, grades = subject_data.split(':')
                student.grades[subject] = list(map(float, grades.split(',')))
        return student


class GradeTrackerApp:
    def __init__(self, root):
        self.student = {}
        self.root = root
        self.root.title("Student Grade Tracker")

        # loading existing data
        self.load_data()

        # Main frame
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Widgets for adding a new student
        self.name_label = tk.Label(self.frame, text="Student Name: ")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_student_btn = tk.Button(self.frame, text="Add Student", command=self.add_student)
        self.add_student_btn.grid(row=0, column=2, padx=5, pady=5)

        # Widgets for adding subjects
        self.subject_label = tk.Label(self.frame, text="Subject:")
        self.subject_label.grid(row=1, column=0, padx=5, pady=5)
        self.subject_entry = tk.Entry(self.frame)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)

        # Widgets for adding grade
        self.grade_label = tk.Label(self.frame, text="Grade:")
        self.grade_label.grid(row=2, column=0, padx=5, pady=5)
        self.grade_entry = tk.Entry(self.frame)
        self.grade_entry.grid(row=2, column=1, padx=5, pady=5)
        self.add_grade_btn = tk.Button(self.frame, text="Add Grade", command=self.add_grade)
        self.add_grade_btn.grid(row=2, column=2, padx=5, pady=5)

        # Widgets for calculate and show average
        self.calc_avg_btn = tk.Button(self.frame, text="Calculate the Average", command=self.calculate_avg)
        self.calc_avg_btn.grid(row=3, columnspan=3, padx=5, pady=5)

        # Widgets for searching a student by name
        self.search_label = tk.Label(self.frame, text="Enter student name")
        self.search_label.grid(row=4, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5)
        self.search_btn = tk.Button(self.frame, text="Search", command=self.search_student)
        self.search_btn.grid(row=4, column=2, padx=5, pady=5)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=5, columnspan=3, padx=5, pady=5)


    def add_student(self):
        name = self.name_entry.get()
        if name in self.student:
            messagebox.showerror("Error", "Student already exists.")
        else:
            self.student[name] = Student(name)
            self.save_data()
            messagebox.showinfo("Success", "Student added.")
        self.name_entry.delete(0, tk.END)

    def add_grade(self):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        try:
            grade = float(self.grade_entry.get())
            if name not in self.student:
                messagebox.showerror("Error", "Student not found.")
            else:
                self.student[name].add_grade(subject, grade)
                self.save_data()
                messagebox.showinfo("Success", "Grade added.")
        except ValueError:
            messagebox.showerror("Error", "Invalid grade. Please enter a number.")
        self.subject_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def calculate_avg(self):
        name = self.name_entry.get()
        if name not in self.student:
            messagebox.showerror("Error", "Student not found.")
        else:
            average= self.student[name].calculate_average()
            self.result_label.config(text=f"{name}'s average grade is {average: .2f}")
        self.name_entry.delete(0, tk.END)

    def save_data(self):
        with open("student_data.txt", "w") as file:
            for student in self.student.values():
                file.write(student.to_string() + "\n")

    def load_data(self):
        if os.path.exists("student_data.txt"):
            with open("student_data.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        student = Student.from_string(line)
                        self.student[student.name] = student

    def search_student(self):
        name = self.search_entry.get()
        if name not in self.student:
            self.result_label.config(text="Student not found")
        else:
            student = self.student[name]
            grades_info = "\n".join([f"{subject}:{','.join(map(str, grades))}" for subject, grades in student.grades.items()])
            average = student.calculate_average()
            self.result_label.config(text=f"Grades for {name}: \n{grades_info}\nAverage: {average: .2f}")
            self.search_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()
