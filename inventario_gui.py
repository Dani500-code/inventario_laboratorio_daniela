import tkinter as tk
from tkinter import ttk, messagebox
import csv, os

ARCHIVO = "inventario.csv"

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nombre", "Cantidad", "Ubicación"])

# ===== FUNCIONES =====
def cargar_datos():
    tree.delete(*tree.get_children())
    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            tree.insert("", tk.END, values=row)

def guardar_datos():
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nombre", "Cantidad", "Ubicación"])
        for row_id in tree.get_children():
            writer.writerow(tree.item(row_id)["values"])

def limpiar_campos():
    for e in (entry_id, entry_nombre, entry_cantidad, entry_ubicacion):
        e.delete(0, tk.END)

def agregar_item():
    valores = [entry_id.get(), entry_nombre.get(), entry_cantidad.get(), entry_ubicacion.get()]
    if not all(valores):
        messagebox.showwarning("Campos incompletos", "Completa todos los campos antes de agregar.")
        return
    tree.insert("", tk.END, values=valores)
    guardar_datos()
    limpiar_campos()

def eliminar_item():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Selecciona un elemento", "Selecciona un ítem para eliminar.")
        return
    for i in sel:
        tree.delete(i)
    guardar_datos()

def editar_item():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Selecciona un elemento", "Selecciona un ítem para editar.")
        return
    i = sel[0]
    valores = [entry_id.get(), entry_nombre.get(), entry_cantidad.get(), entry_ubicacion.get()]
    tree.item(i, values=valores)
    guardar_datos()
    limpiar_campos()

def seleccionar_item(event):
    sel = tree.selection()
    if sel:
        valores = tree.item(sel[0])["values"]
        limpiar_campos()
        entry_id.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])
        entry_cantidad.insert(0, valores[2])
        entry_ubicacion.insert(0, valores[3])

# ===== INTERFAZ =====
root = tk.Tk()
root.title("🧪 Inventario de Laboratorio")
root.geometry("1000x650")
root.config(bg="#f8f9fa")

# ===== ESTILOS =====
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="white",
                foreground="#212529",
                rowheight=32,
                fieldbackground="white",
                font=("Segoe UI", 11))
style.configure("Treeview.Heading",
                background="#007bff",
                foreground="white",
                font=("Segoe UI Semibold", 11))
style.map("Treeview",
          background=[("selected", "#e3f2fd")],
          foreground=[("selected", "#0d47a1")])

# ===== ENCABEZADO =====
lbl_titulo = tk.Label(
    root, text="🧪 Inventario de Laboratorio",
    bg="#f8f9fa", fg="#0d47a1",
    font=("Segoe UI Semibold", 24)
)
lbl_titulo.pack(pady=(20, 10))

# ===== TARJETA FORMULARIO =====
frame_card = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_card.pack(padx=30, pady=10, fill="x")
frame_card.config(highlightbackground="#dee2e6", highlightthickness=1)

for c in range(4):
    frame_card.columnconfigure(c, weight=1)

def label_form(texto, fila, col):
    tk.Label(frame_card, text=texto, bg="white", fg="#495057", font=("Segoe UI", 10, "bold")).grid(
        row=fila, column=col, sticky="e", padx=10, pady=5
    )

label_form("🆔 ID:", 0, 0)
entry_id = tk.Entry(frame_card, font=("Segoe UI", 10), relief="flat", bd=1)
entry_id.grid(row=0, column=1, sticky="w", padx=5, pady=5)

label_form("🔬 Nombre:", 0, 2)
entry_nombre = tk.Entry(frame_card, font=("Segoe UI", 10), width=25, relief="flat", bd=1)
entry_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=5)

label_form("📦 Cantidad:", 1, 0)
entry_cantidad = tk.Entry(frame_card, font=("Segoe UI", 10), relief="flat", bd=1)
entry_cantidad.grid(row=1, column=1, sticky="w", padx=5, pady=5)

label_form("🏷️ Ubicación:", 1, 2)
entry_ubicacion = tk.Entry(frame_card, font=("Segoe UI", 10), width=25, relief="flat", bd=1)
entry_ubicacion.grid(row=1, column=3, sticky="w", padx=5, pady=5)

# ===== BOTONES =====
frame_botones = tk.Frame(root, bg="#f8f9fa")
frame_botones.pack(pady=10)

def boton_moderno(texto, color, comando):
    return tk.Button(
        frame_botones, text=texto, command=comando,
        bg=color, fg="white", activebackground="#343a40",
        font=("Segoe UI Semibold", 11),
        width=14, height=2, relief="flat", cursor="hand2",
        bd=0, highlightthickness=0
    )

boton_moderno("➕ Agregar", "#28a745", agregar_item).grid(row=0, column=0, padx=10, pady=5)
boton_moderno("✏️ Editar", "#17a2b8", editar_item).grid(row=0, column=1, padx=10, pady=5)
boton_moderno("🗑️ Eliminar", "#dc3545", eliminar_item).grid(row=0, column=2, padx=10, pady=5)
boton_moderno("🧹 Limpiar", "#6c757d", limpiar_campos).grid(row=0, column=3, padx=10, pady=5)
boton_moderno("🔄 Recargar", "#007bff", cargar_datos).grid(row=0, column=4, padx=10, pady=5)

# ===== TABLA =====
frame_tabla = tk.Frame(root, bg="white", bd=1, relief="solid")
frame_tabla.pack(padx=30, pady=(10, 30), fill="both", expand=True)
frame_tabla.config(highlightbackground="#dee2e6", highlightthickness=1)

cols = ("ID", "Nombre", "Cantidad", "Ubicación")
tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", selectmode="browse")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=220)

# Scrollbars
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", seleccionar_item)

# ===== CARGAR DATOS =====
cargar_datos()

root.mainloop()
