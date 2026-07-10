import streamlit as st
import requests
import pandas as pd

st.title("Enterprise HRMS Dashboard")

# Sidebar
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Employees", "Attendance", "Payroll", "AI Analytics"])

BASE_URL = "http://localhost:8000"

if menu == "Dashboard":
    st.header("Welcome to HRMS")
    st.write("Professional HR Management System with AI and Face Recognition")

elif menu == "Employees":
    st.header("Employee Management")
    if st.button("List Employees"):
        try:
            resp = requests.get(f"{BASE_URL}/employees/")
            if resp.status_code == 200:
                st.dataframe(pd.DataFrame(resp.json()))
        except:
            st.error("Backend not running")

elif menu == "Attendance":
    st.header("Face Recognition Attendance")
    st.write("In full implementation, upload image or use webcam for recognition.")
    emp_id = st.number_input("Employee ID", 1)
    if st.button("Mark Attendance"):
        try:
            resp = requests.post(f"{BASE_URL}/attendance/mark/?employee_id={emp_id}")
            st.success(resp.json())
        except:
            st.error("Error")

elif menu == "Payroll":
    st.header("Payroll Processing")
    month = st.text_input("Month", "2026-07")
    if st.button("Process Payroll"):
        try:
            resp = requests.post(f"{BASE_URL}/payroll/process/?month={month}")
            st.success("Payroll Processed!")
        except:
            st.error("Error")

elif menu == "AI Analytics":
    st.header("AI Analytics")
    st.write("Attrition Risk Analysis")
    if st.button("Get Insights"):
        try:
            resp = requests.get(f"{BASE_URL}/analytics/attrition/")
            st.json(resp.json())
        except:
            st.error("Error")