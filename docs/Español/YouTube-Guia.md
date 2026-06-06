# Guia de YouTube

Esta guia ayuda a usuarios nuevos a configurar la app `YouTube` desde cero.

## 1. Que muestra la app

La app muestra datos publicos del canal:

1. Titulo del canal
2. Avatar
3. Numero de suscriptores
4. Vistas totales
5. Videos totales

Solo usa datos publicos. No inicia sesion en tu cuenta.

## 2. Lo que necesitas

Prepara estas dos cosas:

1. `Channel Ref`
2. Una clave de `YouTube Data API v3`

Tambien confirma:

1. El dispositivo esta en linea
2. Puedes abrir `settings.html`

## 3. Que es Channel Ref

El dispositivo acepta:

1. Channel ID
2. `@handle`
3. username

Ejemplos:

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

La mejor opcion es:

1. Channel ID que empieza por `UC...`
2. `@handle`

## 4. Como conseguir la API Key

En Google Cloud Console:

1. Inicia sesion
2. Crea o elige un proyecto
3. Activa `YouTube Data API v3`
4. Crea una API key
5. Copia la clave

Enlaces utiles:

1. Crear API key: <https://console.cloud.google.com/apis/credentials>
2. Guia oficial: <https://developers.google.com/youtube/registering_an_application>

## 5. Configurar la pagina del dispositivo

En la pagina `YouTube`, rellena:

### Channel Ref

Ejemplo:

```text
@yourhandle
```

o

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

Pega tu clave de YouTube Data API v3.

### Refresh Interval

Valor recomendado:

```text
60
```

## 6. Guardar y probar

Orden recomendado:

1. Haz clic en `Open This App`
2. Rellena `Channel Ref`
3. Rellena `API Key`
4. Haz clic en `Save YouTube`
5. Haz clic en `Reload YouTube`

## 7. Comportamiento de cache

Ahora la app soporta cache.

Eso significa:

1. Si antes hubo datos correctos
2. La app puede mostrar primero la cache
3. Luego actualiza en segundo plano

Estados comunes:

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

## 8. Problemas comunes

### `Set channel and API key`

La configuracion no esta completa.

### `Wi-Fi offline`

El dispositivo no tiene red.

### `HTTP xxx`

Suele significar:

1. API key no valida
2. API no activada
3. Problema de cuota
4. Referencia de canal incorrecta
