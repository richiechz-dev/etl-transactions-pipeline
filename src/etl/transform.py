import pandas as pd
from sqlalchemy import insert

from database import SessionLocal, init_db
from models.models import Charge, Company


def transform_and_load():
    """Función para transformar los datos del Parquet y cargarlos en la base de datos en las tablas normalizadas 'companies' y 'charges'"""
    # NOTA: Este proceso carga las dos tablas a la base de datos SQLite de manera provisional, por lo que los datos de tipo date o timestamp no se veran refleajos en la db local, al cambiar a  una base de datos como PostgreSQL, estos campos se visualizaran correctamente con su tipo de dato correspondiente.
    
    
    # - Manejo de valores nulos (NaN/NaT) en columnas críticas como 'company_id' e 'id',
    #   que son NOT NULL en la base de datos, requiriendo el descarte de filas
    #   incompletas para mantener la integridad referencial y de clave primaria.
    # - Conversión de 'paid_at' a 'updated_at' y su manejo como campo opcional.
    # - Asegurar que las empresas se carguen una única vez mediante `drop_duplicates`.

    # Se lee el archivo Parquet que contiene los datos procesados, que ya tienen los tipos de datos correctos gracias a la etapa de extracción y la breve transformación.
    df = pd.read_parquet("data/processed/raw_table.parquet")
    
    # Preparacion de las tablas finles a cargar, creando dos dataframes. Uno para companies y otro para charges.
    
    # Para companies
    df_companies = df[['company_id', 'name']].dropna().drop_duplicates(subset=['company_id'])
    df_companies.columns = ['id', 'company_name'] 
    
    # Para charges
    df_charges = df[['id', 'company_id', 'amount', 'status', 'created_at', 'paid_at']]
    df_charges = df_charges.rename(columns={'paid_at': 'updated_at'})
    # Convert NaT to None for proper SQLAlchemy handling of Optional[datetime]
    df_charges['updated_at'] = df_charges['updated_at'].replace({pd.NaT: None})
    # Drop rows where company_id or id is NaN to satisfy NOT NULL constraints
    df_charges.dropna(subset=['company_id', 'id'], inplace=True)


    # Asegurarnos de que las tablas existan mediante la función de inicialización de la base de datos, que crea las tablas según los modelos definidos si no existen ya.
    init_db()

    with SessionLocal() as session:
        try:
            print("[transform_and_load()] Iniciando carga a la base de datos...")

            # Cargar Companies
            companies_data = df_companies.to_dict("records")
            session.execute(insert(Company), companies_data)
            session.commit()
            print(f"[loader] {len(companies_data)} commit de empresas.")

            # Cargar Charges
            charges_data = df_charges.to_dict("records")
            session.execute(insert(Charge), charges_data)        
            session.commit()
            print(f"[loader] {len(charges_data)} commit de cargos.")

        except Exception as e:
            session.rollback() # En caso de error, revertimos la transacción para evitar datos inconsistentes en la base de datos.
            print(f"[error] Falló la carga: {e}")


if __name__ == "__main__":
    transform_and_load()
