import pandas as pd
from database import engine

def extract_to_parquet():
    """Función para extraer los datos de la db en formato crudo, convertirlos a los tipos correctos y guardarlos en formato Parquet"""
    
    df = pd.read_sql_table("raw_table", con=engine) # Leemos de la tabla cruda
    
    # Aquí es donde el string se vuelve Tiempo
    # Usamos format='mixed' ya que el formato csv generalmente no es consistente, e incluso en la db local de sqlite el formato de fecha viene en un formato de texto en realidad
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce') # Convertimos la columna 'amount' a numérica, forzando los errores a NaN para manejar valores no convertibles.
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', format='mixed')
    df['paid_at'] = pd.to_datetime(df['paid_at'], errors='coerce', format='mixed')

    # Guardamos en Parquet
    # El archivo Parquet ahora ya sabe que esas columnas son datetime64 y float64.
    df.to_parquet("data/processed/raw_table.parquet", index=False)
    print("[extract_to_parquet()] Datos extraídos y convertidos a Parquet con tipos correctos")

if __name__ == "__main__":
    extract_to_parquet()