import streamlit as st
import mysql.connector as sql
conn = sql.connect(host='localhost' ,user='root' ,password='hariom2003',database='construction')
cursor = conn.cursor()



def show_machinery():
    cursor.execute("SELECT * FROM machinery")
    mat=cursor.fetchall()
    for r in mat:

        tbl={
            "Machine Name" : r[0],
            "Description":r[1],
            "Start Date":r[2],
            "Stop Date":r[3]
        }

        st.table(tbl)
        if st.button("Available",key=r[0]):
            st.success("Message Passed")

def show_materials():
    st.write("Materials requested")
    cursor.execute("SELECT * FROM materials")
    mat=cursor.fetchall()
    for r in mat:
        tbl={
           "Material Name":r[1],
           "Quantity":r[4],
           "Description":r[3] 
        }
        st.table(tbl)

        if st.button("Material supplied",key=r[3]):
            try:
                cursor.execute("DELETE FROM materials WHERE material_id = %s", (r[0],))
                conn.commit()
                st.success("Material status updated: Material supplied.")
            except Exception as e:
                st.error(f"Error updating material status: {str(e)}")


def page3():
    st.header("Contractor")
    st.write("Bidding open for")
    menu=["show materials demand","show machinery demand"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "show materials demand":
        show_materials()
    if choice == "show machinery demand":
        show_machinery()

page3()
