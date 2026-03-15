import tkinter as tk
from tkinter import ttk, messagebox
from modelos.vehiculo import Vehiculo
from servicios.garaje_servicio import GarajeServicio


class AppGaraje(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Hangar - Sistema de Gestión de Garaje")
        self.geometry("980x720")
        self.configure(bg="#f0f2f5")

        self.servicio = GarajeServicio()
        self.entries: dict[str, tk.Entry] = {}
        self._crear_componentes()

    # ----------------- COMPONENTES UI -----------------

    def _crear_componentes(self):
        # --- HEADER / LOGO ---
        header = tk.Frame(self, bg="#1a2a3a", height=100)
        header.pack(fill="x", padx=0, pady=0)

        tk.Label(header, text="H", font=("Arial Black", 36), fg="white",
                 bg="#3498db", width=2).pack(side="left", padx=20, pady=10)
        tk.Label(header, text="EL HANGAR", font=("Arial Black", 24),
                 fg="white", bg="#1a2a3a").pack(side="left", pady=10)
        tk.Label(header, text="Control de Vehículos y Tarifas",
                 font=("Arial", 12, "italic"), fg="#bdc3c7",
                 bg="#1a2a3a").pack(side="left", padx=20, pady=25)

        # --- CONTENEDOR PRINCIPAL ---
        main_container = tk.Frame(self, bg="#f0f2f5")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # --- FORMULARIO ---
        form_frame = tk.LabelFrame(
            main_container,
            text=" Registro de Ingreso/Salida ",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=20,
            pady=20
        )
        form_frame.pack(fill="x", pady=(0, 20))

        for i in range(3):
            form_frame.columnconfigure(i, weight=1)

        # Fila 1: Placa, Marca, Propietario
        self._crear_entry_con_placeholder(form_frame, "Placa:", "Ej: ABC-1234", 0, 1, 0)
        self._crear_entry_con_placeholder(form_frame, "Marca:", "Ej: Toyota", 0, 1, 1)
        self._crear_entry_con_placeholder(form_frame, "Propietario:", "Ej: Juan Pérez", 0, 1, 2)

        # Fila 2: Horas
        self._crear_entry_con_placeholder(form_frame, "Hora Entrada (HH:MM):", "Ej: 08:30", 2, 3, 0)
        self._crear_entry_con_placeholder(form_frame, "Hora Salida (HH:MM):", "Ej: 14:45", 2, 3, 1)

        # Fila 3: Botones
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(20, 10))

        tk.Button(btn_frame, text="✓ Registrar ENTRADA", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  width=22, height=2, command=self._registrar_entrada, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="🚗 Registrar SALIDA", bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                  width=22, height=2, command=self._registrar_salida, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="✏️ Editar datos", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  width=18, height=2, command=self._editar_vehiculo, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                  width=15, height=2, command=self._eliminar_vehiculo, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="✖ Limpiar Campos", bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                  width=18, height=2, command=self._limpiar_campos, cursor="hand2").pack(side="left", padx=10)

        # --- TABLA ---
        table_frame = tk.LabelFrame(main_container, text=" Vehículos en el Garaje ", font=("Arial", 11, "bold"), bg="white", padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)

        columnas = ("placa", "marca", "propietario", "entrada", "salida", "costo")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", height=12)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        titulos = ["Placa", "Marca", "Propietario", "H. Entrada", "H. Salida", "Costo ($)"]
        for col, tit in zip(columnas, titulos):
            self.tabla.heading(col, text=tit)
            self.tabla.column(col, anchor="center", width=130)

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ----------------- PLACEHOLDERS -----------------

    def _crear_entry_con_placeholder(self, frame, label_text, placeholder, row_label, row_entry, column):
        tk.Label(frame, text=label_text, bg="white", font=("Arial", 10)).grid(
            row=row_label, column=column, sticky="w", padx=10, pady=(5, 0)
        )

        entry = tk.Entry(frame, font=("Arial", 11), relief="solid", bd=1, fg="grey")
        entry.grid(row=row_entry, column=column, sticky="ew", padx=10, pady=(0, 10))
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get().strip() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        self.entries[label_text] = entry

    def _obtener_valor_entry(self, label_text) -> str:
        entry = self.entries[label_text]
        if entry.cget("fg") == "grey":
            return ""
        return entry.get().strip()

    # ----------------- LOGICA -----------------

    def _registrar_entrada(self):
        p = self._obtener_valor_entry("Placa:")
        m = self._obtener_valor_entry("Marca:")
        pr = self._obtener_valor_entry("Propietario:")
        he = self._obtener_valor_entry("Hora Entrada (HH:MM):")

        if not all([p, m, pr, he]):
            messagebox.showwarning("Atención", "Completa los datos de entrada.")
            return

        if self.servicio.buscar_por_placa(p):
            messagebox.showerror("Error", "Placa ya registrada.")
            return

        self.servicio.registrar_entrada(p, m, pr, he)
        self.tabla.insert("", "end", iid=p, values=(p, m, pr, he, "En garaje", "Pendiente"))
        self._limpiar_campos()

    def _registrar_salida(self):
        p = self._obtener_valor_entry("Placa:")
        hs = self._obtener_valor_entry("Hora Salida (HH:MM):")

        if not p or not hs:
            messagebox.showwarning("Atención", "Indica placa y hora de salida.")
            return

        v = self.servicio.registrar_salida(p, hs)
        if v:
            self.tabla.item(p, values=(v.get_placa(), v.get_marca(), v.get_propietario(), v.get_hora_entrada(), v.get_hora_salida(), f"${v.get_costo():.2f}"))
            messagebox.showinfo("Éxito", f"Salida registrada. Costo: ${v.get_costo():.2f}")
            self._limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo procesar la salida.")

    def _editar_vehiculo(self):
        p = self._obtener_valor_entry("Placa:")
        m = self._obtener_valor_entry("Marca:")
        pr = self._obtener_valor_entry("Propietario:")
        if self.servicio.editar_vehiculo(p, m, pr):
            valores = list(self.tabla.item(p, "values"))
            valores[1], valores[2] = m, pr
            self.tabla.item(p, values=valores)
            messagebox.showinfo("Éxito", "Datos actualizados.")
            self._limpiar_campos()

    def _eliminar_vehiculo(self):
        p = self._obtener_valor_entry("Placa:")
        if self.servicio.eliminar_vehiculo(p):
            self.tabla.delete(p)
            messagebox.showinfo("Éxito", "Vehículo eliminado.")
            self._limpiar_campos()

    def _limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            entry.event_generate("<FocusOut>")