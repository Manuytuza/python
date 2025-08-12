def reporte_tienda():
    IGV = 0.18
    META_MENSUAL = 1_000_000  # sin IGV
    
    print("=== Reporte Tienda Arequipa ===")
    
    # Ingreso de datos
    venta_sin_igv = float(input("Venta Total sin IGV (S/.): "))
    accesorios_sin_igv = float(input("Monto de accesorios vendidos sin IGV (S/.): "))
    iphones = int(input("Cantidad iPhone vendidos: "))
    macs = int(input("Cantidad Mac vendidos: "))
    ipads = int(input("Cantidad iPad vendidos: "))
    watch = int(input("Cantidad Watch vendidos: "))
    airpods = int(input("Cantidad AirPods vendidos: "))
    transacciones = int(input("Cantidad de transacciones: "))
    trafico = int(input("Tráfico del día (visitas): "))
    plan_simple = int(input("Cantidad Plan Simple: "))
    buyback = int(input("Cantidad Buyback: "))
    seguros = int(input("Seguros vendidos: "))
    powerpay = int(input("Cantidad PowerPay: "))
    yape = int(input("Ventas con Yape: "))
    
    # Cálculos
    venta_con_igv = venta_sin_igv * (1 + IGV)
    cumplimiento_meta = (venta_sin_igv / META_MENSUAL) * 100
    attach_rate = (accesorios_sin_igv / venta_sin_igv) * 100 if venta_sin_igv > 0 else 0
    tasa_conversion = (transacciones / trafico) * 100 if trafico > 0 else 0
    
    # Resultados
    print("\n=== Tienda Arequipa ===")
    print(f"Venta Total sin IGV: S/. {venta_sin_igv:,.2f}")
    print(f"Venta Total con IGV: S/. {venta_con_igv:,.2f}")
    print(f"Cumplimiento Meta Mensual: {cumplimiento_meta:.2f}%")
    print(f"Attach Rate: {attach_rate:.2f}%")
    print(f"iPhone: {iphones}")
    print(f"Mac: {macs}")
    print(f"iPad: {ipads}")
    print(f"Watch: {watch}")
    print(f"AirPods: {airpods}")
    print(f"Tasa de conversión del día: {tasa_conversion:.2f}%")
    print(f"Plan Simple: {plan_simple}")
    print(f"Buyback: {buyback}")
    print(f"Seguros vendidos: {seguros}")
    print(f"PowerPay: {powerpay}")
    print(f"Ventas con Yape: {yape}")
    
# Ejecutar
reporte_tienda()
