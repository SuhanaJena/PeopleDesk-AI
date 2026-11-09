
import sqlite3

DATABASE = "peopledesk.db"


# ---------------- DATABASE CONNECTION ----------------

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- INITIALIZE DATABASE ----------------

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL,
            leave_balance INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO employees
        (employee_id, name, department, email, leave_balance)
        VALUES
        ('EMP001', 'Suhana Jena', 'Engineering',
         'alex@example.com', 18),

        ('EMP002', 'Jordan Lee', 'Human Resources',
         'jordan@example.com', 15),

        ('EMP003', 'Taylor Smith', 'Marketing',
         'taylor@example.com', 20)
    """)

    conn.commit()
    conn.close()


# ---------------- EMPLOYEE DETAILS ----------------

def get_employee(employee_id):

    conn = get_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    conn.close()

    return dict(employee) if employee else None


# ---------------- LEAVE REQUEST HISTORY ----------------

def get_leave_requests(employee_id):

    conn = get_connection()

    requests = conn.execute(
        """
        SELECT * FROM leave_requests
        WHERE employee_id = ?
        ORDER BY created_at DESC
        """,
        (employee_id,)
    ).fetchall()

    conn.close()

    return [dict(request) for request in requests]


# ---------------- ALL EMPLOYEE REQUESTS ----------------

def get_all_leave_requests():

    conn = get_connection()

    requests = conn.execute(
        """
        SELECT
            leave_requests.*,
            employees.name,
            employees.department
        FROM leave_requests
        JOIN employees
        ON leave_requests.employee_id = employees.employee_id
        ORDER BY leave_requests.created_at DESC
        """
    ).fetchall()

    conn.close()

    return [dict(request) for request in requests]


# ---------------- SUBMIT LEAVE REQUEST ----------------

def submit_leave_request(
    employee_id,
    start_date,
    end_date,
    reason
):

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO leave_requests
        (employee_id, start_date, end_date, reason)
        VALUES (?, ?, ?, ?)
        """,
        (employee_id, start_date, end_date, reason)
    )

    conn.commit()

    request_id = cursor.lastrowid

    conn.close()

    return request_id


# ---------------- APPROVE OR REJECT LEAVE ----------------

def update_leave_status(request_id, new_status):

    if new_status not in ("Approved", "Rejected"):
        raise ValueError("Invalid leave status.")

    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE leave_requests
        SET status = ?
        WHERE request_id = ?
        AND status = 'Pending'
        """,
        (new_status, request_id)
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


# ---------------- DATABASE TEST ----------------

if __name__ == "__main__":

    initialize_database()

    print("PeopleDesk AI database initialized!")

    print("\nEmployees:")

    for employee_id in ("EMP001", "EMP002", "EMP003"):
        print(get_employee(employee_id))

    print("\nAll Leave Requests:")

    print(get_all_leave_requests())