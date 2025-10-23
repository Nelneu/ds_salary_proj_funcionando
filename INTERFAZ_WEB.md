# 🌐 Interfaz Web - Predictor de Salarios

## 🚀 Inicio Rápido

### 1. Iniciar el servidor

```bash
cd /home/user/ds_salary_proj
python3 app/main.py
```

### 2. Abrir en el navegador

Abre tu navegador web y visita:

```
http://localhost:5000
```

o desde la red local:

```
http://TU_IP:5000
```

### 3. Usar la interfaz

1. **Años de Experiencia**: Ingresa un número entre 0 y 15 (puede tener decimales, ej: 5.5)
2. **Nivel de Educación**: Selecciona del menú desplegable:
   - Bachelor's (Licenciatura)
   - Master's (Maestría)
   - PhD (Doctorado)
3. Haz clic en **"CALCULAR SALARIO"**
4. ¡Verás la predicción en pantalla!

## ✨ Características

✅ **Interfaz moderna y responsiva** - Se adapta a cualquier dispositivo
✅ **Validación de datos** - Solo acepta valores válidos
✅ **Menú desplegable** - Evita errores en nivel de educación
✅ **Resultados instantáneos** - Predicción en tiempo real
✅ **Animaciones suaves** - Experiencia de usuario agradable

## 📱 Capturas de pantalla

La interfaz incluye:
- 💰 Icono de dinero
- Formulario intuitivo con validación
- Menú desplegable para educación
- Botón grande y llamativo
- Resultado con formato de moneda ($XX,XXX)
- Mensajes de error amigables

## 🔧 Detener el servidor

Para detener el servidor presiona:

```
Ctrl + C
```

en la terminal donde está corriendo.

## 🌐 Acceso desde otros dispositivos

Si quieres que otros en tu red local accedan:

1. Encuentra tu IP local:
   ```bash
   ip addr show | grep "inet " | grep -v 127.0.0.1
   ```

2. Comparte la URL: `http://TU_IP:5000`

## 📊 Ejemplos de uso

**Ejemplo 1: Recién graduado**
- Años de experiencia: `1.0`
- Nivel de educación: `Bachelor's`
- Resultado esperado: ~$40,000

**Ejemplo 2: Profesional con experiencia**
- Años de experiencia: `5.5`
- Nivel de educación: `Master's`
- Resultado esperado: ~$72,000

**Ejemplo 3: Experto senior**
- Años de experiencia: `10.0`
- Nivel de educación: `PhD`
- Resultado esperado: ~$121,000

## ⚠️ Notas importantes

- El servidor debe estar corriendo para usar la interfaz
- Las predicciones son más precisas para 1-10 años de experiencia
- El modelo fue entrenado con datos históricos reales
- Esta es una interfaz de desarrollo (no usar en producción directamente)

## 🎨 Personalización

Si quieres modificar los estilos, edita:
```
app/templates/index.html
```

Los estilos CSS están incluidos dentro del mismo archivo HTML.

---

**¡Disfruta de tu predictor de salarios!** 💰✨
