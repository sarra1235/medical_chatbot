from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import textwrap



def calcul_distance(address1, address2):
    # Initialize geolocator
    geolocator = Nominatim(user_agent="distance_calculator")

    # Geocode the addresses
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    if not location1 or not location2:
        raise ValueError("One or both addresses could not be geocoded.")

    # Get the coordinates
    coords_1 = (location1.latitude, location1.longitude)
    coords_2 = (location2.latitude, location2.longitude)

    # Calculate the distance
    distance_kilometers = geodesic(coords_1, coords_2).kilometers

    return distance_kilometers

def nearest_Doctors(patient_address,Speciality):
    dataset = pd.read_excel('C:\\Users\\DELL\\Desktop\\python\\data\\ds_medecins.xlsx')
   #print(dataset.head())
   #num_rows = len(dataset)
   #print(num_rows)

    df = dataset[dataset['Speciality'] == Speciality]
    #Extraire les IDs correspondants dans une liste
    list_of_ids = df['Med_ID'].tolist()
    #print(list_of_ids)
    
    distances = []
    for i in range(len(list_of_ids)): 
     ID=list_of_ids[i]
     row = dataset[dataset['Med_ID'] == ID]
     Med_address=row['Med_Address'].iloc[0]
     distance=calcul_distance(Med_address, patient_address)
     distances.append(distance) 

    #print(distances)
    # Créer un tableau 2D avec deux lignes
    tableau = np.array([list_of_ids, distances])
    sorted_indices = np.argsort(tableau[1])
    sorted_tableau = tableau[:, sorted_indices]
    #print(sorted_tableau)
    ids_nearest_doc = sorted_tableau[0, :4]
    # Filtrer les lignes où les IDs sont dans la liste
    coordonnee_med = df[df['Med_ID'].isin(ids_nearest_doc)]
    #print(coordonnee_med)
    # Afficher les lignes filtrées
    return(coordonnee_med)

'''def format_table(df):
    # Create the header
    header = "| {:<25} | {:<10} |".format(
        "Med_Noun", "Phone_Nb"
    )
    separator = "|" + "-"*27 + "|" + "-"*12 + "|"
    
    # Create each row of the table
    rows = []
    for _, row in df.iterrows():
        rows.append("| {:<25} | {:<10} |".format(
            row["Med_Noun"], row["Phone_Nb"]
        ))
    
    # Combine everything into the final table
    table = "\n".join([header, separator] + rows)
    
    return table'''
def format_table(df):
    # Define column widths
    name_width = 25
    phone_width = 10
    address_width = 40  # Adjust this width as needed

    # Create the header
    header = "| {:<25} | {:<10} | {:<40} |".format(
        "Med_Noun", "Phone_Nb", "Med_Address"
    )
    separator = "|" + "-"*(name_width + 2) + "|" + "-"*(phone_width + 2) + "|" + "-"*(address_width + 2) + "|"
    
    # Create each row of the table
    rows = []
    for _, row in df.iterrows():
        # Wrap address text to fit within the cell width
        wrapped_address = textwrap.fill(row["Med_Address"], width=address_width)
        rows.append("| {:<25} | {:<10} | {:<40} |".format(
            row["Med_Noun"], row["Phone_Nb"], wrapped_address
        ))
    
    # Combine everything into the final table
    table = "\n".join([header, separator] + rows)
    
    return table
   



'''address_patient = "Ihec - Institut des Hautes Études Commerciales de Carthage"
Speciality = "Ophtalmologist"

coordonnee_med = nearest_Doctors(address_patient,Speciality)
tab = format_table(coordonnee_med )
print(tab)
#display_Doctors(coordonnee_med)'''
