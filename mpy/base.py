stock = ["Iphone: 10", "Mac: 5", "Airpods.14"]
age_years = 4
age_months = 11
fin_code =(
    f"Dios es primero, hagamoslo por Alice tiene {age_years} años, {age_months} meses y es la mejor programadora del mundo"
) 


def add_numbers(x: int, y: int) -> int:
    return x + y

def list_product():
    global stock
    print(stock)

def add_product(name:str , quanty: int):
    global stock
    item = f"{name}: {quanty}"
    stock.append(item)
    print(f"Producto {name} agregado con cantidad {quanty}")
    list_product()
    
if __name__ == "__main__":
    add_product("Ipad", 3)
    print(add_numbers(2,3))
    print(fin_code)

    
    





