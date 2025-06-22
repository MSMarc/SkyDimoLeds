# ✨ SkyDimo LED Controller (Adalight)

Permite controlar las luces LED de **SkyDimo** directamente desde Python, **sin necesidad de instalar el software del fabricante**.
Ideal para quienes buscan una forma rápida y ligera de **encender automáticamente sus LEDs al iniciar el PC**, usando un simple servicio de Windows.

## 🧩 Características

- ✅ Compatible con dispositivos Adalight/SkyDimo
- 🎨 Ilumina todos los LEDs en color blanco (editable)
- 🖥️ Se puede instalar como servicio de Windows
- 💡 Ideal para Ambilight básico o iluminación constante

## ⚙️ Requisitos

- Python 3.6+
- Dispositivo SkyDimo (o compatible con Adalight)
- Puerto COM identificado (Administrador de dispositivos)

## 🛠 Instalación

1. Clona este repositorio o descarga el código.
   ```bash
   git clone https://github.com/tuusuario/skydimo-controller.git
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
3. Cambia el NUM_LEDS y el PORT según tu dispositivo.
4. Crea el .exe
   ```bash
   pyinstaller --onefile main.py
5. Crea el servicio
   ```bash
   sc.exe create Skydimo binPath= "C:\ruta\completa\a\dist\skydimo.exe" start= auto
6. Ejecuta el servicio
   ```bash
   sc.exe start Skydimo
