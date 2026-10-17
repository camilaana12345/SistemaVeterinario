
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- BASE DE DATOS ----------------

conexion = sqlite3.connect("veterinaria.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    raza TEXT,
    edad INTEGER,
    propietario TEXT NOT NULL,
    telefono TEXT
)
""")

conexion.commit()


# ---------------- FUNCIONES ----------------

def limpiar_campos():
    entrada_nombre.delete(0, tk.END)
    entrada_especie.delete(0, tk.END)
    entrada_raza.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_propietario.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)


def cargar_mascotas():
    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("SELECT * FROM mascotas")
    for mascota in cursor.fetchall():
        tabla.insert("", tk.END, values=mascota)


def registrar_mascota():
    nombre = entrada_nombre.get().strip()
    especie = entrada_especie.get().strip()
    raza = entrada_raza.get().strip()
    edad_texto = entrada_edad.get().strip()
    propietario = entrada_propietario.get().strip()
    telefono = entrada_telefono.get().strip()

    if not nombre or not especie or not propietario:
        messagebox.showwarning(
            "Campos obligatorios",
            "Ingresa el nombre, la especie y el propietario."
        )
        return

    if edad_texto:
        try:
            edad = int(edad_texto)
            if edad < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "La edad debe ser un número entero positivo."
            )
            return
    else:
        edad = None

    cursor.execute("""
        INSERT INTO mascotas
        (nombre, especie, raza, edad, propietario, telefono)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, especie, raza, edad, propietario, telefono))

    conexion.commit()
    cargar_mascotas()
    limpiar_campos()

    messagebox.showinfo(
        "Registro exitoso",
        "La mascota fue registrada correctamente."
    )


def eliminar_mascota():
    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning(
            "Atención",
            "Selecciona una mascota de la tabla."
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Deseas eliminar la mascota seleccionada?"
    )

    if confirmar:
        valores = tabla.item(seleccion[0], "values")
        cursor.execute(
            "DELETE FROM mascotas WHERE id = ?", (valores[0],)
        )
        conexion.commit()
        cargar_mascotas()
        limpiar_campos()

        messagebox.showinfo(
            "Correcto",
            "La mascota fue eliminada."
        )


def seleccionar_mascota(event):
    seleccion = tabla.selection()

    if seleccion:
        valores = tabla.item(seleccion[0], "values")

        limpiar_campos()
        entrada_nombre.insert(0, valores[1])
        entrada_especie.insert(0, valores[2])
        entrada_raza.insert(0, valores[3])

        if valores[4] != "":
            entrada_edad.insert(0, valores[4])

        entrada_propietario.insert(0, valores[5])
        entrada_telefono.insert(0, valores[6])


def buscar_mascota():
    termino = entrada_busqueda.get().strip()

    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("""
        SELECT * FROM mascotas
        WHERE nombre LIKE ?
        OR especie LIKE ?
        OR propietario LIKE ?
    """, (
        f"%{termino}%",
        f"%{termino}%",
        f"%{termino}%"
    ))

    for mascota in cursor.fetchall():
        tabla.insert("", tk.END, values=mascota)


def mostrar_todas():
    entrada_busqueda.delete(0, tk.END)
    cargar_mascotas()


def cerrar_programa():
    conexion.close()
    ventana.destroy()


# ---------------- VENTANA PRINCIPAL ----------------

ventana = tk.Tk()
ventana.title("Sistema de Gestión Veterinaria")
ventana.geometry("1000x650")
ventana.minsize(850, 550)
ventana.configure(bg="#EAF2F8")

titulo = tk.Label(
    ventana,
    text="SISTEMA DE GESTIÓN VETERINARIA",
    font=("Arial", 20, "bold"),
    bg="#1F618D",
    fg="white",
    pady=15
)
titulo.pack(fill="x")

# ---------------- FORMULARIO ----------------

marco_formulario = tk.LabelFrame(
    ventana,
    text="Datos de la mascota y su propietario",
    font=("Arial", 11, "bold"),
    bg="#EAF2F8",
    padx=15,
    pady=10
)
marco_formulario.pack(fill="x", padx=15, pady=12)

