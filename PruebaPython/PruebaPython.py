from cmath import cos
import csv
import datetime
from dataclasses import dataclass, field
from typing import List
import pandas as pd

MONEDA_ISO = "EUR"
RECUR_Z001 = "Z001"
RECUR_Z002 = "Z002"


@dataclass
class DatosEntradaCostesIngresos:
    PEP_Nivel: str
    PEP_ElementoPEP: str
    PEP_DefinicionProyecto: str
    PEP_Descripcion: str
    PEP_NombreBoc: str
    PEP_PorcentajeServicioCyber: str
    Fecha_Inicio: str
    Fecha_Fin: str
    CC_Fecha: str
    IAFPTTCCT_CodActividad: str
    IAFPTTCCT_ActivPrincipal: str
    IAFPTTCCT_FaseServicio: str
    CC_Ingreso: str
    MA_Mg_2023: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # Reemplaza los espacios en blanco en las claves con guiones bajos y establece el atributo
            attribute_name = key.replace(" ", "_")
            setattr(self, attribute_name, value)




@dataclass
class DatosSalidaCostesIngresos:
    IdProyectoMaestro: str
    Descripcion: str
    Moneda: str
    FechaInicio: str
    FechaFin: str
    PEP: str
    Recurso: str
    Fecha: str
    Costes: str
    Ingresos: str


def leer_datos_de_archivo_csv(input_file_path: str) -> List[DatosEntradaCostesIngresos]:
    df = pd.read_csv(input_file_path)
    return [
        DatosEntradaCostesIngresos(*row)
        for row in df.to_records(index=False)
    ]


def escribir_datos_a_archivo_csv(datos_salida: List[DatosSalidaCostesIngresos], output_file_path: str):
    df = pd.DataFrame([vars(d) for d in datos_salida])
    df.to_csv(output_file_path, index=False)


def determinar_coste_o_ingreso(dato: DatosEntradaCostesIngresos) -> str:
    descripcion = dato.PEP_Descripcion.lower()
    if "coste" in descripcion:
        return "coste"
    elif "ingresos" in descripcion:
        return "ingresos"
    else:
        return "DESCONOCIDO"


def crear_coste_ingreso(dato: DatosEntradaCostesIngresos, coste_o_ingreso: str) -> DatosSalidaCostesIngresos:
    id_proyecto_maestro = dato.PEP_DefinicionProyecto
    descripcion = dato.PEP_Descripcion
    moneda = MONEDA_ISO
    fecha_inicio = datetime.datetime.strptime(dato.Fecha_Inicio, "%d-%m-%y").strftime("%Y-%m-%d")
    fecha_fin = datetime.datetime.strptime(dato.Fecha_Fin, "%d-%m-%Y").strftime("%Y-%m-%d")

    pep = dato.PEP_ElementoPEP
    recurso = RECUR_Z001 if coste_o_ingreso == "coste" else RECUR_Z002
    fecha = datetime.datetime.strptime(dato.CC_Fecha, "%d-%m-%Y").strftime("%Y-%m-%d")

    costes = dato.CC_Ingreso if coste_o_ingreso == "coste" else ""
    ingresos = dato.CC_Ingreso if coste_o_ingreso == "ingreso" else ""  # Cambie "ingresos" a "ingreso"

    return DatosSalidaCostesIngresos(id_proyecto_maestro, descripcion, moneda, fecha_inicio, fecha_fin, pep, recurso, fecha, costes, ingresos)


 
class DatosSalidaCostesIngresos:
    def __init__(
        self,
        id_proyecto_maestro,
        descripcion,
        moneda,
        fecha_inicio,
        fecha_fin,
        pep,
        recurso,
        fecha,
        costes,
        ingresos,
    ):
        self.id_proyecto_maestro = id_proyecto_maestro
        self.descripcion = descripcion
        self.moneda = moneda
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.pep = pep
        self.recurso = recurso
        self.fecha = fecha
        self.costes = costes
        self.ingresos = ingresos


def leer_datos_de_archivo_csv(ruta_archivo: str) -> List[DatosEntradaCostesIngresos]:
    datos = []
    with open(ruta_archivo, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            datos.append(DatosEntradaCostesIngresos(**row))
    return datos


def procesar_datos(datos_entrada: List[DatosEntradaCostesIngresos]) -> List[DatosSalidaCostesIngresos]:
    datos_salida = []

    for dato in datos_entrada:
        coste_o_ingreso = determinar_coste_o_ingreso(dato)

        if dato.CC_Ingreso:
            datos_salida.append(crear_coste_ingreso(dato, coste_o_ingreso))

    return datos_salida


def determinar_coste_o_ingreso(dato: DatosEntradaCostesIngresos):
    descripcion = dato.PEP_Descripcion.lower()
    if "coste" in descripcion:
        return "coste"
    elif "ingreso" in descripcion:
        return "ingreso"
    else:
        return "DESCONOCIDO"




def escribir_datos_en_archivo_csv(ruta_archivo: str, datos_salida: List[DatosSalidaCostesIngresos]):
    fieldnames = [
        "id_proyecto_maestro",
        "descripcion",
        "moneda",
        "fecha_inicio",
        "fecha_fin",
        "pep",
        "recurso",
        "fecha",
        "costes",
        "ingresos",
    ]

    with open(ruta_archivo, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dato in datos_salida:
            writer.writerow(vars(dato))  # Llama al método to_dict() en lugar de usar vars()



def main():
    ruta_archivo_entrada = r"C:\Users\mparicio\Desktop\Proyectos\Proyecto TelefonicaTEC\DatosPrueba\CostesIngresos\CostesIngresosEstructura1.csv"
    ruta_archivo_salida = r"C:\Users\mparicio\Desktop\Proyectos\Proyecto TelefonicaTEC\DatosPrueba\DatosSalida/salida.csv"

    datos_entrada = leer_datos_de_archivo_csv(ruta_archivo_entrada)
    datos_salida = procesar_datos(datos_entrada)
    escribir_datos_en_archivo_csv(ruta_archivo_salida, datos_salida)   


if __name__ == "__main__":
    main()
