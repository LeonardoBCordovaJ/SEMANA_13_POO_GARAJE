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
        self._crear_entry_con_placeholder(
            frame=form_frame,
            label_text="Placa:",
            placeholder="Ej: ABC-1234",
            row_label=0,
            row_entry=1,
            column=0
        )
        self._crear_entry_con_placeholder(
            frame=form_frame,
            label_text="Marca:",
            placeholder="Ej: Toyota",
            row_label=0,
            row_entry=1,
            column=1
        )
        self._crear_entry_con_placeholder(
            frame=form_frame,
            label_text="Propietario:",
            placeholder="Ej: Juan Pérez",
            row_label=0,
            row_entry=1,
            column=2
        )

        # Fila 2: Horas
        self._crear_entry_con_placeholder(
            frame=form_frame,
            label_text="Hora Entrada (HH:MM):",
            placeholder="Ej: 08:30",
            row_label=2,
            row_entry=3,
            column=0
        )
        self._crear_entry_con_placeholder(
            frame=form_frame,
            label_text="Hora Salida (HH:MM):",
            placeholder="Ej: 14:45",
            row_label=2,
            row_entry=3,
            column=1
        )

        # Fila 3: Botones
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(20, 10))

        tk.Button(
            btn_frame,
            text="✓ Registrar ENTRADA",
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            height=2,
            command=self._registrar_entrada,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="🚗 Registrar SALIDA",
            bg="#2980b9",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            height=2,
            command=self._registrar_salida,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="✏️ Editar datos",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2,
            command=self._editar_vehiculo,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            bg="#c0392b",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            height=2,
            command=self._eliminar_vehiculo,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="✖ Limpiar Campos",
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2,
            command=self._limpiar_campos,
            cursor="hand2"
        ).pack(side="left", padx=10)

        # --- TABLA ---
        table_frame = tk.LabelFrame(
            main_container,
            text=" Vehículos en el Garaje ",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
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

        def on_focus_in(event, ph=placeholder):
            if entry.get() == ph:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event, ph=placeholder):
            if entry.get().strip() == "":
                entry.insert(0, ph)
                entry.config(fg="grey")

        entry.bind("<​FocusIn>", on_focus_in)
        entry.bind("<​FocusOut>", on_focus_out)

        self.entries[label_text] = entry

    def _obtener_valor_entry(self, label_text) -> str:
        """
        Devuelve el valor del entry sin el placeholder.
        """
        entry = self.entries[label_text]
        valor = entry.get().strip()
        # Si esta en gris, significa que sigue el placeholder
        if entry.cget("fg") == "grey":
            return ""
        return valor

    # ----------------- LOGICA DE NEGOCIO (UI) -----------------

    def _registrar_entrada(self):
        placa = self._obtener_valor_entry("Placa:")
        marca = self._obtener_valor_entry("Marca:")
        propietario = self._obtener_valor_entry("Propietario:")
        hora_ent = self._obtener_valor_entry("Hora Entrada (HH:MM):")

        if not all([placa, marca, propietario, hora_ent]):
            messagebox.showwarning("Atención", "Para registrar ENTRADA debes completar placa, marca, propietario y hora de entrada.")
            return

        if self.servicio.buscar_por_placa(placa):
            messagebox.showerror("Error", "Ya existe un vehículo con esa placa en el sistema.")
            return

        vehiculo = self.servicio.registrar_entrada(placa, marca, propietario, hora_ent)

        self.tabla.insert(
            "",
            "end",
            iid=vehiculo.get_placa(),
            values=(placa, marca, propietario, hora_ent, "En garaje", "Pendiente")
        )

        messagebox.showinfo("Éxito", f"Entrada registrada para el vehículo {placa}.")
        self._limpiar_campos()

    def _registrar_salida(self):
        placa = self._obtener_valor_entry("Placa:")
        hora_sal = self._obtener_valor_entry("Hora Salida (HH:MM):")

        if not placa or not hora_sal:
            messagebox.showwarning("Atención", "Para registrar SALIDA debes indicar la placa y la hora de salida.")
            return

        vehiculo = self.servicio.registrar_salida(placa, hora_sal)
        if vehiculo is None:
            messagebox.showerror("Error", "No se pudo registrar la salida. Verifica la placa y las horas.")
            return

        costo = vehiculo.get_costo()

        # Actualizar fila en la tabla
        if self.tabla.exists(placa):
            self.tabla.item(
                placa,
                values=(
                    vehiculo.get_placa(),
                    vehiculo.get_marca(),
                    vehiculo.get_propietario(),
                    vehiculo.get_hora_entrada(),
                    vehiculo.get_hora_salida(),
                    f"${costo:.2f}"
                )
            )

        messagebox.showinfo(
            "Salida registrada",
            f"Vehículo {placa} retirado.\nTiempo calculado y costo total: ${costo:.2f}"
        )
        self._limpiar_campos()

    def _editar_vehiculo(self):
        placa = self._obtener_valor_entry("Placa:")
        nueva_marca = self._obtener_valor_entry("Marca:")
        nuevo_prop = self._obtener_valor_entry("Propietario:")

        if not placa or not nueva_marca or not nuevo_prop:
            messagebox.showwarning("Atención", "Para editar debes indicar placa, nueva marca y nuevo propietario.")
            return

        ok = self.servicio.editar_vehiculo(placa, nueva_marca, nuevo_prop)
        if not ok:
            messagebox.showerror("Error", "No se encontró un vehículo con esa placa.")
            return

        # Actualizar en tabla
        if self.tabla.exists(placa):
            valores = list(self.tabla.item(placa, "values"))
            valores[1] = nueva_marca
            valores[2] = nuevo_prop
            self.tabla.item(placa, values=valores)

        messagebox.showinfo("Éxito", f"Datos del vehículo {placa} actualizados.")
        self._limpiar_campos()

    def _eliminar_vehiculo(self):
        placa = self._obtener_valor_entry("Placa:")
        if not placa:
            messagebox.showwarning("Atención", "Indica la placa del vehículo que deseas eliminar.")
            return

        if not self.servicio.eliminar_vehiculo(placa):
            messagebox.showerror("Error", "No se encontró un vehículo con esa placa.")
            return

        if self.tabla.exists(placa):
            self.tabla.delete(placa)

        messagebox.showinfo("Eliminado", f"Vehículo {placa} eliminado del sistema.")
        self._limpiar_campos()

    def _limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            # forzamos el evento de salida de foco para restaurar placeholder
            entry.event_generate("<​FocusOut>")