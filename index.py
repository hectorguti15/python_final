import random


def RegistrarProducto(tipo,numeroProducto):
    print(f"Producto {numeroProducto + 1}")
    descripcion = input("Descripción del producto: ")
    importado = input("Importado: ")
    codigoInventario = random.randint(2860, 12857) * 7
    costoAlmacenamiento = None
    funda = None
    if tipo == "Laptops":
        costoAlmacenamiento = random.randrange(200, 451, 2)
        funda = random.randint(80, 150)
    elif tipo == "Desktops":
        costoAlmacenamiento = random.randint(60, 83) * 3
        funda = random.randint(150, 250)
    elif tipo == "Impresoras":
        costoAlmacenamiento  = random.randrange(91, 156, 2)
    return descripcion, importado, codigoInventario, costoAlmacenamiento, funda

def RegistrarVentas():
    tipo = input("¿De que producto electronico desea hacer su venta?: ")
    try: 
        productosDic = {}
        with open(f"data_{tipo}.txt","r+") as document:
            productosDocument = document.readlines()           
            if productosDocument:     
                for producto in productosDocument:
                    producto = producto.rstrip("\n").split(",")
                    modelo = producto[0].strip()
                    descripcion = producto[1].strip()
                    importado = producto[2].strip()
                    codigoInventario = producto[3].strip()
                    costoAlmacenamiento = producto[4].strip()
                    funda = producto[5].strip()
                    productosDic[modelo] = {
                    "Descripcion": descripcion,
                    "Importado": importado,
                    "Codigo de Inventario": codigoInventario,
                    "Costo de Almacenamiento": costoAlmacenamiento,
                    "Funda": funda
                    }
                    print(f"---{producto[0]}---")
                    print(f"Descripcion: {producto[1]}")
                    print(f"Importado: {producto[2]}")
                    print(f"Codigo de Inventario: {producto[3]}")
                    print(f"Costo de Almacenamiento: {producto[4]}")
                    print(f"Funda: {producto[5]}")

                cantidadModelosAdquirir = int(input("¿Cuantos modelos va a adquirir?: "))
                if cantidadModelosAdquirir <= len(productosDic):
                    for i in range(cantidadModelosAdquirir):
                        modelo = input("Elija un modelo: ")
                        with open("data_ventas.txt","a+") as ventas:
                            precioVenta = (int(productosDic[modelo]["Costo de Almacenamiento"]) * 0.25) + int(productosDic[modelo]["Costo de Almacenamiento"])    
                            ventas.seek(0)
                            contenido = ventas.read()
                            ultimaVenta = contenido.rfind("Ventas")
                            if ultimaVenta != -1:
                                numeroStr = contenido[ultimaVenta:].split()[1]
                                numeroVenta = int(numeroStr.replace(',', ''))
                                numeroVenta = numeroVenta + 1
                            else:
                                numeroVenta = 2000

                            cantidad = int(input(f"Ingrese la cantidad a adquirir del {modelo}: ")) 
                            nombre = productosDic[modelo]["Descripcion"]
                            precioFinal = precioVenta * cantidad 
                            ventas.write(f"Ventas {numeroVenta}, {nombre}, {precioVenta}, {cantidad}, {precioFinal}\n")      
                            print("Producto comprado con exito")
                else:
                    print("Cantidad de modelos insuficientes")
            else:
                print("No se encontraron productos")

    except:
        print("Error en el archivo")

def LeerVentas(lista,ventas):
    contenido = ventas.readlines()
    if not contenido:
        print("Aun no se ha registrado ninguna venta")
        exit()
    for venta in contenido:
        infoVenta = venta.split(",")
        numeroVenta  = infoVenta[0].strip()
        descripcion = infoVenta[1].strip()
        precioVenta = infoVenta[2].strip()
        cantidad = infoVenta[3].strip()
        precioFinal = infoVenta[4].strip()
        print(f"---{numeroVenta}---")
        print(f"Descripcion: {descripcion}")
        print(f"Precio de venta: {precioVenta}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio final: {precioFinal}")

        venta = {int(numeroVenta.split()[1]): {'Descripcion': descripcion, 'Precio de Venta': precioVenta, 'Cantidad': int(cantidad), 'Precio final': precioFinal}}
        lista.append(venta)

def ModificarCantidadVenta():
    try: 
        with open("data_ventas.txt","r") as ventas:
            ventasArray = []
            LeerVentas(ventasArray,ventas)
            ventasArray = quickSort(ventasArray)
            numeroVenta = int(input("Ingrese el numero de venta que desea realizar el cambio: "))
            encontradoNumeroVenta = busquedaBinaria(ventasArray,numeroVenta)
            if encontradoNumeroVenta != -1:
                cantidadNueva = int(input("Ingresar la nueva cantidad: "))
                ventasArray[encontradoNumeroVenta][numeroVenta]['Cantidad'] = cantidadNueva
                ventasArray[encontradoNumeroVenta][numeroVenta]['Precio final'] = int(ventasArray[encontradoNumeroVenta][numeroVenta]['Cantidad']) * float(ventasArray[encontradoNumeroVenta][numeroVenta]['Precio de Venta'])
                
                with open("data_ventas.txt", "w") as ventas:
                    for ventasDic in ventasArray:
                        numeroVentaW = list(ventasDic.keys())[0]
                        descripcionW = ventasDic[numeroVentaW]['Descripcion']
                        precioVentaW = ventasDic[numeroVentaW]['Precio de Venta']
                        cantidadW = ventasDic[numeroVentaW]['Cantidad']
                        ventaFinalW = ventasDic[numeroVentaW]['Precio final']
                        ventas.write(f"Ventas {numeroVentaW}, {descripcionW}, {precioVentaW}, {cantidadW}, {ventaFinalW}\n")
                print("Producto cambiado exitosamente")
            else:
                print("No existe ese numero de venta")
                exit()
    except:
        print("Error en el archivo")


