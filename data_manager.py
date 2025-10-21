import csv
import os

def save_data(filename, data, fieldnames):
    """
    Guarda los datos en un archivo CSV.
    Args:
        filename (str): El nombre del archivo CSV.
        data (list of dict): Los datos a guardar.
        fieldnames (list of str): Los nombres de las columnas del CSV.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"Error al escribir en el archivo {filename}: {e}")

def load_data(filename):
    """
    Carga los datos desde un archivo CSV.
    Args:
        filename (str): El nombre del archivo CSV.
    Returns:
        list of dict: Los datos cargados.
    """
    data = []
    if not os.path.exists(filename):
        return data
        
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(dict(row))
    except IOError as e:
        print(f"Error al leer del archivo {filename}: {e}")
    return data

