# printDCC

printDCC es una aplicación que permite la conexión al servidor anakena.dcc.uchile.cl y el envío de archivos para impresión.

## Requisitos
    - Python 3.x
    - paramiko (para la conexión SSH)

Para instalar las dependencias, puedes ejecutar:

```bash
pip install -r requirements.txt
```

## Funcionalidades

- **Iniciar sesión**: Ingresa el nombre de usuario y la contraseña del servidor SSH y presiona “Iniciar sesión”. Si las credenciales son correctas, accederás a la pantalla de configuración de impresión.

- **Configurar la impresión**:
    - Selecciona la impresora de destino.
    - Elige un archivo PDF local para subir y especifica un nombre de archivo de salida en formato PostScript
    - Define el número de copias y selecciona si deseas imprimir a doble cara.  

- **Enviar a imprimir**: Al presionar “Imprimir”, el archivo se convierte automáticamente a formato PS y se envía al servidor para la impresión.

- **Cerrar sesión**: Usa el botón "Cerrar Sesión" para desconectarte del servidor SSH de manera segura.

## Créditos

Desarrollado por @cstammp 
Versión: 1.0  
Licencia: MIT License © 2024