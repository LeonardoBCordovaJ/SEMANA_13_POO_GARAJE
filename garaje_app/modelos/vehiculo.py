class Vehiculo:
    """
    Modelo que representa un vehiculo en el sistema del garaje 'El Hangar'.

    Atributos encapsulados:
    - _placa: Identificador unico del vehiculo.
    - _marca: Marca del fabricante.
    - _propietario: Nombre del dueño.
    - _hora_entrada: Hora de ingreso (formato HH:MM).
    - _hora_salida: Hora de egreso (formato HH:MM).
    - _costo: Valor calculado segun el tiempo de permanencia.
    """

    def __init__(self, placa: str, marca: str, propietario: str, hora_entrada: str, hora_salida: str, costo: float):
        self._placa = placa
        self._marca = marca
        self._propietario = propietario
        self._hora_entrada = hora_entrada
        self._hora_salida = hora_salida
        self._costo = costo

    # ---- Getters ----
    def get_placa(self) -> str: return self._placa

    def get_marca(self) -> str: return self._marca

    def get_propietario(self) -> str: return self._propietario

    def get_hora_entrada(self) -> str: return self._hora_entrada

    def get_hora_salida(self) -> str: return self._hora_salida

    def get_costo(self) -> float: return self._costo

    def __str__(self) -> str:
        return f"Placa: {self._placa} | Marca: {self._marca} | Costo: ${self._costo:.2f}"