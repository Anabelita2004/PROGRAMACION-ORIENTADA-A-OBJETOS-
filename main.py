import json


class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


class Inventario:
    def __init__(self):
        self.productos = {}
        self.cargar_desde_archivo()

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            print("Error: El ID ya existe en el inventario.")
        else:
            self.productos[producto.id_producto] = producto
            print("Producto agregado correctamente.")
            self.guardar_en_archivo()

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("Producto eliminado correctamente.")
            self.guardar_en_archivo()
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].cantidad = cantidad
            if precio is not None:
                self.productos[id_producto].precio = precio
            print("Producto actualizado correctamente.")
            self.guardar_en_archivo()
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        return resultados if resultados else "No se encontraron productos."

    def mostrar_inventario(self):
        if self.productos:
            for producto in self.productos.values():
                print(producto)
        else:
            print("El inventario está vacío.")

    def guardar_en_archivo(self, archivo="inventario.json"):
        with open(archivo, "w") as f:
            json.dump({id: vars(p) for id, p in self.productos.items()}, f)

    def cargar_desde_archivo(self, archivo="inventario.json"):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                self.productos = {int(id): Producto(**info) for id, info in datos.items()}
        except FileNotFoundError:
            self.productos = {}
        except json.JSONDecodeError:
            print("Error al cargar el archivo de inventario.")


def menu():
    inventario = Inventario()
    while True:
        print("\n--- MENÚ DE INVENTARIO ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar inventario")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = int(input("ID del producto: "))
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            inventario.agregar_producto(Producto(id_producto, nombre, cantidad, precio))
        elif opcion == "2":
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            inventario.eliminar_producto(id_producto)
        elif opcion == "3":
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))
            cantidad = input("Nueva cantidad (deje vacío para no cambiar): ")
            precio = input("Nuevo precio (deje vacío para no cambiar): ")
            inventario.actualizar_producto(id_producto, int(cantidad) if cantidad else None,
                                           float(precio) if precio else None)
        elif opcion == "4":
            nombre = input("Ingrese el nombre del producto a buscar: ")
            resultados = inventario.buscar_producto(nombre)
            if isinstance(resultados, str):
                print(resultados)
            else:
                for p in resultados:
                    print(p)
        elif opcion == "5":
            inventario.mostrar_inventario()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
