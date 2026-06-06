# AI Usage Anleitung

Diese Anleitung ist fur neue Nutzer. Sie hilft dir, `AI Usage` von Anfang an einzurichten, damit das Geraet die Nutzung von Claude oder Codex anzeigen kann.

## 1. Vor dem Start

Bitte zuerst pruefen:

1. Das Geraet ist eingeschaltet.
2. Das Geraet und dein Computer sind im selben lokalen Netzwerk.
3. Du kannst `ii.html` im Browser oeffnen.
4. Du kennst die IP des Geraets.
5. Python 3 ist installiert.

Python pruefen:

```bash
python3 --version
```

Unter Windows auch:

```bash
py --version
```

## 2. Wie AI Usage funktioniert

`AI Usage` zeigt lokale AI-Nutzungsdaten auf dem Geraet an.

Unterstuetzte Quellen:

1. Claude
2. Codex

Du startest ein Python-Skript auf deinem Computer:

1. Das Skript liest lokale Daten.
2. Das Skript sendet die Daten per HTTP an das Geraet.
3. Das Geraet aktualisiert die App `AI Usage`.

Claude und Codex nutzen denselben Endpoint:

```text
/api/claude_usage
```

## 3. Claude einrichten

### Schritt 1

Oeffne `AI Usage` auf dem Geraet.

### Schritt 2

Lade herunter:

```text
claude_usage.py
```

### Schritt 3

Starte:

```bash
python3 claude_usage.py 192.168.1.123
```

Ersetze `192.168.1.123` durch die echte IP des Geraets.

Windows:

```bash
py claude_usage.py 192.168.1.123
```

### Schritt 4

Lass das Skript weiterlaufen und halte das Geraet auf der Seite `AI Usage`.

## 4. Codex einrichten

### Schritt 1

Oeffne `AI Usage` auf dem Geraet.

### Schritt 2

Lade herunter:

```text
codex_usage.py
```

### Schritt 3

Starte:

```bash
python3 codex_usage.py 192.168.1.123
```

Windows:

```bash
py codex_usage.py 192.168.1.123
```

### Schritt 4

Pruefe, ob lokale Codex-Sessiondaten vorhanden sind.

Typischer Pfad:

```text
~/.codex/sessions
```

Unter Windows meist:

```text
C:\Users\DeinName\.codex\sessions
```

Wenn noch keine Session existiert, benutze Codex zuerst einmal.

## 5. Haeufige Probleme

### Keine Aktualisierung auf dem Geraet

Bitte pruefen:

1. Richtige IP
2. Gleiches Netzwerk
3. Geraet ist noch auf `AI Usage`
4. Skript laeuft noch
5. Lokale Daten von Claude oder Codex sind vorhanden

### Netzwerkfehler

Meist bedeutet das:

1. Falsche IP
2. Geraet offline
3. Anderes Netzwerk
4. Router-Isolation
