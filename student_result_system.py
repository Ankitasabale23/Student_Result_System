import json
import os

FILE_NAME = "students.json"


def load_students():
    """Load student records from a JSON file."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved records.")
    return {}


def save_students(students):
    """Save student records."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_result(marks):
    """Calculate percentage, grade, and result."""
    total = sum(marks.values())
    percentage = total / len(marks)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    result = "Pass" if all(mark >= 35 for mark in marks.values()) else "Fail"

    return total, percentage, grade, result


def add_student(students):
    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if student_id in students:
        print("Student ID already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    try:
        count = int(input("Enter number of subjects: "))
        if count <= 0:
            print("Number of subjects must be positive.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    marks = {}

    for i in range(count):
        subject = input(f"Enter subject {i + 1} name: ").strip()

        if not subject:
            print("Subject name cannot be empty.")
            return

        if subject in marks:
            print("Subject already entered. Try adding the student again.")
            return

        try:
            mark = float(input(f"Enter marks for {subject} (0-100): "))
            if not 0 <= mark <= 100:
                print("Marks must be between 0 and 100.")
                return
        except ValueError:
            print("Invalid marks.")
            return

        marks[subject] = mark

    students[student_id] = {
        "name": name,
        "marks": marks
    }

    save_students(students)
    print("Student record added successfully!")


def display_student(student_id, student):
    marks = student["marks"]
    total, percentage, grade, result = calculate_result(marks)

    print("\n--- Student Result ---")
    print("Student ID:", student_id)
    print("Name:", student["name"])

    print("\nSubject Marks:")
    for subject, mark in marks.items():
        print(f"{subject}: {mark:g}")

    print(f"\nTotal Marks: {total:g} / {len(marks) * 100}")
    print(f"Percentage: {percentage:.2f}%")
    print("Grade:", grade)
    print("Result:", result)


def view_students(students):
    if not students:
        print("No student records available.")
        return

    for student_id, student in students.items():
        display_student(student_id, student)


def search_student(students):
    student_id = input("Enter student ID to search: ").strip()

    if student_id in students:
        display_student(student_id, students[student_id])
    else:
        print("Student not found.")


def update_marks(students):
    student_id = input("Enter student ID: ").strip()

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]
    print("Subjects:", ", ".join(student["marks"].keys()))

    subject = input("Enter subject to update: ").strip()

    if subject not in student["marks"]:
        print("Subject not found.")
        return

    try:
        mark = float(input("Enter new marks (0-100): "))
        if not 0 <= mark <= 100:
            print("Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid marks.")
        return

    student["marks"][subject] = mark
    save_students(students)
    print("Marks updated successfully!")


def performance_summary(students):
    if not students:
        print("No student records available.")
        return

    percentages = []

    print("\n--- Performance Summary ---")

    for student_id, student in students.items():
        _, percentage, grade, result = calculate_result(student["marks"])
        percentages.append(percentage)
        print(
            f"{student['name']} (ID: {student_id}) - "
            f"{percentage:.2f}% | Grade: {grade} | {result}"
        )

    print(f"\nNumber of students: {len(students)}")
    print(f"Class average: {sum(percentages) / len(percentages):.2f}%")
    print(f"Highest percentage: {max(percentages):.2f}%")
    print(f"Lowest percentage: {min(percentages):.2f}%")


def main():
    students = load_students()

    while True:
        print("\n===== STUDENT RESULT & GRADE MANAGEMENT =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Marks")
        print("5. Performance Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_marks(students)
        elif choice == "5":
            performance_summary(students)
        elif choice == "6":
            print("Thank you for using the Student Result System!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()