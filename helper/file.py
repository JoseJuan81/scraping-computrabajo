from pathlib import Path

def save_file_path(file_name: str) -> Path:
    """Función que retorna la ruta del archivo donde se guardaran los datos"""

    main_dir = Path().absolute()
    _file_name = f"{file_name}.csv"
    return Path(main_dir, "result", _file_name)

