import turtle

# Crear ventana
window = turtle.Screen()

# Crear tortuga
tortuga = turtle.Turtle()

# Opcional: Cambiar color
tortuga.color("yellow")  # Color amarillo como los letreros de peligro
tortuga.fillcolor("yellow")
tortuga.begin_fill()

# Dibujar triángulo
for _ in range(3):
    tortuga.forward(150)  # Avanza 150 pasos
    tortuga.left(120)     # Gira 120 grados a la izquierda

tortuga.end_fill()

# Dejar ventana abierta
window.mainloop()

1+5=
