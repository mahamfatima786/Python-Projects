import sqlite3

DB_NAME = "students.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                marks REAL NOT NULL,
                grade TEXT NOT NULL
            )
            """
        )


def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    if marks >= 80:
        return "A"
    if marks >= 70:
        return "B"
    if marks >= 60:
        return "C"
    if marks >= 50:
        return "D"
    return "F"


def read_marks(prompt="Marks (0-100): "):
    while True:
        try:
            marks = float(input(prompt))
            if 0 <= marks <= 100:
                return marks
            print("Marks 0 se 100 ke darmiyan hone chahiye.")
        except ValueError:
            print("Meharbani karke sahi number likhein.")


def add_student():
    name = input("Naam: ").strip()
    roll_no = input("Roll number: ").strip()
    if not name or not roll_no:
        print("Naam aur roll number khali nahi ho sakte.")
        return
    marks = read_marks()
    grade = calculate_grade(marks)
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (name, roll_no, marks, grade) VALUES (?, ?, ?, ?)",
                (name, roll_no, marks, grade),
            )
        print(f"Student add ho gaya. Grade: {grade}")
    except sqlite3.IntegrityError:
        print("Ye roll number pehle se maujood hai.")


def print_rows(rows):
    if not rows:
        print("Koi record nahi mila.")
        return
    print(f"\n{'Roll No':<12}{'Naam':<22}{'Marks':<10}{'Grade':<6}")
    print("-" * 50)
    for _, name, roll_no, marks, grade in rows:
        print(f"{roll_no:<12}{name:<22}{marks:<10}{grade:<6}")
    print()


def view_all():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    print_rows(rows)


def search_student():
    print("1. Roll number se search\n2. Naam se search")
    choice = input("Option chunein: ").strip()
    with get_connection() as conn:
        if choice == "1":
            roll_no = input("Roll number: ").strip()
            rows = conn.execute(
                "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
            ).fetchall()
        elif choice == "2":
            name = input("Naam (ya uska hissa): ").strip()
            rows = conn.execute(
                "SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",)
            ).fetchall()
        else:
            print("Ghalat option.")
            return
    print_rows(rows)


def update_student():
    roll_no = input("Jis student ko update karna hai uska roll number: ").strip()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
        ).fetchone()
        if not row:
            print("Student nahi mila.")
            return
        print(f"Maujooda naam: {row[1]}, marks: {row[3]}")
        new_name = input("Naya naam (khali chhorein to wohi rahega): ").strip() or row[1]
        marks_text = input("Naye marks (khali chhorein to wohi rahenge): ").strip()
        if marks_text:
            try:
                new_marks = float(marks_text)
                if not 0 <= new_marks <= 100:
                    raise ValueError
            except ValueError:
                print("Ghalat marks. Update cancel.")
                return
        else:
            new_marks = row[3]
        new_grade = calculate_grade(new_marks)
        conn.execute(
            "UPDATE students SET name = ?, marks = ?, grade = ? WHERE roll_no = ?",
            (new_name, new_marks, new_grade, roll_no),
        )
    print(f"Record update ho gaya. Naya grade: {new_grade}")


def delete_student():
    roll_no = input("Jis student ko delete karna hai uska roll number: ").strip()
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
    print("Record delete ho gaya." if cur.rowcount else "Student nahi mila.")


def main():
    init_db()
    actions = {
        "1": add_student,
        "2": view_all,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
    }
    while True:
        print(
            "\n=== Student Management System ===\n"
            "1. Student add karein\n"
            "2. Tamam students dekhein\n"
            "3. Student search karein\n"
            "4. Student update karein\n"
            "5. Student delete karein\n"
            "6. Exit"
        )
        choice = input("Option chunein: ").strip()
        if choice == "6":
            print("Khuda hafiz!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Ghalat option, dobara koshish karein.")


if __name__ == "__main__":
    main()