tk.Label(marco_formulario, text="Nombre:", bg="#EAF2F8").grid(
    row=0, column=0, sticky="w", padx=5, pady=6
)
entrada_nombre = tk.Entry(marco_formulario, width=25)
entrada_nombre.grid(row=0, column=1, padx=5, pady=6)

tk.Label(marco_formulario, text="Especie:", bg="#EAF2F8").grid(
    row=0, column=2, sticky="w", padx=5, pady=6
)
entrada_especie = tk.Entry(marco_formulario, width=25)
entrada_especie.grid(row=0, column=3, padx=5, pady=6)

tk.Label(marco_formulario, text="Raza:", bg="#EAF2F8").grid(
    row=1, column=0, sticky="w", padx=5, pady=6
)
entrada_raza = tk.Entry(marco_formulario, width=25)
entrada_raza.grid(row=1, column=1, padx=5, pady=6)

tk.Label(marco_formulario, text="Edad:", bg="#EAF2F8").grid(
    row=1, column=2, sticky="w", padx=5, pady=6
)
entrada_edad = tk.Entry(marco_formulario, width=25)
entrada_edad.grid(row=1, column=3, padx=5, pady=6)

tk.Label(marco_formulario, text="Propietario:", bg="#EAF2F8").grid(
    row=2, column=0, sticky="w", padx=5, pady=6
)
entrada_propietario = tk.Entry(marco_formulario, width=25)
entrada_propietario.grid(row=2, column=1, padx=5, pady=6)

tk.Label(marco_formulario, text="Teléfono:", bg="#EAF2F8").grid(
    row=2, column=2, sticky="w", padx=5, pady=6
)
entrada_telefono = tk.Entry(marco_formulario, width=25)
entrada_telefono.grid(row=2, column=3, padx=5, pady=6)

# ---------------- BOTONES ----------------

marco_botones = tk.Frame(ventana, bg="#EAF2F8")
marco_botones.pack(pady=5)

tk.Button(
    marco_botones, text="Registrar mascota",
    command=registrar_mascota,
    bg="#229954", fg="white", width=18
).grid(row=0, column=0, padx=5)

tk.Button(
    marco_botones, text="Eliminar seleccionada",
    command=eliminar_mascota,
    bg="#C0392B", fg="white", width=18
).grid(row=0, column=1, padx=5)

tk.Button(
    marco_botones, text="Limpiar campos",
    command=limpiar_campos,
    width=15
).grid(row=0, column=2, padx=5)

# ---------------- BUSCADOR ----------------

marco_busqueda = tk.Frame(ventana, bg="#EAF2F8")
marco_busqueda.pack(fill="x", padx=15, pady=8)

tk.Label(
    marco_busqueda, text="Buscar mascota:",
    bg="#EAF2F8", font=("Arial", 10, "bold")
).pack(side="left", padx=5)

entrada_busqueda = tk.Entry(marco_busqueda, width=30)
entrada_busqueda.pack(side="left", padx=5)

tk.Button(
    marco_busqueda, text="Buscar",
    command=buscar_mascota
).pack(side="left", padx=5)

tk.Button(
    marco_busqueda, text="Mostrar todas",
    command=mostrar_todas
).pack(side="left", padx=5)

# ---------------- TABLA DE PACIENTES ----------------

marco_tabla = tk.Frame(ventana)
marco_tabla.pack(fill="both", expand=True, padx=15, pady=10)

columnas = (
    "ID", "Nombre", "Especie", "Raza",
    "Edad", "Propietario", "Teléfono"
)

tabla = ttk.Treeview(
    marco_tabla,
    columns=columnas,
    show="headings"
)

for columna in columnas:
    tabla.heading(columna, text=columna)
    tabla.column(columna, width=110, anchor="center")

tabla.column("ID", width=45)
tabla.column("Nombre", width=120)
tabla.column("Propietario", width=150)

barra = ttk.Scrollbar(
    marco_tabla, orient="vertical", command=tabla.yview
)
tabla.configure(yscrollcommand=barra.set)

tabla.pack(side="left", fill="both", expand=True)
barra.pack(side="right", fill="y")

tabla.bind("<<TreeviewSelect>>", seleccionar_mascota)

# ---------------- INICIAR SISTEMA ----------------

cargar_mascotas()
ventana.protocol("WM_DELETE_WINDOW", cerrar_programa)
ventana.mainloop()
