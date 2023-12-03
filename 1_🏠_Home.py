from http import client
import streamlit as st
import mysql.connector as sql
conn = sql.connect(host='localhost' ,user='root' ,password='hariom2003',database='construction')


cursor = conn.cursor()
# cursor.execute()

custom_css = """
<style>
body {
    background-color: white;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def home_page():
    st.title("Construction Connect")
    st.image("/Users/tushar/desk_stuff/dbms_proj/construction_app/dbms_img1.webp",caption="building your dream",use_column_width=True,width=2000)
    # page_bg_img = '''
    #     <style>
    #     body {
    #     background-image: url(https://media.gq.com/photos/5b6b20e3a3a1320b7280f029/16:9/pass/the-brutal-wonders-of-the-architecture-world-gq-style-fall-2018_07.jpg";
    #     background-size: cover;
    #     }
    #     </style>
    #     '''

    # st.markdown(page_bg_img, unsafe_allow_html=True)
home_page()


