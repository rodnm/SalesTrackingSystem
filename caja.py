import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class Store:
    def __init__(self):
        # Inicializa el inventario con productos y sus precios y cantidades
        self.inventory = {
            "pulsera": [3, 50],
            "sticker": [1, 200],
            "llavero": [10, 12],
            "postit": [3.5, 12],
        }
        # Inicializa el registro de ventas
        self.sales_record = {}

    def display_inventory(self):
        # Crea una lista con el encabezado de la tabla
        inventory_list = [
            "{:<15} {:<10} {:<10}".format("Producto", "Precio", "Cantidad")
        ]
        # Añade cada producto y su información formateada
        for producto, info in self.inventory.items():
            precio, cantidad = info
            inventory_list.append(
                "{:<15} {:<10.2f} {:<10}".format(producto, precio, cantidad)
            )
        # Devuelve el inventario como una cadena de texto
        return "\n".join(inventory_list)

    def purchase_product(self, product_name, quantity):
        # Verifica si el producto está en el inventario
        if product_name not in self.inventory:
            return f"'{product_name}' no está disponible en la tienda."

        # Verifica si la cantidad es válida
        if quantity <= 0:
            return "La cantidad debe ser un número positivo."

        # Obtiene el precio y la cantidad disponible del producto
        price, available_quantity = self.inventory[product_name]

        # Verifica si hay suficiente stock
        if quantity <= available_quantity:
            # Calcula el precio total y actualiza el inventario
            total_price = price * quantity
            self.inventory[product_name][1] -= quantity
            # Actualiza el registro de ventas
            self.update_sales_record(product_name, quantity)
            return f"El precio total de {quantity} '{product_name}' es: S/{total_price:.2f}"
        else:
            return f"Lo sentimos, por ahora no contamos con suficiente stock de '{product_name}'. Stock disponible: {available_quantity} unidades."

    def update_sales_record(self, producto, cantidad):
        # Obtiene la fecha y hora actual
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_actual = fecha_hora_actual.split()[0]
        hora_actual = fecha_hora_actual.split()[1]

        # Añade la venta al registro, con fecha, hora y cantidad
        if fecha_actual in self.sales_record:
            self.sales_record[fecha_actual].append((hora_actual, producto, cantidad))
        else:
            self.sales_record[fecha_actual] = [(hora_actual, producto, cantidad)]

    def generate_sales_report(self):
        report_list = []
        total_store_income = 0

        for fecha, ventas in sorted(self.sales_record.items()):
            for venta in ventas:
                hora, producto, cantidad = venta
                precio, _ = self.inventory.get(producto, [0, 0])
                ingresos_producto = precio * cantidad
                total_store_income += ingresos_producto
                report_list.append(
                    (
                        fecha,
                        hora,
                        producto,
                        f"S/{precio:.2f}",
                        cantidad,
                        f"S/{ingresos_producto:.2f}",
                    )
                )

        return report_list, total_store_income

        # Añade el ingreso total al final del informe
        report_list.append(f"Ingreso Total de la Tienda: S/{total_store_income:.2f}")
        return "\n".join(report_list)

    def export_sales_report_to_csv(self, filename):
        # Verifica que el nombre del archivo no esté vacío y que termine en .csv
        if not filename.strip():
            return "El nombre del archivo no puede estar vacío."

        if not filename.endswith(".csv"):
            filename += ".csv"

        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            return f"La ruta del archivo '{directory}' no existe."

        try:
            # Crea o abre el archivo CSV para escritura
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Escribe las columnas del encabezado que se muestran en el informe
                writer.writerow(
                    [
                        "Fecha",
                        "Hora",
                        "Producto",
                        "Precio",
                        "Cantidad Vendida",
                        "Ingresos",
                    ]
                )

                # Escribe cada registro de ventas en el archivo CSV
                for fecha, ventas in self.sales_record.items():
                    for venta in ventas:
                        hora, producto, cantidad_vendida = venta
                        precio, _ = self.inventory.get(producto, [0, 0])
                        ingresos = precio * cantidad_vendida
                        writer.writerow(
                            [
                                fecha,
                                hora,
                                producto,
                                f"S/{precio:.2f}",
                                cantidad_vendida,
                                f"S/{ingresos:.2f}",
                            ]
                        )

            return f"El informe de ventas ha sido exportado a {filename}"
        except Exception as e:
            return f"Ha ocurrido un error al exportar el informe: {e}"

    def export_inventory_to_csv(self, filename):
        # Verifica que el nombre del archivo no esté vacío y que termine en .csv
        if not filename.strip():
            return "El nombre del archivo no puede estar vacío."

        if not filename.endswith(".csv"):
            filename += ".csv"

        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            return f"La ruta del archivo '{directory}' no existe."

        try:
            # Crea o abre el archivo CSV para escritura
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Producto", "Precio", "Cantidad"])

                # Escribe cada producto en el archivo CSV
                for producto, (precio, cantidad) in self.inventory.items():
                    writer.writerow([producto, precio, cantidad])

            return f"El inventario ha sido exportado a {filename}"
        except Exception as e:
            return f"Ha ocurrido un error al exportar el inventario: {e}"

    def load_inventory_from_csv(self, filename):
        # Verifica que el archivo exista
        if not os.path.exists(filename):
            return f"El archivo '{filename}' no existe."

        try:
            # Abre el archivo CSV para lectura
            with open(filename, mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la cabecera
                self.inventory = {
                    rows[0]: [float(rows[1]), int(rows[2])] for rows in reader
                }

            return f"Inventario cargado desde '{filename}'"
        except Exception as e:
            return f"Ha ocurrido un error al cargar el inventario: {e}"


class StoreGUI:
    def __init__(self, root):
        self.store = Store()
        self.root = root
        self.root.title("Simulador de Caja de Venta")
        self.create_widgets()

    def create_widgets(self):
        # Configuración de botones y campos de entrada
        self.inventory_button = tk.Button(
            self.root, text="Mostrar Inventario", command=self.show_inventory
        )
        self.inventory_button.grid(row=0, column=0, padx=10, pady=10)

        self.purchase_label = tk.Label(self.root, text="Comprar Producto:")
        self.purchase_label.grid(row=1, column=0, padx=10, pady=10)

        self.product_label = tk.Label(self.root, text="Producto:")
        self.product_label.grid(row=2, column=0, padx=10, pady=10)
        self.product_entry = tk.Entry(self.root)
        self.product_entry.grid(row=2, column=1, padx=10, pady=10)
        self.product_entry.bind(
            "<Return>", lambda e: self.focus_next_widget(self.quantity_entry)
        )

        self.quantity_label = tk.Label(self.root, text="Cantidad:")
        self.quantity_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)
        self.quantity_entry.bind(
            "<Return>", lambda e: self.focus_next_widget(self.purchase_button)
        )

        self.purchase_button = tk.Button(
            self.root, text="Comprar", command=self.purchase_product
        )
        self.purchase_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.purchase_button.bind("<Return>", lambda e: self.purchase_product())

        # Botones para generar y exportar informes
        self.report_button = tk.Button(
            self.root,
            text="Generar Informe de Ventas",
            command=self.generate_sales_report,
        )
        self.report_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.export_sales_button = tk.Button(
            self.root,
            text="Exportar Informe de Ventas a CSV",
            command=self.export_sales_report,
        )
        self.export_sales_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.export_inventory_button = tk.Button(
            self.root, text="Exportar Inventario a CSV", command=self.export_inventory
        )
        self.export_inventory_button.grid(
            row=7, column=0, columnspan=2, padx=10, pady=10
        )

        # Botón para cargar el inventario desde un archivo CSV
        self.load_inventory_button = tk.Button(
            self.root, text="Cargar Inventario desde CSV", command=self.load_inventory
        )
        self.load_inventory_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def focus_next_widget(self, next_widget):
        # Cambia el enfoque a la siguiente entrada o botón
        next_widget.focus()

    def show_inventory(self):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventario de Productos")
        inventory_window.geometry("400x250")

        # Crear un Treeview para mostrar los productos en formato de tabla
        tree = ttk.Treeview(
            inventory_window,
            columns=("Producto", "Precio", "Cantidad"),
            show="headings",
        )

        # Encabezados clickeables para ordenar
        tree.heading(
            "Producto",
            text="Producto",
            command=lambda: self.sort_inventory(
                tree, "Producto", False, is_numeric=False
            ),
        )
        tree.heading(
            "Precio",
            text="Precio",
            command=lambda: self.sort_inventory(tree, "Precio", False, is_numeric=True),
        )
        tree.heading(
            "Cantidad",
            text="Cantidad",
            command=lambda: self.sort_inventory(
                tree, "Cantidad", False, is_numeric=True
            ),
        )

        # Ajustar el ancho de las columnas
        tree.column("Producto", width=150)
        tree.column("Precio", width=100)
        tree.column("Cantidad", width=100)

        # Insertar datos en el Treeview
        for producto, (precio, cantidad) in self.store.inventory.items():
            tree.insert("", tk.END, values=(producto, f"S/{precio:.2f}", cantidad))

        tree.pack(expand=True, fill="both")

        close_button = tk.Button(
            inventory_window, text="Cerrar", command=inventory_window.destroy
        )
        close_button.pack(pady=10)

    def sort_inventory(self, tree, col, reverse, is_numeric):
        # Obtener todos los elementos de la tabla
        items = []
        for k in tree.get_children(""):
            value = tree.set(k, col)
            # Convertir a float si es precio o cantidad; para precio, quitar el símbolo "S/"
            if is_numeric:
                value = float(value[2:]) if col == "Precio" else float(value)
            items.append((value, k))

        # Ordenar por el valor de la columna seleccionada
        items.sort(reverse=reverse)

        # Reordenar los elementos en la tabla
        for index, (val, k) in enumerate(items):
            tree.move(k, "", index)

        # Alternar el orden para el próximo clic
        tree.heading(
            col, command=lambda: self.sort_inventory(tree, col, not reverse, is_numeric)
        )

    def purchase_product(self):
        # Realiza una compra y muestra el resultado en un cuadro de mensaje
        product_name = self.product_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        result = self.store.purchase_product(product_name, quantity)
        self.show_message("Compra", result)

    def show_message(self, title, message):
        # Función personalizada para mostrar un mensaje y permitir el uso de "Enter" para cerrarlo
        response = messagebox.showinfo(title, message)
        if response == "ok":
            self.root.focus()  # Regresa el enfoque a la ventana principal

    def generate_sales_report(self):
        report_data, total_income = self.store.generate_sales_report()

        # Crear una nueva ventana para mostrar el informe
        report_window = tk.Toplevel(self.root)
        report_window.title("Informe de Ventas")
        report_window.geometry("1200x400")

        # Crear un Frame para incluir el Treeview y el scrollbar
        frame = tk.Frame(report_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Treeview para mostrar las ventas
        columns = (
            "Fecha",
            "Hora",
            "Producto",
            "Precio",
            "Cantidad Vendida",
            "Ingresos",
        )
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Definir los encabezados
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=100, stretch=True)

        # Añadir un Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insertar los datos en el Treeview
        for venta in report_data:
            tree.insert("", tk.END, values=venta)

        # Añadir el Treeview al Frame
        tree.pack(fill=tk.BOTH, expand=True)

        # Mostrar el ingreso total al final de la ventana
        total_label = tk.Label(
            report_window,
            text=f"Ingreso Total: S/{total_income:.2f}",
            font=("Arial", 12, "bold"),
        )
        total_label.pack(pady=10)

        # Añadir funcionalidad para ajustar el tamaño y activar el scroll
        frame.pack(fill=tk.BOTH, expand=True)
        tree.pack(fill=tk.BOTH, expand=True)

    def export_sales_report(self):
        # Exporta el informe de ventas a un archivo CSV
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filename:
            result = self.store.export_sales_report_to_csv(filename)
            messagebox.showinfo("Exportar Informe de Ventas", result)

    def export_inventory(self):
        # Exporta el inventario a un archivo CSV
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filename:
            result = self.store.export_inventory_to_csv(filename)
            messagebox.showinfo("Exportar Inventario", result)

    def load_inventory(self):
        # Carga el inventario desde un archivo CSV
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            result = self.store.load_inventory_from_csv(filename)
            messagebox.showinfo("Cargar Inventario", result)

    def on_closing(self):
        # Pregunta al usuario si desea guardar el inventario e informe de ventas
        if messagebox.askyesnocancel(
            "Salir",
            "¿Desea guardar el inventario e informe de ventas antes de salir?\nRecuerda: primero se guarda el inventario final y después se guarda el informe de ventas final.",
        ):
            # Si elige "Sí", muestra los cuadros de diálogo para guardar el inventario e informe de ventas
            self.export_inventory()
            self.export_sales_report()
            # Después de guardar, cierra la aplicación
            self.root.destroy()
        elif messagebox.askyesno(
            "Salir", "¿Está seguro de que desea salir sin guardar?"
        ):
            # Si elige "No guardar", cierra la aplicación
            self.root.destroy()
        # Si elige "Cancelar", no hace nada y deja la ventana abierta


if __name__ == "__main__":
    root = tk.Tk()
    app = StoreGUI(root)
    # Configura el evento de cierre de la ventana principal para llamar a `on_closing`
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
