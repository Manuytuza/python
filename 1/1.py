def saludo () : 
            print ("Hola, bienvenido a la tienda de Arequipa!")
            nombre = input("Escribe tu nombre  ")
            razon = input("¿por quien lo haces?  ")
            print(f"Hola {nombre}, gracias por hacer esto por {razon}.")


def add_numbers() -> int:
    print("Vamos a sumar dos números.")
    x = int(input("Ingresa primer número: "))
    y = int(input("Ingresa segundo número: "))
    print(f"La suma de {x} + {y} es igual a {x + y}")


stock = ["Iphone: 10", "Mac: 5", "Airpods: 14"]

def list_product() -> None:
    print("Stock actual:")
    for item in stock:
        print(" -", item)

def add_product() -> None:
    item = str(input (f"Ingresa el producto: "))
    quantity = int(input("Ingresa la cantidad: "))
    stock.append(f"{item} : {quantity}")
    print(f"Producto '{item}' agregado con cantidad {quantity}.")

#ingresamor punto 4 CRM_CHAT_GTP
# clase_04_menu.py

# Lista inicial del stock
stock = ["Iphone: 10", "Mac: 5", "Airpods: 14"]

# Función para listar productos
def list_product() -> None:
    print("\nStock actual:")   # \n hace un salto de línea antes de imprimir
    for item in stock:         # Recorre la lista 'stock' producto por producto
        print(" -", item)      # Imprime cada producto con un guion

# Función para agregar producto
def add_product(name: str, quantity: int) -> None:
    stock.append(f"{name}: {quantity}")     # Agrega nuevo producto con f-string
    print(f"Producto '{name}' agregado con cantidad {quantity}.")

# Función para eliminar producto
def remove_product(name: str) -> None:
    for i, item in enumerate(stock):             # enumerate da índice + valor
        nombre, _, _ = item.partition(":")       # separa "Nombre: cantidad"
        if nombre.strip().lower() == name.strip().lower():  # compara ignorando mayúsculas/minúsculas
            eliminado = stock.pop(i)             # elimina por índice
            print(f"Eliminado: {eliminado}")
            return                               # sale de la función
    print("No se encontró el producto.")         # si no encontró, avisa

# Función para actualizar producto
def update_product(name: str, new_quantity: int) -> None:
    for i, item in enumerate(stock):
        nombre, _, _ = item.partition(":")
        if nombre.strip().lower() == name.strip().lower():
            stock[i] = f"{nombre.strip()}: {new_quantity}"  # reemplaza cantidad
            print(f"Actualizado: {stock[i]}")
            return
    print("No se encontró el producto.")

# Función principal del menú
def menu() -> None:
    while True:                        # Bucle infinito hasta que elijas salir
        print("\n--- Menú ---")
        print("1) Listar productos")
        print("2) Agregar producto")
        print("3) Eliminar producto")
        print("4) Actualizar cantidad")
        print("5) Salir")

        opcion = input("Elige una opción: ").strip()   # lee opción como string

        if opcion == "1":
            list_product()
        elif opcion == "2":
            nombre = input("Nombre del producto: ").strip()
            try:
                cantidad = int(input("Cantidad: ").strip())  # convierte a entero
            except ValueError:
                print("Cantidad inválida.")   # si no es número, error controlado
                continue
            add_product(nombre, cantidad)
        elif opcion == "3":
            nombre = input("Nombre del producto a eliminar: ").strip()
            remove_product(nombre)
        elif opcion == "4":
            nombre = input("Producto a actualizar: ").strip()
            try:
                nueva_cantidad = int(input("Nueva cantidad: ").strip())
            except ValueError:
                print("Cantidad inválida.")
                continue
            update_product(nombre, nueva_cantidad)
        elif opcion == "5":
            print("Saliendo...")
            break   # rompe el while y termina el programa
        else:
            print("Opción inválida.")   # si eliges otra cosa, avisa

# Punto de entrada del programa
if __name__ == "__main__":
    menu()
