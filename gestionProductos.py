import json
import os

# Clase base Producto
class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad
        }

# Clases derivadas
class ProductoElectrónico(Producto):
    def __init__(self, nombre, precio, cantidad, marca, voltaje):
        super().__init__(nombre, precio, cantidad)
        self.marca = marca
        self.voltaje = voltaje

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'marca': self.marca,
            'voltaje': self.voltaje
        })
        return data

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, fecha_expedicion, fecha_caducidad):
        super().__init__(nombre, precio, cantidad)
        self.fecha_expedicion = fecha_expedicion
        self.fecha_caducidad = fecha_caducidad

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'fecha_expedicion': self.fecha_expedicion,
            'fecha_caducidad': self.fecha_caducidad
        })
        return data

# Funciones CRUD
def guardar_datos(productos, archivo='productos.json'):
    with open(archivo, 'w') as f:
        json.dump([prod.to_dict() for prod in productos], f, indent=4)

def cargar_datos(archivo='productos.json'):
    if not os.path.exists(archivo):
        return []
    with open(archivo, 'r') as f:
        data = json.load(f)
        productos = []
        for item in data:
            if 'voltaje' in item:  # Asumimos que si tiene 'voltaje', es un ProductoElectrónico
                productos.append(ProductoElectrónico(**item))
            elif 'fecha_caducidad' in item:  # Asumimos que si tiene 'fecha_caducidad', es un ProductoAlimenticio
                productos.append(ProductoAlimenticio(**item))
            else:
                productos.append(Producto(**item))
        return productos

def crear_producto(productos):
    try:
        tipo = input("Tipo de producto (electrónico/alimenticio): ").strip().lower()
        nombre = input("Nombre: ").strip()
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad en stock: "))
        
        if tipo == 'electrónico':
            marca = input("Marca: ").strip()
            voltaje = input("Voltaje: ").strip()
            producto = ProductoElectrónico(nombre, precio, cantidad, marca, voltaje)
        elif tipo == 'alimenticio':
            fecha_expedicion = input("Fecha de expedición (YYYY-MM-DD): ").strip()
            fecha_caducidad = input("Fecha de caducidad (YYYY-MM-DD): ").strip()
            producto = ProductoAlimenticio(nombre, precio, cantidad, fecha_expedicion, fecha_caducidad)
        else:
            print("Tipo de producto no reconocido.")
            return
        
        productos.append(producto)
        print("Producto creado exitosamente.")
    except ValueError as e:
        print(f"Error en los datos ingresados: {e}")

def listar_productos(productos):
    for idx, producto in enumerate(productos):
        print(f"{idx + 1}. {producto.to_dict()}")

def actualizar_producto(productos):
    listar_productos(productos)
    try:
        idx = int(input("Número del producto a actualizar: ")) - 1
        if idx < 0 or idx >= len(productos):
            print("Índice inválido.")
            return
        
        producto = productos[idx]
        print(f"Actualizando {producto.nombre}")
        nuevo_nombre = input(f"Nuevo nombre ({producto.nombre}): ").strip()
        if nuevo_nombre:
            producto.nombre = nuevo_nombre
        
        nuevo_precio = input(f"Nuevo precio ({producto.precio}): ").strip()
        if nuevo_precio:
            producto.precio = float(nuevo_precio)
        
        nueva_cantidad = input(f"Nueva cantidad ({producto.cantidad}): ").strip()
        if nueva_cantidad:
            producto.cantidad = int(nueva_cantidad)
        
        if isinstance(producto, ProductoElectrónico):
            nueva_marca = input(f"Nueva marca ({producto.marca}): ").strip()
            if nueva_marca:
                producto.marca = nueva_marca
            nuevo_voltaje = input(f"Nuevo voltaje ({producto.voltaje}): ").strip()
            if nuevo_voltaje:
                producto.voltaje = nuevo_voltaje
        elif isinstance(producto, ProductoAlimenticio):
            nueva_fecha_expedicion = input(f"Nueva fecha de expedición ({producto.fecha_expedicion}): ").strip()
            if nueva_fecha_expedicion:
                producto.fecha_expedicion = nueva_fecha_expedicion
            nueva_fecha_caducidad = input(f"Nueva fecha de caducidad ({producto.fecha_caducidad}): ").strip()
            if nueva_fecha_caducidad:
                producto.fecha_caducidad = nueva_fecha_caducidad
        
        print("Producto actualizado exitosamente.")
    except ValueError as e:
        print(f"Error en los datos ingresados: {e}")

def eliminar_producto(productos):
    listar_productos(productos)
    try:
        idx = int(input("Número del producto a eliminar: ")) - 1
        if idx < 0 or idx >= len(productos):
            print("Índice inválido.")
            return
        
        productos.pop(idx)
        print("Producto eliminado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def menu():
    productos = cargar_datos()
    while True:
        print("\nSistema de Gestión de Productos")
        print("1. Crear producto")
        print("2. Listar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_producto(productos)
        elif opcion == '2':
            listar_productos(productos)
        elif opcion == '3':
            actualizar_producto(productos)
        elif opcion == '4':
            eliminar_producto(productos)
        elif opcion == '5':
            guardar_datos(productos)
            print("Datos guardados. Salir...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    menu()