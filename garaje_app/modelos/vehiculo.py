class Vehiculo:
    """
    Modelo que representa un vehiculo en el sistema del garaje 'El Hangar'.

    Atributos encapsulados:
    - _placa: Identificador unico del vehiculo.
    - _marca: Marca del fabricante.
    - _propietario: Nombre del dueño.
    - _hora_entrada: Hora de ingreso (formato HH:MM).
    - _hora_salida: Hora de egreso (formato HH:MM) - puede ser None mientras el vehiculo esta en el garaje.
    - _costo: Valor calculado segun el tiempo de permanencia - puede ser None hasta registrar la salida.
    """

    def __init__(self, placa: str, marca: str, propietario: str, hora_entrada: str,
                 hora_salida: str | None = None, costo: float | None = None):
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
    def get_hora_salida(self) -> str | None: return self._hora_salida
    def get_costo(self) -> float | None: return self._costo

    # ---- Setters ----
    def set_marca(self, marca: str): self._marca = marca
    def set_propietario(self, propietario: str): self._propietario = propietario
    def set_hora_salida(self, hora_salida: str): self._hora_salida = hora_salida
    def set_costo(self, costo: float): self._costo = costo

    def __str__(self) -> str:
        return (f"Placa: {self._placa} | Marca: {self._marca} | "
                f"Entrada: {self._hora_entrada} | Salida: {self._hora_salida or 'En garaje'} | "
                f"Costo: ${self._costo:.2f}" if self._costo is not None else "Costo pendiente")