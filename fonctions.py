import streamlit as st
import mysql.connector as MC
import connexion as c
import pandas as pd


def afficher_visualisation_clients(conn):
    try:
        cursor=conn.cursor()
        req='Select * From customer'
        cursor.execute(req)
        mylst=cursor.fetchall()
        headers = ("ID","Nom", "Âge", "Salaire", "Email")
        new_data = []
        for row in mylst:
            new_row = row[:-1]  
            new_data.append(new_row)
            
        df = pd.DataFrame(new_data, columns=headers)
    
        st.subheader("Bienvenue sur la page de visualisation des clients!:smile:")
        st.dataframe(df)
        
        delete_checkbox = st.checkbox("Supprimer Client", key="delete_checkbox")
        update_checkbox = st.checkbox("Modifier Client", key="update_checkbox")
        
        if delete_checkbox:
            id_options = ["Aucun"] + list(df["ID"])
            Id_delete = st.selectbox("Choisissez l'id du client à supprimer", id_options)
            if st.button("Supprimer"):
                resultat=delete_client(conn,Id_delete)
                st.success(resultat)
        if update_checkbox:
            id_options = ["Aucun"] + list(df["ID"])
            Id_update = st.selectbox("Choisissez l'id du client à modifier", id_options)
            if Id_update != "Aucun":
                client_info = df[df["ID"] == Id_update].iloc[0]
                
                nom = st.text_input("Nom", value=client_info["Nom"])
                age = st.number_input("Âge", value=int(client_info["Âge"]))
                salaire = st.number_input("Salaire",value= float(client_info["Salaire"]))
                email = st.text_input("Email", value=client_info["Email"])
            
            if st.button("Modifier"):
                resultat = update_client(conn, Id_update, nom, age, salaire, email)
                st.success(resultat)
                
    except MC.Error as err:
        st.write(err)
        
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()
            

def afficher_creation_client(conn):
    st.subheader("Voici la page de création de client")
    nom = st.text_input("Nom")
    age = st.number_input("Âge", min_value=0, max_value=100)
    salaire = st.number_input("Salaire", min_value=0)
    email = st.text_input("Email")
    if st.button("Creer"):
        cursor = conn.cursor()
        req = "INSERT INTO customer (name, age, salaire, email) VALUES (%s, %s, %s, %s)"
        valeurs = (nom, age, salaire, email)
        cursor.execute(req, valeurs)
        conn.commit()
        conn.close()    
        st.success("Données insérées avec succès !")
        

def afficher_customer_replication_1(conn):
    st.subheader("Voici la page de replication 1 client")
    try:
        cursor=conn.cursor()
        req='Select * From customer_replication_1'
        cursor.execute(req)
        mylst=cursor.fetchall()
        headers = ("Nom", "Âge", "Salaire", "Email")
        new_data = []
        for row in mylst:
            new_row = row[1:-1] 
            new_data.append(new_row)
            
        df = pd.DataFrame(new_data, columns=headers)

        st.dataframe(df)
            
    except MC.Error as err:
        st.write(err)
        
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()
                
    

def afficher_customer_replication_2(conn):
    st.subheader("Voici la page de replication 2 client")
    try:
        cursor=conn.cursor()
        req='Select * From customer_replication_2'
        cursor.execute(req)
        mylst=cursor.fetchall()
        headers = ("Nom", "Âge", "Salaire", "Email","Time")
        new_data = []
        for row in mylst:
            new_row = row[1:]  
            new_data.append(new_row)
            
        df = pd.DataFrame(new_data, columns=headers)

        st.dataframe(df)
        
    except MC.Error as err:
        st.write(err)
        
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()
    
def delete_client(conn, id_client):
    try:
        cursor = conn.cursor()
        # Exécution de la requête sql pour supprimer le client avec l'ID spécifié
        sql_query = "DELETE FROM customer WHERE ID = %s"
        cursor.execute(sql_query, (id_client,))
        conn.commit() 
        
        # Vérifiez si le client a été supprimé avec succès
        if cursor.rowcount > 0:
            message = f"Le client avec l'ID {id_client} a été supprimé avec succès."
        else:
            message = f"Aucun client trouvé avec l'ID {id_client}. Aucune suppression n'a été effectuée."
        
        return message  
    
    except MC.Error as err:
        return f"Erreur lors de la suppression du client: {err}"
    
    finally:
        if conn.is_connected():
            cursor.close()

def update_client(conn, id_client, nom, age, salaire, email):
    try:
        cursor = conn.cursor()
        # Exécutez la requête SQL pour mettre à jour les informations du client
        sql_query = "UPDATE customer SET name = %s, age = %s, salaire = %s, email = %s WHERE ID = %s"
        cursor.execute(sql_query, (nom, age, salaire, email, id_client))
        conn.commit()  # Validez la mise à jour dans la base de données
        
        # Vérifiez si le client a été mis à jour avec succès
        if cursor.rowcount > 0:
            message = f"Les informations du client avec l'ID {id_client} ont été mises à jour avec succès."
        else:
            message = f"Aucun client trouvé avec l'ID {id_client}. Aucune mise à jour n'a été effectuée."
        
        return message  
    
    except MC.Error as err:
        return f"Erreur lors de la mise à jour des informations du client: {err}"
    
    finally:
        if conn.is_connected():
            cursor.close()
 
 
def afficher_client_delete(conn):
    st.subheader("Voici la page des clients supprimes")
    try:
        cursor=conn.cursor()
        req='Select * From customer_deleted'
        cursor.execute(req)
        mylst=cursor.fetchall()
        headers = ("Nom", "Âge", "Salaire", "Email","Date Suppression")
        new_data = []
        for row in mylst:
            new_row = row[1:]  
            new_data.append(new_row)
            
        df = pd.DataFrame(new_data, columns=headers)

        st.dataframe(df)
        
    except MC.Error as err:
        st.write(err)
        
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()

def afficher_client_update(conn):
    st.subheader("Voici la page des clients modifies")
    try:
        cursor=conn.cursor()
        req='Select * From customer_updated'
        cursor.execute(req)
        mylst=cursor.fetchall()
        headers = ("Ancien_Nom", "Ancien_Âge", "Ancien_Salaire", "Ancien_Email","Date Modification")
        new_data = []
        for row in mylst:
            new_row = row[1:]  
            new_data.append(new_row)
            
        df = pd.DataFrame(new_data, columns=headers)

        st.dataframe(df)
        
    except MC.Error as err:
        st.write(err)
        
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()

def navigation():
    st.sidebar.title("Navigation")
    choix_page = st.sidebar.radio("Aller à :", ("Visualisation des Clients", "Visualisation des Clients Db Replica1", "Visualisation des Clients Db Replica2", "Création Client", "Suppression Client","Mise à jour Client"))
    conn=c.connection()
    if choix_page == "Visualisation des Clients":
        afficher_visualisation_clients(conn)
        
    elif choix_page == "Visualisation des Clients Db Replica1":
        afficher_customer_replication_1(conn)
    elif choix_page == "Visualisation des Clients Db Replica2":
        afficher_customer_replication_2(conn)
    elif choix_page == "Création Client":
        afficher_creation_client(conn)
    
    elif choix_page == "Suppression Client":
        afficher_client_delete(conn)
    elif choix_page == "Mise à jour Client":
        afficher_client_update(conn)

