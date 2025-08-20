def reporte_tienda():
    IGV = 0.18
    META_MENSUAL = 1_000_000  # sin IGV
    
    print("=== Reporte Tienda Arequipa ===")
    
    # Ingreso de datos
    venta_con_igv = float(input("Venta Total con IGV (S/.): ") or 0)
    venta_con_igv_mes = float(input("Venta Total del mes con IGV (S/.): ") or 0)
    accesorios_con_igv = float(input("Monto de accesorios vendidos con IGV (S/.): ") or 0)
    iphones = int(input("Cantidad iPhone vendidos: ") or 0)
    macs = int(input("Cantidad Mac vendidos: ") or 0)
    ipads = int(input("Cantidad iPad vendidos: ") or 0)
    watch = int(input("Cantidad Watch vendidos: ") or 0)
    airpods = int(input("Cantidad AirPods vendidos: ") or 0)
    transacciones = int(input("Cantidad de transacciones: ") or 0)
    trafico = int(input("Tráfico del día (visitas): ") or 0)
    plan_simple = int(input("Cantidad Plan Simple: ") or 0)
    buyback = int(input("Cantidad Buyback: ") or 0)
    seguros = int(input("Seguros vendidos: ") or 0)
    powerpay = int(input("Cantidad PowerPay: ") or 0)
    yape = int(input("Ventas con Yape: ") or 0)

    
    # Cálculos
    venta_sin_igv = venta_con_igv / (1 + IGV)
    venta_sin_igv_mes = venta_con_igv_mes / (1 + IGV)
    accesorios_sin_igv = accesorios_con_igv / (1 + IGV)
    cumplimiento_meta = (venta_sin_igv_mes / META_MENSUAL) * 100 if META_MENSUAL > 0 else 0
    attach_rate = (accesorios_sin_igv / venta_sin_igv) * 100 if venta_sin_igv > 0 else 0
    tasa_conversion = (transacciones / trafico) * 100 if trafico > 0 else 0
    
    # Resultados
    print("\n")  # Salto de línea antes de empezar
    print("\nReporte Tienda Arequipa ")
    print(f"Venta Total sin IGV: S/. {venta_sin_igv:,.2f}")
    print(f"Cumplimiento Meta Mensual: {cumplimiento_meta:.2f}%")
    print(f"Attach: {attach_rate:.2f}%")
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

