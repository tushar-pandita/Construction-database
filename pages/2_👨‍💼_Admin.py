
import streamlit as st
import mysql.connector as sql
conn = sql.connect(host='localhost' ,user='root' ,password='hariom2003',database='construction')
import pandas as pd

cursor = conn.cursor()

if conn.is_connected:
    print("conneted")




def add_engineer():
        if 'add_engineer_state' not in st.session_state:
            st.session_state.add_engineer_state = False
        
        if not st.session_state.add_engineer_state:
            st.subheader("add engineer details")
            name=st.text_input("Name")
            project_id=int(st.number_input("Project Allocated"))
            emp_ssn=int(st.number_input("employee id"))
            contact = int(st.number_input("contact number"))
            Roles = st.text_input("enter a role")
            pswd=st.text_input("Password")
            add_button_clicked = st.button("Add")

            if add_button_clicked:
                try:
                    cursor.execute("INSERT INTO employee (emp_name, p_id, emp_ssn,contact,Roles,psword) VALUES (%s, %s, %s, %s,%s,%s)", (name, project_id, emp_ssn,contact,Roles,pswd))
                    conn.commit()
                    st.success("Engineer added")
                except Exception as e:
                    st.error("Error: " + str(e))
        
   
def add_client():
            client_name = st.text_input("Client Name")
            client_id = int(st.number_input("Client ID",placeholder="enter client ID"))
            contact = int(st.number_input("Contact",placeholder="enter contact number"))
            pin = st.text_input("address pin no. of the client")
            state = st.text_input("address state of the client")
            locality = st.text_input("address locality of the client")

            if st.button("add"):
                try:
                    cursor.execute("INSERT INTO client (client_id ,client_name ,contact ,pin ,sta ,locality ) VALUES (%s, %s, %s, %s, %s ,%s)", (client_id, client_name, contact, pin, state, locality )  )
                    conn.commit()
                    st.success("client_added")
                except Exception as e:
                    print("Error:", str(e))

def show_clients():
    st.subheader("Clients")
    cursor.execute("SELECT * FROM client")
    client_data = cursor.fetchall()

    if not client_data:
        st.write("No clients available.")
    else:
        client_ids = [row[0] for row in client_data]
        selected_client_id = st.selectbox("Select a client ID", client_ids)

        for row in client_data:
            if row[0] == selected_client_id:
                client_info = {
                    "Client ID": [row[0]],
                    "Client Name": [row[1]],
                    "Contact": [row[2]],
                    "P_ID": [row[3]]
                }
                st.table(client_info)

                if row[3] is None:
                    if st.button("Add Project"):
                       st.session_state.add_project = True

    if "add_project" in st.session_state:
        st.subheader("Add Project")
        p_id = int(st.number_input("Project ID", key="project_id_input", placeholder="Enter project ID"))
        p_name = st.text_input("Project Name", key="p_name_input", placeholder="Enter project name")
        budget = int(st.number_input("Budget in terms of cr", key="budget_input", placeholder="Enter budget"))
        st_date = st.date_input("Start date of the project", key="st_date_input")
        expected_finish = st.date_input("Expected finishing date", key="expected_finish_input")

        if st.button("Add"):
            try:
                cursor.execute("INSERT INTO projects (p_id, p_name, budget, st_date, expected_finish) VALUES (%s, %s, %s, %s, %s)", (p_id, p_name, budget, st_date, expected_finish))
                cursor.execute("UPDATE client SET p_id = %s WHERE client_id = %s", (p_id, selected_client_id))
                conn.commit()
                st.success("Project added")
                del st.session_state.add_project  # Remove the trigger
            except Exception as e:
                print("Error:", str(e))

def fetch_employees_with_same_p_id(project_id):
    cursor.execute("SELECT emp_ssn FROM employee WHERE p_id = %s", (project_id,))
    employees = cursor.fetchall()
    return [employee[0] for employee in employees]

def assign_manager_to_project(employee_ssn, project_id):
    cursor.execute("UPDATE projects SET mgr_ssn = %s WHERE p_id = %s", (employee_ssn, project_id))
    conn.commit()

def show_projects():
    st.subheader("Projects")
    cursor.execute("SELECT * FROM projects")
    project_data = cursor.fetchall()

    if not project_data:
        st.write("No clients available.")
    else:
        project_names = [row[1] for row in project_data]
        selected_project_name = st.selectbox("Select a project name", project_names)

        for row in project_data:
            if row[1] == selected_project_name:
                project_info = {
                    "Project ID": [row[0]],
                    "Project Name": [row[1]],
                    "Bugdet": [row[2]],
                    "Mgr ssn": [row[3]],
                    "Start date": [row[4]],
                    "expected finish": [row[5]]
                }
                st.table(project_info)

                if st.button("Delete Project"):
                    cursor.execute("DELETE FROM projects WHERE p_id = %s", (row[0],))
                    conn.commit()
                    st.success("Project deleted successfully.")
                    selected_project_name = ""
                        


                if row[3] is None:
                    employees_with_same_p_id = fetch_employees_with_same_p_id(row[0])
                    selected_employee_ssn = st.selectbox("Select a manager (Emp SSN)", employees_with_same_p_id)
                    
                    if st.button("Assign Manager"):
                        assign_manager_to_project(selected_employee_ssn, row[0])
                        st.success("Manager assigned to the project.")
    

