; size_t safe_strcpy(char *dst, size_t dst_size, const char *src);
; Kopiert die Zeichenkette von src nach dst, aber maximal dst_size-1 Nutzbytes,
; damit immer Platz fuer den Nullterminator bleibt. Wenn dst_size 0 ist, wird
;   rdi = dst
;   rsi = dst_size
;   rdx = src
;   Rueckgabe in rax = Anzahl kopierter Bytes (ohne Nullterminator)
section .text
global safe_strcpy

safe_strcpy:
    push rbp                  ;
    mov  rbp, rsp

                               ; Sonderfall: dst_size == 0 -> kein Platz zum Schreiben 
    test rsi, rsi              ; pruefe ob dst_size == 0
    jz   .no_space             ; falls ja: nichts schreiben, 0 zurueckgeaben

                               ; Register fuer die Kopierschleife vorbereiten 
    xor  rcx, rcx              ; rcx = Schleifenzaehler / Index, beginnt bei 0
    dec  rsi                   ; rsi = dst_size - 1 (max. erlaubte Nutzbytes,
                               ; 1 Byte bleibt fuer den Nullterminator)
.copy_loop:
    cmp  rcx, rsi               ; haben wir schon dst_size-1 Bytes kopiert?
    jge  .terminate              ; falls rcx >= dst_size-1 -> break, Terminator setzen

    mov  al, [rdx + rcx]        ; al = src[rcx]  
    test al, al                  ; ist es der Nullterminator von src?
    jz   .terminate               ; falls ja: src ist zu Ende, Schleife beenden

    mov  [rdi + rcx], al        ; dst[rcx] = al  (Zeichen kopieren)
    inc  rcx                     ; Index um 1 erhoehen
    jmp  .copy_loop              ; naechstes Zeichen

.terminate:
    mov  byte [rdi + rcx], 0     ; dst[rcx] = '\0' -> garantierte Nullterminierung,
                                  ; auch wenn src laenger als dst_size war
    mov  rax, rcx                ; Rueckgabewert = Anzahl kopierter Bytes (ohne '\0')
    jmp  .done

.no_space:
    xor  rax, rax                ; dst_size war 0 -> 0 Bytes kopiert, nichts geschrieben

.done:
    pop  rbp                     ; zurueckgeben
    ret