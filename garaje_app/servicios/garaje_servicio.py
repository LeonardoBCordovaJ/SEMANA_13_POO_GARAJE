import math
from modelos.vehiculo import Vehiculo

class GarajeServicio:
    """
    Servicio que gestiona la logica del garaje 'El Hangar'.
    Administra la coleccion de vehiculos y el calculo de tarifas.
    """

    def __init__(self):
        # Lista en memoria para almacenar los objetos Vehiculo
        self._vehiculos: list[Vehiculo] = []

    # ----------------- CALCULO DE TARIFA -----------------

    def calcular_costo(self, entrada: str, salida: str) -> float:
        """
        Calcula el costo basado en bloques de 30 minutos ($1.00 por bloque).
        Formato esperado: HH:MM (24h)
        """
        try:
            h_ent, m_ent = map(int, entrada.split(':'))
            h_sal, m_sal = map(int, salida.split(':'))

            total_min_ent = h_ent * 60 + m_ent
            total_min_sal = h_sal * 60 + m_sal

            diferencia = total_min_sal - total_min_ent

            if diferencia <= 0:
                return 0.0

            bloques = math.ceil(diferencia / 30)
            return float(bloques * 1.00)
        except Exception:
            return 0.0

    # ----------------- OPERACIONES SOBRE COLECCION -----------------

    def registrar_entrada(self, placa: str, marca: str, propietario: str, hora_entrada: str) -> Vehiculo:
        """
        Registra un nuevo vehiculo que ingresa al garaje.
        La hora de salida y el costo quedan pendientes (None).
        """
        vehiculo = Vehiculo(placa, marca, propietario, hora_entrada)
        self._vehiculos.append(vehiculo)
        return vehiculo

    def registrar_salida(self, placa: str, hora_salida: str) -> Vehiculo | None:
        """
        Registra la salida de un vehiculo existente y calcula el costo.
        Busca por placa; si no encuentra, retorna None.
        """
        vehiculo = self.buscar_por_placa(placa)
        if vehiculo is None:
            return None

        costo = self.calcular_costo(vehiculo.get_hora_entrada(), hora_salida)
        if costo <= 0:
            return None

        vehiculo.set_hora_salida(hora_salida)
        vehiculo.set_costo(costo)
        return vehiculo

    def buscar_por_placa(self, placa: str) -> Vehiculo | None:
        for v in self._vehiculos:
            if v.get_placa() == placa:
                return v
        return None

    def editar_vehiculo(self, placa_original: str, nueva_marca: str, nuevo_propietario: str) -> bool:
        vehiculo = self.buscar_por_placa(placa_original)
        if vehiculo is None:
            return False
        vehiculo.set_marca(nueva_marca)
        vehiculo.set_propietario(nuevo_propietario)
        return True

    def eliminar_vehiculo(self, placa: str) -> bool:
        vehiculo = self.buscar_por_placa(placa)
        if vehiculo is None:
            return False
        self._vehiculos.remove(vehiculo)
        return True

    def obtener_todos(self) -> list[Vehiculo]:
        """Retorna la lista completa de vehiculos registrados."""
        return self._vehiculos