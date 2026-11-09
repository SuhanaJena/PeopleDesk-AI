
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from database import (
    initialize_database,
    get_employee,
    get_leave_requests,
    get_all_leave_requests,
    submit_leave_request,
    update_leave_status
)

# =====================================================
# 1. CONFIGURATION
# =====================================================

load_dotenv()
initialize_database()

GEMINI_MODEL = "gemini-3.5-flash-lite"
EMPLOYEE_ID = "EMP001"
ALLOCATED_LEAVES = 24

st.set_page_config(
    page_title="PeopleDesk AI",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

employee = get_employee(EMPLOYEE_ID)

if not employee:
    st.error("Employee record not found in the database.")
    st.stop()

remaining_leaves = employee["leave_balance"]
used_leaves = max(0, ALLOCATED_LEAVES - remaining_leaves)


# =====================================================
# 2. SAMPLE HR KNOWLEDGE BASE
# =====================================================

POLICIES = {
    "Leave Policy": {
        "category": "Employee Benefits",
        "description": "Guidelines for applying and managing leave.",
        "content": """
Employees can apply for leave through the PeopleDesk AI portal.

Every application should include a start date, end date and reason.

Leave applications remain Pending until reviewed by HR.

Employees should check their available leave balance before applying.
"""
    },

    "Holiday Policy": {
        "category": "Company Guidelines",
        "description": "Information about company holidays.",
        "content": """
The company holiday calendar includes public holidays and
organization-specific holidays.

Employees should refer to the official HR holiday calendar
for confirmed dates.
"""
    },

    "Onboarding Guidelines": {
        "category": "New Employees",
        "description": "Activities required during onboarding.",
        "content": """
New employees are expected to submit personal documents,
complete identity verification, receive IT equipment
and attend company orientation.
"""
    },

    "Employee Support": {
        "category": "Employee Services",
        "description": "How employees can access HR assistance.",
        "content": """
Employees can contact the HR support team for assistance
with workplace policies, benefits, onboarding and leave.
"""
    }
}


# =====================================================
# 3. ONBOARDING DATA
# =====================================================

ONBOARDING_TASKS = [
    "Submit personal documents",
    "Complete identity verification",
    "Set up IT equipment",
    "Complete company orientation"
]

if "onboarding_status" not in st.session_state:
    st.session_state.onboarding_status = {
        task: False for task in ONBOARDING_TASKS
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

if "queued_prompt" not in st.session_state:
    st.session_state.queued_prompt = None


# =====================================================
# 4. DARK THEME STYLING
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #090F20;
        color: #F5F7FF;
    }

    [data-testid="stSidebar"] {
        background-color: #101A32;
    }

    [data-testid="stMetric"] {
        background-color: #172440;
        border: 1px solid #2A3A5B;
        border-radius: 14px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #27E0C3;
    }

    [data-testid="stMetricLabel"] {
        color: #C4CEE1;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #172440;
        border-color: #2A3A5B;
        border-radius: 14px;
    }

    hr {
        border-color: #293957;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def section_heading(title, subtitle=None):
    st.subheader(title)

    if subtitle:
        st.caption(subtitle)


def status_badge(status):

    if status == "Approved":
        st.success("✓ Approved")

    elif status == "Rejected":
        st.error("✕ Rejected")

    else:
        st.warning("◷ Pending")


def get_policy_context(question):

    question_words = set(question.lower().split())
    matches = []

    for title, policy in POLICIES.items():

        searchable = (
            title + " " +
            policy["category"] + " " +
            policy["content"]
        ).lower()

        if any(word in searchable for word in question_words):
            matches.append(
                title + ":\n" + policy["content"]
            )

    if matches:
        return "\n\n".join(matches)

    return "No matching policy was found in the sample knowledge base."


def get_employee_context():

    current_employee = get_employee(EMPLOYEE_ID)
    current_requests = get_leave_requests(EMPLOYEE_ID)

    return f"""
EMPLOYEE INFORMATION

Name: {current_employee['name']}
Employee ID: {current_employee['employee_id']}
Department: {current_employee['department']}
Email: {current_employee['email']}
Remaining leave balance: {current_employee['leave_balance']} days

LEAVE REQUESTS

{current_requests}
"""


# =====================================================
# 6. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.title("🏢 PeopleDesk AI")
    st.caption("INTELLIGENT EMPLOYEE EXPERIENCE")

    st.divider()

    st.markdown("### 👤 Employee Profile")

    st.write(f"**{employee['name']}**")
    st.caption(employee["department"])
    st.caption(f"Employee ID: {employee['employee_id']}")

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Choose a section",
        [
            "Dashboard",
            "AI HR Assistant",
            "Leave Balance",
            "Onboarding Tracker",
            "Leave Request",
            "Request Tracking",
            "HR Admin Dashboard",
            "HR Knowledge Base"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.success("● System Online")
    st.caption("Powered by Google Gemini")
    st.caption("Demonstration Environment")


# =====================================================
# 7. COMMON PAGE HEADER
# =====================================================

st.caption("PEOPLEDESK  /  EMPLOYEE SERVICES")

st.title(page)

st.caption(
    f"Welcome, {employee['name']} · "
    f"{employee['department']} Department"
)

st.divider()


# =====================================================
# 8. DASHBOARD
# =====================================================

if page == "Dashboard":

    # Native Streamlit welcome banner.
    # No HTML headings or HTML text are used here.

    with st.container(border=True):

        st.caption("✦ YOUR EMPLOYEE WORKSPACE")

        st.title(f"Welcome back, {employee['name']}!")

        st.write(
            "Your workday, employee services and HR support "
            "— all in one place."
        )

        st.info("Your employee self-service workspace is ready.")

    requests = get_leave_requests(EMPLOYEE_ID)

    pending = sum(
        request["status"] == "Pending"
        for request in requests
    )

    approved = sum(
        request["status"] == "Approved"
        for request in requests
    )

    rejected = sum(
        request["status"] == "Rejected"
        for request in requests
    )

    completed = sum(
        st.session_state.onboarding_status.values()
    )

    st.subheader("📊 Your Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Available Leave",
        f"{remaining_leaves} days"
    )

    c2.metric(
        "Leaves Used",
        f"{used_leaves} days"
    )

    c3.metric(
        "Pending Requests",
        pending
    )

    c4.metric(
        "Onboarding Tasks",
        f"{completed}/4"
    )

    st.divider()

    left, right = st.columns([1.4, 1])

    with left:

        section_heading(
            "📋 Recent Leave Activity",
            "Your latest leave applications."
        )

        if requests:

            for request in requests[:4]:

                with st.container(border=True):

                    col1, col2 = st.columns([2, 1])

                    with col1:

                        st.markdown(
                            f"**Request #{request['request_id']}**"
                        )

                        st.caption(
                            f"{request['start_date']} → "
                            f"{request['end_date']}"
                        )

                        st.caption(
                            f"Reason: {request['reason']}"
                        )

                    with col2:
                        status_badge(request["status"])

        else:

            st.info("No leave applications yet.")

    with right:

        section_heading(
            "📅 Leave Utilization",
            "Your sample annual leave allocation."
        )

        st.metric(
            "Available Balance",
            f"{remaining_leaves} days"
        )

        utilization = min(
            used_leaves / ALLOCATED_LEAVES,
            1.0
        )

        st.progress(utilization)

        st.caption(
            f"{used_leaves} used out of "
            f"{ALLOCATED_LEAVES} allocated days."
        )

        st.divider()

        section_heading("🎯 Onboarding Progress")

        progress = completed / len(ONBOARDING_TASKS)

        st.progress(progress)

        st.write(f"{int(progress * 100)}% completed")

        st.caption(
            f"{completed} of {len(ONBOARDING_TASKS)} activities completed."
        )

    st.divider()

    section_heading(
        "⚡ Employee Services",
        "Explore your employee self-service features."
    )

    services = [
        ("✦ AI HR Assistant", "Get answers to HR questions."),
        ("📅 Leave Balance", "Check your available leave."),
        ("📋 Onboarding Tracker", "Monitor onboarding activities."),
        ("📌 Request Tracking", "Track your applications."),
        ("📚 HR Knowledge Base", "Explore employee policies."),
        ("🛡️ HR Admin Dashboard", "Review leave applications.")
    ]

    for index in range(0, len(services), 3):

        columns = st.columns(3)

        for column, service in zip(
            columns,
            services[index:index + 3]
        ):

            with column:

                with st.container(border=True):

                    st.markdown(f"### {service[0]}")
                    st.caption(service[1])


# =====================================================
# 9. AI HR ASSISTANT
# =====================================================

elif page == "AI HR Assistant":

    section_heading(
        "✦ Your Personal HR Assistant",
        "Ask questions about your employee profile, leave and HR policies."
    )

    st.info(
        "PeopleDesk AI uses Gemini to answer questions using "
        "employee information and the sample HR knowledge base."
    )

    st.markdown("### Suggested Questions")

    suggestions = [
        "What is my leave balance?",
        "What is the leave policy?",
        "Show my leave requests.",
        "What are the onboarding steps?"
    ]

    suggestion_columns = st.columns(2)

    for index, suggestion in enumerate(suggestions):

        with suggestion_columns[index % 2]:

            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                width="stretch"
            ):

                st.session_state.queued_prompt = suggestion
                st.rerun()

    st.divider()

    # Display conversation history

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input

    prompt = st.chat_input("Message PeopleDesk AI...")

    if st.session_state.queued_prompt:

        prompt = st.session_state.queued_prompt
        st.session_state.queued_prompt = None

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            reply = (
                "Gemini API key is missing. "
                "Please check your local .env file."
            )

        else:

            try:

                client = genai.Client(api_key=api_key)

                employee_context = get_employee_context()
                policy_context = get_policy_context(prompt)

                context = f"""
You are PeopleDesk AI, a professional employee HR assistant.

{employee_context}

RETRIEVED SAMPLE HR POLICY INFORMATION:
{policy_context}

INSTRUCTIONS:
1. Answer clearly and professionally.
2. Use only the supplied employee information.
3. Never invent employee records or leave balances.
4. Use the supplied policy information when relevant.
5. Explain when information is unavailable.
6. You cannot approve or reject leave requests.
7. HR decisions are handled separately.
8. This is a demonstration application.
"""

                with st.spinner("PeopleDesk AI is thinking..."):

                    response = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=f"{context}\n\nQuestion: {prompt}"
                    )

                reply = response.text or (
                    "I could not generate a response. Please try again."
                )

            except Exception as error:

                print("Gemini error:", repr(error))

                reply = (
                    "Unable to connect to the AI service. "
                    "Please try again."
                )

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

        with st.chat_message("assistant"):
            st.write(reply)

    if st.button("Clear Conversation"):

        st.session_state.messages = []
        st.session_state.queued_prompt = None
        st.rerun()


# =====================================================
# 10. LEAVE BALANCE
# =====================================================

elif page == "Leave Balance":

    section_heading(
        "📅 Your Leave Summary",
        "View your annual leave allocation and current balance."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Allocated Leaves",
        f"{ALLOCATED_LEAVES} days"
    )

    c2.metric(
        "Used Leaves",
        f"{used_leaves} days"
    )

    c3.metric(
        "Available Leaves",
        f"{remaining_leaves} days"
    )

    st.divider()

    with st.container(border=True):

        st.subheader("Annual Leave Utilization")

        utilization = min(
            used_leaves / ALLOCATED_LEAVES,
            1.0
        )

        st.progress(utilization)

        st.write(
            f"{used_leaves} days used · "
            f"{remaining_leaves} days remaining"
        )

    st.divider()

    st.subheader("Leave Guidelines")

    st.markdown("""
    - Review your available balance before applying.
    - Enter accurate leave dates and a reason.
    - Track your application through Request Tracking.
    - Applications remain pending until reviewed by HR.
    """)

    st.caption(
        "The 24-day annual allocation is sample data. "
        "The database stores the current remaining balance."
    )


# =====================================================
# 11. ONBOARDING TRACKER
# =====================================================

elif page == "Onboarding Tracker":

    section_heading(
        "📋 Your Onboarding Journey",
        "Complete these activities to finish the sample onboarding checklist."
    )

    completed = sum(
        st.session_state.onboarding_status.values()
    )

    total = len(ONBOARDING_TASKS)
    progress = completed / total

    c1, c2 = st.columns(2)

    c1.metric(
        "Completed Activities",
        f"{completed}/{total}"
    )

    c2.metric(
        "Completion",
        f"{int(progress * 100)}%"
    )

    st.progress(progress)

    st.divider()

    for index, task in enumerate(ONBOARDING_TASKS):

        with st.container(border=True):

            checked = st.checkbox(
                task,
                value=st.session_state.onboarding_status[task],
                key=f"onboarding_task_{index}"
            )

            st.session_state.onboarding_status[task] = checked

            if checked:
                st.success("Completed")
            else:
                st.caption("Awaiting completion")

    if completed == total:
        st.success("All onboarding activities have been completed!")
    else:
        st.info("Continue completing your onboarding activities.")

    st.caption(
        "This checklist uses session-based demonstration data."
    )


# =====================================================
# 12. LEAVE REQUEST
# =====================================================

elif page == "Leave Request":

    section_heading(
        "📅 Apply for Leave",
        "Submit a new leave application for HR review."
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Available Balance",
        f"{remaining_leaves} days"
    )

    c2.metric(
        "Department",
        employee["department"]
    )

    st.divider()

    with st.container(border=True):

        st.subheader("Application Details")

        with st.form("leave_application_form"):

            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")

            reason = st.text_area(
                "Reason for Leave",
                placeholder="Briefly describe your reason..."
            )

            submitted = st.form_submit_button(
                "Submit Application",
                type="primary",
                width="stretch"
            )

            if submitted:

                if end_date < start_date:

                    st.error(
                        "End date cannot be before start date."
                    )

                elif not reason.strip():

                    st.error(
                        "Please enter a reason for leave."
                    )

                else:

                    days = (end_date - start_date).days + 1

                    if days > remaining_leaves:

                        st.error(
                            "Requested duration exceeds your available balance."
                        )

                    else:

                        try:

                            request_id = submit_leave_request(
                                EMPLOYEE_ID,
                                start_date.isoformat(),
                                end_date.isoformat(),
                                reason.strip()
                            )

                            st.success(
                                f"Application #{request_id} submitted successfully!"
                            )

                            st.warning(
                                "Your application is Pending HR review."
                            )

                        except Exception as error:

                            print("Leave submission error:", repr(error))
                            st.error(
                                "Unable to submit your application."
                            )

    st.caption(
        "Submitting an application does not automatically deduct leave days."
    )


# =====================================================
# 13. REQUEST TRACKING
# =====================================================

elif page == "Request Tracking":

    section_heading(
        "📌 My Leave Applications",
        "View the latest status of your submitted requests."
    )

    requests = get_leave_requests(EMPLOYEE_ID)

    if requests:

        pending = sum(
            request["status"] == "Pending"
            for request in requests
        )

        approved = sum(
            request["status"] == "Approved"
            for request in requests
        )

        rejected = sum(
            request["status"] == "Rejected"
            for request in requests
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("Pending", pending)
        c2.metric("Approved", approved)
        c3.metric("Rejected", rejected)

        st.divider()

        for request in requests:

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(
                        f"### Leave Request #{request['request_id']}"
                    )

                    st.write(
                        f"**Duration:** {request['start_date']} "
                        f"to {request['end_date']}"
                    )

                    st.write(
                        f"**Reason:** {request['reason']}"
                    )

                    st.caption(
                        f"Submitted: {request['created_at']}"
                    )

                with right:
                    status_badge(request["status"])

    else:

        st.info(
            "You have not submitted any leave applications yet."
        )


# =====================================================
# 14. HR ADMIN DASHBOARD
# =====================================================

elif page == "HR Admin Dashboard":

    section_heading(
        "🛡️ HR Operations Center",
        "Review and manage employee leave applications."
    )

    st.warning(
        "Demonstration environment: this dashboard does not "
        "currently have authentication or role-based access protection."
    )

    all_requests = get_all_leave_requests()

    pending_requests = [
        request for request in all_requests
        if request["status"] == "Pending"
    ]

    approved_requests = [
        request for request in all_requests
        if request["status"] == "Approved"
    ]

    rejected_requests = [
        request for request in all_requests
        if request["status"] == "Rejected"
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Applications",
        len(all_requests)
    )

    c2.metric(
        "Awaiting Review",
        len(pending_requests)
    )

    c3.metric(
        "Approved",
        len(approved_requests)
    )

    c4.metric(
        "Rejected",
        len(rejected_requests)
    )

    st.divider()

    st.subheader("Applications Awaiting Review")

    if pending_requests:

        for request in pending_requests:

            with st.container(border=True):

                st.markdown(
                    f"### Request #{request['request_id']} · "
                    f"{request['name']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Employee ID:** {request['employee_id']}"
                    )

                    st.write(
                        f"**Department:** {request['department']}"
                    )

                    st.write(
                        f"**Reason:** {request['reason']}"
                    )

                with col2:

                    st.write(
                        f"**Leave Dates:** {request['start_date']} "
                        f"to {request['end_date']}"
                    )

                    status_badge(request["status"])

                approve_col, reject_col = st.columns(2)

                with approve_col:

                    if st.button(
                        "✓ Approve Request",
                        key=f"approve_{request['request_id']}",
                        type="primary",
                        width="stretch"
                    ):

                        updated = update_leave_status(
                            request["request_id"],
                            "Approved"
                        )

                        if updated:
                            st.success("Request approved.")
                        else:
                            st.warning(
                                "This request was already processed."
                            )

                        st.rerun()

                with reject_col:

                    if st.button(
                        "✕ Reject Request",
                        key=f"reject_{request['request_id']}",
                        width="stretch"
                    ):

                        updated = update_leave_status(
                            request["request_id"],
                            "Rejected"
                        )

                        if updated:
                            st.success("Request rejected.")
                        else:
                            st.warning(
                                "This request was already processed."
                            )

                        st.rerun()

    else:

        st.success("There are no pending applications.")

    st.divider()

    st.subheader("All Employee Applications")

    if all_requests:

        st.dataframe(
            all_requests,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No employee applications are available.")


# =====================================================
# 15. HR KNOWLEDGE BASE
# =====================================================

elif page == "HR Knowledge Base":

    section_heading(
        "📚 HR Knowledge Center",
        "Find employee guidelines, company policies and helpful information."
    )

    search = st.text_input(
        "Search the knowledge base",
        placeholder="Try leave, holidays, onboarding..."
    )

    filtered = []

    for title, policy in POLICIES.items():

        searchable = (
            title + " " +
            policy["category"] + " " +
            policy["description"] + " " +
            policy["content"]
        ).lower()

        if not search or search.lower() in searchable:
            filtered.append((title, policy))

    st.write(f"**{len(filtered)} policy resources found**")

    for title, policy in filtered:

        with st.container(border=True):

            st.markdown(f"### 📄 {title}")

            st.caption(
                f"{policy['category']} · {policy['description']}"
            )

            with st.expander("Read Policy"):
                st.write(policy["content"])

    if not filtered:

        st.info(
            "No matching policies found. Try another search."
        )

    st.divider()

    st.subheader("Frequently Asked Questions")

    faqs = {
        "How do I apply for leave?":
            "Open Leave Request, choose your dates and submit your reason.",

        "Where can I see my leave balance?":
            "Open Leave Balance to view your allocation and remaining days.",

        "How can I check my leave status?":
            "Open Request Tracking to view your applications.",

        "What are the onboarding activities?":
            "Submit documents, verify your ID, set up IT equipment and complete orientation."
    }

    for question, answer in faqs.items():

        with st.expander(question):
            st.write(answer)

    st.info(
        "This is a sample knowledge base. Official company policies "
        "must be supplied by the organization."
    )


# =====================================================
# 16. FOOTER
# =====================================================

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:

    st.caption(
        "© 2026 PeopleDesk AI · Employee Experience Platform"
    )

with footer_right:

    st.caption(
        "✦ AI Powered · Demonstration Environment"
    )