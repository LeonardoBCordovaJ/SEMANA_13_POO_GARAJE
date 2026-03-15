import math
from modelos.vehiculo import Vehiculo

class GarajeServicio:
    """
    Servicio que gestiona la logica del garaje 'El Hangar'.
    Administra la lista de vehiculos y el calculo de tarifas.
    """

    def __init__(self):
        # Lista en memoria para almacenar los objetos Vehiculo
        self._vehiculos: list[Vehiculo] = []

    def calcular_costo(self, entrada: str, salida: str) -> float:
        """
        Calcula el costo basado en bloques de 30 minutos ($1.00 por bloque).
        Formato esperado: HH:MM (24h)
        """
        try:
            h_ent, m_ent = map(int, entrada.split(':'))
            h_sal, m_sal = map(int, salida.split(':'))

            # Convertir todo a minutos totales desde las 00:00
            total_min_ent = h_ent * 60 + m_ent
            total_min_sal = h_sal * 60 + m_sal

            diferencia = total_min_sal - total_min_ent

            if diferencia <= 0:
                return 0.0

            # Calculo de bloques de 30 minutos (redondeo hacia arriba)
            bloques = math.ceil(diferencia / 30)
            return float(bloques * 1.00)
        except Exception:
            return 0.0

    def registrar_vehiculo(self, vehiculo: Vehiculo):
        """Agrega un vehiculo a la coleccion."""
        self._vehiculos.append(vehiculo)

    def obtener_todos(self) -> list[Vehiculo]:
        """Retorna la lista completa de vehiculos registrados."""
        return self._vehiculos