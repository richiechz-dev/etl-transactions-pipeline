import pandas as pd
from database import engine

def load_csv_to_raw():
    """Funcion para leer los datos crudos, y cargarlos en la base de datos con Pandas"""
    
    df = pd.read_csv("data/raw/data_prueba_tecnica.csv") # Leemos el csv con pandas 
    df.to_sql("raw_table", con=engine, if_exists="replace", index=False) # Cargamos el csv a la tabla cruda de la base de datos, si la tabla ya existe, se reemplaza con los nuevos datos del csv, y no se incluye el indice del dataframe como una columna adicional en la tabla.
    
    print("[load_csv_to_raw()] Datos csv cargados en la tabla cruda de la base de datos")

if __name__ == "__main__":
    load_csv_to_raw()
