import random

def juego_adivina_numero():
    numero_secreto = random.randint(1, 100)
    intentos = 0

    print("Estoy pensando en un número entre 1 y 100.")
    while True:
        try:
            adivinanza = int(input("Intenta adivinar el número: "))
            intentos += 1
            if adivinanza < numero_secreto:
                print("Muy bajo, intenta de nuevo.")
            elif adivinanza > numero_secreto:
                print("Muy alto, intenta de nuevo.")
            else:
                print(f"¡Felicidades! Adivinaste el número en {intentos} intentos.")
                break
        except ValueError:
            print("Por favor, ingresa un número válido.")

if __name__ == "__main__":
    juego_adivina_numero()