
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

from database import (
    initialize_database,
    get_employee,
    get_leave_requests,
    submit_leave_request
)

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

initialize_database()

EMPLOYEE_ID = "EMP001"


@app.route("/")
def home():
    employee = get_employee(EMPLOYEE_ID)
    leave_requests = get_leave_requests(EMPLOYEE_ID)

    return render_template(
        "index.html",
        employee=employee,
        leave_requests=leave_requests
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    employee = get_employee(EMPLOYEE_ID)
    leave_requests = get_leave_requests(EMPLOYEE_ID)

    if not employee:
        return jsonify({"reply": "Employee record not found."}), 404

    if not client:
        return jsonify({
            "reply": "Gemini API key is missing. Please configure your .env file."
        }), 500

    context = f"""
    You are PeopleDesk AI, an employee self-service assistant.

    Employee information:
    Name: {employee['name']}
    Employee ID: {employee['employee_id']}
    Department: {employee['department']}
    Leave balance: {employee['leave_balance']} days

    Leave requests:
    {leave_requests}

    Answer employee questions politely and clearly.
    Use only the employee information provided above.
    Never invent leave balances or request statuses.
    You cannot approve leave requests or perform actual HR actions.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{context}\n\nEmployee question: {message}"
        )

        return jsonify({"reply": response.text})

    except Exception as error:
        print("Gemini API error:", error)
        return jsonify({
            "reply": "I'm having trouble connecting to the AI service. Please try again."
        }), 500


@app.route("/api/leave", methods=["POST"])
def apply_leave():
    data = request.get_json()

    start_date = data.get("start_date", "").strip()
    end_date = data.get("end_date", "").strip()
    reason = data.get("reason", "").strip()

    if not start_date or not end_date:
        return jsonify({"message": "Please provide both leave dates."}), 400

    if end_date < start_date:
        return jsonify({"message": "End date cannot be before start date."}), 400

    employee = get_employee(EMPLOYEE_ID)

    request_id = submit_leave_request(
        EMPLOYEE_ID, start_date, end_date, reason
    )

    return jsonify({
        "message": "Your leave request has been recorded as Pending.",
        "request_id": request_id
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)