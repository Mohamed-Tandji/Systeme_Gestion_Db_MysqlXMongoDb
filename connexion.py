import mysql.connector as MC
import streamlit as st


try:
    def connection():
        
        conn=MC.connect(host='localhost',database='gestion_clients',user='root',password='')
        
        return conn
        
    
except MC.Error as err:
    st.subheader(err)
    