def legal():

    
    cursor.execute("SELECT * FROM legal_docs")
    result = cursor.fetchall()

    df = pd.DataFrame(result,columns=["registration", "site_id", "land_type", "descript", "acquired_under", "doc"])
    df['doc'] = df['doc'].apply(lambda x: f"[Link]({x})")
    st.table(df)

    if "add_legal" not in st.session_state:
        st.session_state.add_legal = False
    
    if st.button("add legal doc"):
        st.session_state.add_legal = True
    
    if st.session_state.add_legal:
        st.write("enter legal information")
        registration = st.number_input("Registration", min_value=1, step=1)
        cursor.execute("select site_id FROM site_")
        site_result = cursor.fetchall()
        site_ids = [p[0] for p in site_result]
        site_id = st.selectbox("select a site",site_ids)
        land_type = st.text_input("Land Type", max_chars=20)
        descript = st.text_input("Description", max_chars=100)
        acquired_under = st.text_input("Acquired Under", max_chars=20)
        doc = st.text_input("Document", max_chars=100)

        if st.button("Submit"):
            try:
                # Assuming your table is named 'site_info'
                cursor.execute("INSERT INTO legal_docs (registration, site_id, land_type, descript, acquired_under, doc) VALUES (%s, %s, %s, %s, %s, %s)", (registration, site_id, land_type, descript, acquired_under, doc))
                conn.commit()
                st.session_state.add_legal = False
                st.success("Data submitted successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")


def site():

    if "add_site" not in st.session_state:
        st.session_state.add_site = False
    
    if st.button("add site"):
        st.session_state.add_site = True

    if st.session_state.add_site:
        st.write("Enter site information:")
        site_id = st.number_input("Site ID", key="site_id_input")
        site_name = st.text_input("Site Name", key="site_name_input")
        address = st.text_area("Address", key="site_address_input")
        cursor.execute("select p_id FROM projects")
        p_ids = cursor.fetchall()
        print(p_ids)
        project_ids = [p[0] for p in p_ids]
        p_id = st.selectbox("select a project",project_ids)
        registration_office = st.text_input("Registration Office", key="registration_office_input")

        if st.button("add site",key="add_site_button"):
            try:
                cursor.execute("INSERT INTO site_ (site_id, site_name, addr, p_id, registration_office) VALUES (%s, %s, %s, %s, %s)",(site_id, site_name, address, p_id, registration_office))
                conn.commit()
                st.success("site added successfully")
                st.session_state.add_site = False
            except Exception as e:
                st.error(f"Error: {e}")


    cursor.execute("SELECT * FROM site_")
    site_data = cursor.fetchall()
 

    if not site_data :
        print("no site data available")

    else:
        site_names=[row[2] for row in site_data]
        selected_site_name = st.selectbox("select a site name",site_names)

        for row in site_data:
            if row[2] == selected_site_name:
                site_info = {
                    "site_id": [row[0]],
                    "mgr_ssn": [row[1]],
                    "site name": [row[2]],
                    "address": [row[3]],
                    "project ID": [row[4]],
                    "registration office": [row[5]]
                }
                st.table(site_info)
            
            if row[1] is None:
                emp_same = fetch_employees_with_same_p_id(row[4])
                selected_emp = st.selectbox(f"Select a manager (Emp SSN)",emp_same, key='1')

                
                if st.button("Assign Manager", key="2"):
                    cursor.execute( "UPDATE site_ SET mgr_ssn = %s WHERE p_id = %s", (selected_emp, row[4]))
                    conn.commit()
                    st.success("Manager assigned to the site.")

def reports():
    st.write("Reports")
    cursor.execute("select p.p_name,r.report,r.emp_ssn from reports r join projects p where p.p_id=r.p_id;")
    res=cursor.fetchall()
    for r in res:
        r_info={
            "Project Name":[r[0]],
            "Report":[r[1]],
            "reported by":[r[2]]
        }
        st.table(r_info)

def page_1():
    st.title("Admin")
        
    
    def admin_login():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if username == "admin" and password == "12345":
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials")

        if st.session_state.logged_in:
            if st.button("Logout", key="logout_button"):
                st.session_state.logged_in = False

        if st.session_state.logged_in:
            st.write("You are logged in as an admin.")
            menu = ["show clients","add client", "Projects","Add engineer","site","legal documents","show reports"]
            choice = st.sidebar.selectbox("Menu", menu)
            if choice == "Add engineer":
                add_engineer()
            if choice == "show clients":
                show_clients()
            if choice == "add client":
                add_client()
            if choice == "Projects":
                show_projects()
            if choice == "site":
                site()
            if choice == "legal documents":
                legal()
            if choice =="show reports":
                reports()


            
    admin_login()


page_1()