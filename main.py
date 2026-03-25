import sqlite3


# 🔌 Conexión a la base de datos
def conectar():
    return sqlite3.connect("inventario.db")


# 🧱 Crear tabla
def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        cantidad INTEGER,
        precio INTEGER
    )
    """)

    conexion.commit()
    conexion.close()


# 📋 Menú
def mostrar_menu():
    print("\n📦 SISTEMA DE INVENTARIO")
    print("1. Agregar producto")
    print("2. Ver productos")
    print("3. Editar producto")
    print("4. Eliminar producto")
    print("5. Salir")


# ➕ Agregar producto
def agregar_producto():
    try:
        nombre = input("Nombre del producto: ")

        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return

        cantidad = int(input("Cantidad: "))
        if cantidad <= 0:
            print("❌ La cantidad debe ser mayor a 0")
            return

        precio = int(input("Precio: "))
        if precio <= 0:
            print("❌ El precio debe ser mayor a 0")
            return

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO productos (nombre, cantidad, precio)
        VALUES (?, ?, ?)
        """, (nombre, cantidad, precio))

        conexion.commit()
        conexion.close()

        print("✅ Producto agregado correctamente")

    except ValueError:
        print("❌ Cantidad y precio deben ser números válidos")

    except sqlite3.IntegrityError:
        print("❌ Este producto ya existe")


# 📖 Ver productos
def ver_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre, cantidad, precio FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    if len(productos) == 0:
        print("🛒 No hay productos aún")
    else:
        print("\n📋 ===== LISTA DE PRODUCTOS =====")
        for p in productos:
            print(f"📦 {p[0]:<15} | Cant: {p[1]:<5} | 💲 {p[2]:,}")


# ✏️ Editar producto
def editar_producto():
    nombre = input("Nombre del producto a editar: ")

    try:
        nueva_cantidad = int(input("Nueva cantidad: "))
        nuevo_precio = int(input("Nuevo precio: "))

        if nueva_cantidad <= 0 or nuevo_precio <= 0:
            print("❌ Valores deben ser mayores a 0")
            return

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE productos
        SET cantidad = ?, precio = ?
        WHERE nombre = ?
        """, (nueva_cantidad, nuevo_precio, nombre))

        if cursor.rowcount == 0:
            print("❌ Producto no encontrado")
        else:
            print("✏️ Producto actualizado correctamente")

        conexion.commit()
        conexion.close()

    except ValueError:
        print("❌ Debes ingresar números válidos")


# 🗑️ Eliminar producto
def eliminar_producto():
    nombre = input("Nombre del producto a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))

    if cursor.rowcount == 0:
        print("❌ Producto no encontrado")
    else:
        print("🗑️ Producto eliminado correctamente")

    conexion.commit()
    conexion.close()


# 🚀 Programa principal
def main():
    crear_tabla()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto()
        
        elif opcion == "2":
            ver_productos()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "3":
            editar_producto()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "4":
            eliminar_producto()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()