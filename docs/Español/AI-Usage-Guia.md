# Guia de AI Usage

Esta guia es para usuarios nuevos. Te ayuda a configurar `AI Usage` desde cero para que el dispositivo muestre el uso de Claude o Codex.

## 1. Antes de empezar

Comprueba esto primero:

1. El dispositivo esta encendido.
2. El dispositivo y tu ordenador estan en la misma red local.
3. Puedes abrir la pagina `settings.html`.
4. Conoces la IP del dispositivo.
5. Python 3 esta instalado.

Comprobar Python:

```bash
python3 --version
```

En Windows tambien puedes usar:

```bash
py --version
```

## 2. Como funciona AI Usage

`AI Usage` muestra en el dispositivo los datos de uso de AI que estan en tu ordenador.

Fuentes compatibles:

1. Claude
2. Codex

Debes ejecutar un script Python en tu ordenador:

1. El script lee datos locales.
2. El script envia datos al dispositivo por HTTP.
3. El dispositivo actualiza la app `AI Usage`.

Claude y Codex usan este mismo endpoint:

```text
/api/claude_usage
```

## 3. Configurar Claude

### Paso 1

Abre `AI Usage` en el dispositivo.

### Paso 2

Descarga:

```text
claude_usage.py
```

Descarga directa:

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/claude_usage.py>

### Paso 3

Ejecuta:

```bash
python3 claude_usage.py 192.168.1.123
```

Cambia `192.168.1.123` por la IP real del dispositivo.

En Windows:

```bash
py claude_usage.py 192.168.1.123
```

### Paso 4

Deja el script en ejecucion y mantén el dispositivo en la pagina `AI Usage`.

## 4. Configurar Codex

### Paso 1

Abre `AI Usage` en el dispositivo.

### Paso 2

Descarga:

```text
codex_usage.py
```

Descarga directa:

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/codex_usage.py>

### Paso 3

Ejecuta:

```bash
python3 codex_usage.py 192.168.1.123
```

Windows:

```bash
py codex_usage.py 192.168.1.123
```

### Paso 4

Comprueba que existen datos de sesion de Codex.

Ruta comun:

```text
~/.codex/sessions
```

En Windows normalmente:

```text
C:\Users\TuNombre\.codex\sessions
```

Si no existe ninguna sesion, usa Codex una vez primero.

## 5. Problemas comunes

### El dispositivo no se actualiza

Revisa:

1. IP correcta
2. Misma red local
3. El dispositivo sigue en `AI Usage`
4. El script sigue activo
5. Existen datos locales de Claude o Codex

### Error de red

Normalmente significa:

1. IP incorrecta
2. Dispositivo sin conexion
3. Red diferente
4. Aislamiento del router
