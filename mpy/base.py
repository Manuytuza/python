stock = "Iphone, Mac, Airpods"
age = "4 years, and 11 months"
fin_code = f"Dios es primero, hagamoslo por Alice tiene {age} años"


def sum (x,y):
    return x + y

def list_client():
    global stock
    print(stock)

def create_client(client_name):
    list_client()
    global stock
    _add_coma()
    stock += client_name
    list_client()
    

def _add_coma():
    global stock
    stock +=(", ")



if __name__ == "__main__":
    create_client("Ipad")
    print(sum(2,3))
    print(fin_code)

    
    





