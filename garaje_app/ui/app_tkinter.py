import tkinter as tk
from tkinter import ttk, messagebox
from modelos.vehiculo import Vehiculo
from servicios.garaje_servicio import GarajeServicio


class AppGaraje(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Hangar - Sistema de Gestión de Garaje")
        self.geometry("950x650")
        self.configure(bg="#f0f2f5")

        self.servicio = GarajeServicio()
        self._crear_componentes()

    def _crear_componentes(self):
        # --- HEADER / LOGO ---
        header = tk.Frame(self, bg="#1a2a3a", height=100)
        header.pack(fill="x", padx=0, pady=0)

        # Logo simulado
        tk.Label(header, text="H", font=("Arial Black", 36), fg="white", bg="#3498db", width=2).pack(side="left",
                                                                                                     padx=20, pady=10)
        tk.Label(header, text="EL HANGAR", font=("Arial Black", 24), fg="white", bg="#1a2a3a").pack(side="left",
                                                                                                    pady=10)
        tk.Label(header, text="Control de Vehículos y Tarifas", font=("Arial", 12, "italic"), fg="#bdc3c7",
                 bg="#1a2a3a").pack(side="left", padx=20, pady=25)

        # --- CONTENEDOR PRINCIPAL ---
        main_container = tk.Frame(self, bg="#f0f2f5")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # --- FORMULARIO (NUEVO REGISTRO) ---
        form_frame = tk.LabelFrame(main_container, text=" Registro de Ingreso/Salida ", font=("Arial", 11, "bold"),
                                   bg="white", padx=20, pady=20)
        form_frame.pack(fill="x", pady=(0, 20))

        # Grid del formulario
        labels = ["Placa:", "Marca:", "Propietario:", "Hora Entrada (HH:MM):", "Hora Salida (HH:MM):"]
        self.entries = {}

        for i, text in enumerate(labels):
            row, col = (0, i) if i < 3 else (1, i - 3)
            tk.Label(form_frame, text=text, bg="white", font=("Arial", 10)).grid(row=row * 2, column=col, sticky="w",
                                                                                 padx=10, pady=(5, 0))
            entry = tk.Entry(form_frame, font=("Arial", 11), relief="solid", bd=1)
            entry.grid(row=row * 2 + 1, column=col, sticky="ew", padx=10, pady=(0, 10))
            self.entries[text] = entry

        # Botones
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

        tk.Button(btn_frame, text="✓ Registrar Vehículo", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  width=20, height=2, command=self._registrar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✖ Limpiar Campos", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  width=20, height=2, command=self._limpiar).pack(side="left", padx=10)

        # --- TABLA DE REGISTROS ---
        table_frame = tk.LabelFrame(main_container, text=" Vehículos en el Garaje ", font=("Arial", 11, "bold"),
                                    bg="white", padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)

        columnas = ("placa", "marca", "propietario", "entrada", "salida", "costo")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings")

        # Configurar encabezados
        titulos = ["Placa", "Marca", "Propietario", "H. Entrada", "H. Salida", "Costo ($)"]
        for col, tit in zip(columnas, titulos):
            self.tabla.heading(col, text=tit)
            self.tabla.column(col, anchor="center", width=120)

        # Scrollbar
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _registrar(self):
        # Obtener datos
        p = self.entries["Placa:"].get().strip()
        m = self.entries["Marca:"].get().strip()
        pr = self.entries["Propietario:"].get().strip()
        he = self.entries["Hora Entrada (HH:MM):"].get().strip()
        hs = self.entries["Hora Salida (HH:MM):"].get().strip()

        if not all([p, m, pr, he, hs]):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        # Calcular costo y crear objeto
        costo = self.servicio.calcular_costo(he, hs)
        nuevo_v = Vehiculo(p, m, pr, he, hs, costo)

        # Guardar en servicio
        self.servicio.registrar_vehiculo(nuevo_v)

        # Actualizar tabla
        self.tabla.insert("", "end", values=(p, m, pr, he, hs, f"${costo:.2f}"))

        messagebox.showinfo("Éxito", f"Vehículo {p} registrado.\nCosto total: ${costo:.2f}")
        self._limpiar()

    def _limpiar(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)