def busquedaBinaria(lista, elemento):
    lista = quickSort(lista)
    print(lista)
    pos = -1
    izq = 0
    der = len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        clave = list(lista[medio].keys())[0] 
        if elemento == clave:
            pos = medio
            break
        else:
            if elemento < clave:
                der = medio - 1
            else:
                izq = medio + 1
    return pos


def quickSort(lista):
    izquierda = []
    centro = []
    derecha = []
    if len(lista) > 1:
        pivote = list(lista[0].keys())[0] 
        for i in lista:
            clave = list(i.keys())[0]
            if clave  < pivote:
                izquierda.append(i)
            elif clave  == pivote:
                centro.append(i)
            elif clave > pivote:
                derecha.append(i)
        return quickSort(izquierda)+centro+quickSort(derecha)
    else:
      return lista


def ordenamientoBurbuja(lista):
    n = len(lista)

    for i in range(n-1):
        for j in range(n-1-i):
            if float(list(lista[j].values())[0]['Precio final']) > float(list(lista[j+1].values())[0]['Precio final']):
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista


def buscarVenta():
    try:
        with open("data_ventas.txt","r") as ventas:
            ventasArray = []
            LeerVentas(ventasArray,ventas)
            numeroVenta = int(input("Ingresa el numero de venta que estas buscando: "))
            for ventasDic in ventasArray:
                if list(ventasDic.keys())[0] == numeroVenta:
                    print("---VENTA ENCONTRADA---")
                    print(f"Descripcion: {ventasDic[numeroVenta]['Descripcion']}")
                    print(f"Precio de Venta: {ventasDic[numeroVenta]['Precio de Venta']}")
                    print(f"Cantidad: {ventasDic[numeroVenta]['Cantidad']}")
                    print(f"Precio final: {ventasDic[numeroVenta]['Precio final']}")
                    break
    except:
       print("Error en el archivo")

def MostrarVentaTotalAlto():
    with open("data_ventas.txt","r") as ventas:
            ventasArray = []
            LeerVentas(ventasArray,ventas)
            ventasArray = ordenamientoBurbuja(ventasArray)
            ultimoIndice = len(ventasArray) - 1
            ventaAlto = list(ventasArray[ultimoIndice].values())[0]
            print("---VENTA MAS ALTA---")
            print(f"Descripcion: {ventaAlto['Descripcion']}")
            print(f"Precio de Venta: {ventaAlto['Precio de Venta']}")
            print(f"Cantidad: {ventaAlto['Cantidad']}")
            print(f"Precio final: {ventaAlto['Precio final']}")

def main():
    print("<---------MENÚ------->")
    print("1. Ingresar un producto")
    print("2. Registrar venta")
    print("3. Modificar cantidad de una venta")
    print("4. Buscar venta por el número de venta") 
    print("5. Mostrar venta con el total más alto")
    print("6. Salir")
    opcion = int(input("Seleccione una opción: "))


    while opcion != 6:
        if opcion == 1:
            try:
                tipo = input("¿Que tipo de producto se esta registrando?: ")
                registros = int(input(f"¿Cuantas productos vas a registrar del tipo {tipo}?: "))
                for i in range(registros):
                    producto = RegistrarProducto(tipo,i)
                    with open(f"data_{tipo}.txt","a+") as document:
                        document.seek(0)
                        contenido = document.readlines()
                        modelosRegistrados = len(contenido)
                        if modelosRegistrados > 0:
                            ultimaLinea = contenido[-1]
                            ultimoModelo = int(ultimaLinea.split(",")[0].split()[-1]) + 1
                        else:
                            ultimoModelo = 1
                        document.write(f"Modelo {ultimoModelo}, {producto[0]}, {producto[1]}, {producto[2]}, {producto[3]}, {producto[4]}\n")
                        print("Producto registrado exitosamente")
            except:
                print("No se pudo registrar correctamente el producto")
        elif opcion == 2:
                RegistrarVentas()
        elif opcion == 3:
            ModificarCantidadVenta()
        elif opcion == 4:
            buscarVenta()
        elif opcion == 5:
            MostrarVentaTotalAlto()
        print("<---------MENÚ------->")
        print("1. Ingresar un producto")
        print("2. Registrar venta")
        print("3. Modificar cantidad de una venta")
        print("4. Buscar venta por el número de venta") 
        print("5. Mostrar venta con el total más alto")
        print("6. Salir")
        opcion = int(input("Seleccione una opción: "))
main()



