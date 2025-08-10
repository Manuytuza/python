stock = ["Iphone: 10", "Mac: 5", "Airpods.14"]
age_years = 4
age_months = 11
fin_code =(
    f"Dios es primero, hagamoslo por Alice tiene {age_years} años, {age_months} meses y es la mejor programadora del mundo"
) 


def add_numbers(x: int, y: int) -> int:
    x = int(input("Ingresa primer número: "))
    y = int(input("Ingresa segundo número: "))
    print(f"La suma de {x} + {y} es igual a {x + y}")


def list_product():
    global stock
    print(stock)

def add_product(name:str , quanty: int):
    global stock
    item = f"{name}: {quanty}"
    stock.append(item)
    print(f"Producto {name} agregado con cantidad {quanty}")
    list_product()

def main():
    nombre = input("¿Cómo te llamas? ")
    print(f"Hola, {nombre}. Bienvenido a Python en tu MacBook.")   



if __name__ == "__main__":
    add_product("Ipad", 3)
    add_numbers()
    print(fin_code)
    main()


    
    





