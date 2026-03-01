import streamlit as st
import pandas as pd
from database import *

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="IT Service Desk System",
    page_icon="💻",
    layout="wide"
)

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #2c3e50;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
create_table()

# ---------- TITLE ----------
st.title("💻 IT Service Desk Management System")

# ---------- LOGIN SYSTEM ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = ["Login","Raise Ticket","View Tickets","Dashboard","Update Ticket"]
choice = st.sidebar.selectbox("Menu",menu)

# ---------- LOGIN PAGE ----------
if choice == "Login":

    st.subheader("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Admin Login Successful")

        elif username == "employee" and password == "user123":
            st.session_state.logged_in = True
            st.success("Employee Login Successful")

        else:
            st.error("Invalid credentials")

# ---------- RAISE TICKET ----------
elif choice == "Raise Ticket":

    st.subheader("Create IT Ticket")

    name = st.text_input("Employee Name")

    issue = st.selectbox(
        "Issue Type",
        ["Network Issue","Software Issue","Hardware Issue","Login Problem"]
    )

    priority = st.selectbox(
        "Priority",
        ["Low","Medium","High"]
    )

    if st.button("Submit Ticket"):
        add_ticket(name,issue,priority)
        st.success("Ticket Created Successfully")

# ---------- VIEW TICKETS ----------
elif choice == "View Tickets":

    st.subheader("All Tickets")

    result = view_tickets()

    df = pd.DataFrame(
        result,
        columns=["ID","Name","Issue","Priority","Status"]
    )

    search = st.text_input("Search by Name")

    if search:
        df = df[df["Name"].str.contains(search)]

    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Ticket Report",
        csv,
        "tickets_report.csv",
        "text/csv"
    )

# ---------- DASHBOARD ----------
elif choice == "Dashboard":

    st.subheader("Ticket Analytics Dashboard")

    result = view_tickets()

    df = pd.DataFrame(
        result,
        columns=["ID","Name","Issue","Priority","Status"]
    )

    total = len(df)
    open_tickets = len(df[df["Status"]=="Open"])
    resolved = len(df[df["Status"]=="Resolved"])

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Tickets", total)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Resolved Tickets", resolved)

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        st.write("Tickets by Priority")
        st.bar_chart(df["Priority"].value_counts())

    with col2:
        st.write("Tickets by Status")
        st.bar_chart(df["Status"].value_counts())

# ---------- UPDATE STATUS ----------
elif choice == "Update Ticket":

    st.subheader("Update Ticket Status")

    ticket_id = st.number_input("Ticket ID",min_value=1)

    status = st.selectbox(
        "Select Status",
        ["Open","In Progress","Resolved"]
    )

    if st.button("Update Status"):
        update_status(status,ticket_id)
        st.success("Ticket Updated Successfully")
