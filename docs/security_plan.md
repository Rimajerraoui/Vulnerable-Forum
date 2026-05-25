# Security Plan

## SQL Injection (Login)
Ziel: Login ohne Passwort umgehen  
Beispiel: ' OR 1=1 --

## XSS (Posts)
Ziel: Script im Forum ausführen  
Beispiel: <script>alert("XSS")</script>

## XSS (Search)
Ziel: Script über Suchfeld

## IDOR (Profile)
Ziel: Zugriff auf andere Accounts  
Beispiel: /profile?id=2

## Broken Authentication
Ziel: Login umgehen oder Session missbrauchen

## Path Traversal
Ziel: Dateien lesen  
Beispiel: ../../etc/passwd

## Schwache Passwörter
Ziel: leicht erraten

## CSRF
Ziel: Aktionen ohne Zustimmung ausführen