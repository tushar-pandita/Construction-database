
import streamlit as st
import mysql.connector as sql
conn = sql.connect(host='localhost' ,user='root' ,password='hariom2003',database='construction')


cursor = conn.cursor()

def show_projects(ssn):
    cursor.execute("SELECT p_id FROM employee WHERE emp_ssn = %s", (ssn,))
    result = cursor.fetchone()

    if result is not None:
        p_id = result[0]
        # Use the 'project_id' to fetch project details from the 'projects' table
        cursor.execute("SELECT * FROM projects WHERE p_id = %s", (p_id,))
        project_details = cursor.fetchone()
        if project_details is not None:
            # Define a table to display the project details
            cursor.execute("SELECT contact FROM employee WHERE emp_ssn = %s", (project_details[3],))
            mgr_no=cursor.fetchone()
            project_details={
                "Project ID": [project_details[0]],
                "Project Name":[project_details[1]],
                "Budget":[project_details[2]],
                "Manager SSN":[project_details[3]],
                "Start Date":[project_details[4]],
                "Expected Finish Date":[project_details[5]],
                "manager contact no.":[mgr_no[0]]
            }
            st.table(project_details)
        else:
            print("Project not found.")
    else:
        print("Employee not found.")

def reports(emp_ssn):
        cursor.execute("select p_id FROM projects")
        p_ids = cursor.fetchall()
        project_ids = [p[0] for p in p_ids]
        p_id = st.selectbox("select a project",project_ids)
        emp_ssn=int(st.number_input("Employee ID",key="rep_emp_id",placeholder="Enter employee ID"))
        report_text=st.text_area("Report",key="eng_report")
        if st.button("Submit",key="abc"):
                try:
                   cursor.execute("INSERT INTO reports (p_id,emp_ssn,report) VALUES (%s,%s,%s)", (p_id,emp_ssn,report_text))
                   conn.commit()
                   st.success("Submitted")
                except Exception as e:
                    st.error(str(e))

def machinery():
    st.write("Demand Machinary")
    m_name=st.text_input("Machine name",key="m_name")
    desc=st.text_area("Description",key="desc_mach",placeholder="Describe the quantity / dimensions")
    st_date=st.date_input("Start Date",key="st_date")
    stop_date=st.date_input("Stop Date", key="Stop_date")
    if st.button("Send Details to Contractor",key="det_to_con"):
        try:
            cursor.execute("INSERT INTO machinery (m_name,m_desc,str,stp) VALUES (%s,%s,%s,%s)", (m_name,desc,st_date,stop_date))
            conn.commit()
            st.success("Submitted")
        except Exception as e:
            st.error(str(e))

def req_materials():
    mid=int(st.number_input("Material ID",key="m_id",placeholder="Enter material ID"))
    mname=st.text_input("Material Name",key="m_name",placeholder="Enter Material Name")
    cursor.execute("select p_id FROM projects")
    p_ids = cursor.fetchall()
    print(p_ids)
    project_ids = [p[0] for p in p_ids]
    p_id = st.selectbox("select a project",project_ids)
    desc=st.text_area("Description",key="m_desc",placeholder="Dimensions Optional")
    qty=int(st.number_input("Quantity",key="m_qty"))
    if st.button("Add"):
        try:
            cursor.execute("Insert into materials (material_id,material_name,p_id,descript,Quantity) values (%s, %s, %s, %s, %s)",(mid,mname,p_id,desc,qty))
            conn.commit()
            st.success("Added")
        except Exception as e:
            st.error(str(e))

def page_2():
    st.title("Engineer")
    
    def engineer_login():
        if 'eng_logged_in' not in st.session_state:
            st.session_state.eng_logged_in = False

        emp_ssn= ""

        if not st.session_state.eng_logged_in:
            emp_ssn_input = st.text_input("Enter your employee ID for login", key="emp_ssn_login")
            password = st.text_input("Enter your password for login", type="password", key="password_login")

            if st.button("Login"):
                cursor.execute("SELECT emp_ssn, psword FROM employee WHERE emp_ssn = %s", (emp_ssn_input,))
                result = cursor.fetchone()

                if result is not None:
                    stored_emp_ssn, stored_password = result
                    if password == stored_password:
                        st.session_state.eng_logged_in = True
                        st.success("Login successful!")
                        emp_ssn=emp_ssn_input
                    else:
                        st.error("Invalid credentials")     
                else:
                    st.error("Employee ID and password don't match")
        
        if st.session_state.eng_logged_in:
            st.write("You are logged in as an engineer")
            menu = ["show projects","request materials","report","machinery"]
            choice = st.sidebar.selectbox("Menu", menu)
            if choice == "show projects":
                show_projects(emp_ssn)
            if choice == "report":
                reports(emp_ssn)
            if choice == "request materials":
                req_materials()
            if choice == "machinery":
                machinery()
    


    engineer_login()

page_2()