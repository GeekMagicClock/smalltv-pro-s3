# YouTube Anleitung

Diese Anleitung hilft neuen Nutzern, die `YouTube` App von Anfang an einzurichten.

## 1. Was die App anzeigt

Die App zeigt oeffentliche Kanaldaten:

1. Kanalname
2. Avatar
3. Abonnenten
4. Gesamtaufrufe
5. Gesamtzahl der Videos

Die App nutzt nur oeffentliche Daten. Sie meldet sich nicht bei deinem YouTube-Konto an.

## 2. Was du brauchst

Du brauchst:

1. `Channel Ref`
2. Einen `YouTube Data API v3` Key

Bitte auch pruefen:

1. Das Geraet ist online
2. `ii.html` laesst sich oeffnen

## 3. Was ist Channel Ref

Das Geraet unterstuetzt:

1. Channel ID
2. `@handle`
3. username

Beispiele:

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

Am besten verwenden:

1. `UC...` Channel ID
2. `@handle`

## 4. So bekommst du einen API Key

In der Google Cloud Console:

1. Anmelden
2. Projekt erstellen oder auswaehlen
3. `YouTube Data API v3` aktivieren
4. API Key erstellen
5. Key kopieren

## 5. Im Geraet konfigurieren

Auf der Seite `YouTube` ausfuellen:

### Channel Ref

Zum Beispiel:

```text
@yourhandle
```

oder

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

Deinen YouTube Data API v3 Key einfuegen.

### Refresh Interval

Empfohlener Standardwert:

```text
60
```

## 6. Speichern und testen

Empfohlene Reihenfolge:

1. `Open This App` klicken
2. `Channel Ref` eintragen
3. `API Key` eintragen
4. `Save YouTube` klicken
5. `Reload YouTube` klicken

## 7. Cache-Verhalten

Die App unterstuetzt jetzt Cache.

Das bedeutet:

1. Wenn frueher schon Daten geladen wurden
2. Kann die App zuerst Cache zeigen
3. Danach aktualisiert sie im Hintergrund

Haeufige Statusanzeigen:

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

## 8. Haeufige Probleme

### `Set channel and API key`

Die Konfiguration ist nicht vollstaendig.

### `Wi-Fi offline`

Das Geraet ist nicht online.

### `HTTP xxx`

Das bedeutet meistens:

1. API Key ist ungueltig
2. API ist nicht aktiviert
3. Quota-Problem
4. Falscher Channel Ref
