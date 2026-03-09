from etl.loader import load_csv_to_raw
from etl.extractor import extract_to_parquet
from etl.transform import transform_and_load

def main():
    # 1.1 Carga de Informacion
    #   Se realizo la carga de informacion mediante Pandas, previamente ya se tenia un conocimiento basico de esta libreria para hacer inserciones de los datos crudos proporcinados de una sola tabla en un archivo csv. En especifico la que se encuentra en la carpeta "data/raw/data_prueba_tecnica.csv" 
    load_csv_to_raw()
    
    # 1.2 Extraccion de Informacion
    #   Se realizo la extraccion a la db de informacion mediante Pandas asi como la transformacion a parquet (conserva los metadatos de los tipos de datos) se creo un nuevo archivo parquet con el mismo nombre pero con extension .parquet en la carpeta "data/processed/".
    extract_to_parquet() 
    
    # 1.3 Transformacion de Informacion
    #   Se realizo la limpieza de los datos con Pandas e inspeccion inicial mediante un jupyter notebook en google colab
    # 1.4 Carga de Informacion Transformada
    #   Se realizo la carga de informacion transformada a la base de datos con Pandas y sqlalchemy, se crearon las dos nuevas tablas de companies y charges a partir del dataset procesado parquet.
    transform_and_load()



if __name__ == "__main__":
    main()
