import pandas as pd

from pathlib import Path

from helper.enums import CandidateFields


def save_file_path(file_name: str) -> Path:
    """Función que retorna la ruta del archivo donde se guardaran los datos"""

    main_dir = Path().absolute()
    _file_name = f"{file_name}.csv"
    return Path(main_dir, "result", _file_name)


def save_candidates(candidates: list, file_name: str) -> list[dict]:
    """Función para guardar lista de candidatos scrapeados"""

    dt = pd.DataFrame.from_dict(candidates, orient="columns")

    _unusefull_data = dt[CandidateFields.NAME.value] != "Sin Nombre"
    dt = dt.loc[_unusefull_data]

    print("Contactos filtrados:")
    print(f"{len(dt.index)} contactos a guardar")
    print("=="*50)

    save_path = save_file_path(file_name)
    dt.to_csv(save_path, index=False, header=True)

    return dt.to_dict(orient="records")
