# VulnForum – Vulnerable Web Application

Eine absichtlich unsichere Webanwendung für IT-Sicherheit Schulungszwecke.

---

## Projektbeschreibung

VulnForum ist ein Forum mit **8 absichtlich eingebauten Sicherheitslücken** aus den OWASP Top 10.
Ziel ist es, reale Angriffe zu demonstrieren und automatisiert auszunutzen.

---

## Technologien

| Technologie | Verwendung |
|---|---|
| Python + Flask | Backend |
| SQLite | Datenbank |
| HTML + CSS | Frontend |
| Python requests | Exploit-Skript |

---

## Installation

**1. Repository klonen:**
```bash
git clone https://github.com/Rimajerraoui/Vulnerable-Forum.git
cd Vulnerable-Forum
```

**2. Bibliotheken installieren:**
```bash
pip install -r requirements.txt
```

**3. App starten:**
```bash
python app.py
```

**4. Browser öffnen:**
```
http://127.0.0.1:5000
```

---

## Sicherheitslücken

| Nr. | Lücke | Route |
|---|---|---|
| 1 | SQL Injection | `/login` |
| 2 | Blind SQL Injection | `/usercheck` |
| 3 | Broken Authentication | `/register` |
| 4 | Schwacher Secret Key | `app.py` |
| 5 | Stored XSS | `/forum` |
| 6 | Reflected XSS | `/search` |
| 7 | IDOR | `/post/<id>` |
| 8 | Path Traversal | `/files/` |

---

## Exploit-Skript starten

```bash
cd exploit
python exploit.py
```

---

## Rollenaufteilung

| Person | Aufgabe |
|---|---|
| Person 1 | Backend (Flask, Datenbank, Sicherheitslücken) |
| Person 2 | Frontend (HTML, CSS, Design) |
| Person 3 | Security & Testing (Exploit-Skript, Dokumentation) |

---

## Wichtig

> Diese Anwendung ist **absichtlich unsicher** und darf nur in einer kontrollierten Umgebung verwendet werden!

---

*Projekt entwickelt im Rahmen des IT-Sicherheitskurses*
