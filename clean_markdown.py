#!/usr/bin/env python3
"""
Script per pulire i file Markdown:
- Rimuove spazi a inizio riga
- Rende vuote le linee composte solo da spazi/tab
- Fa trim delle righe (rimuove spazi in fondo)
- Rimuove caratteri invisibili e speciali
- Normalizza gli a capo con \r\n (CRLF)
- Forza encoding UTF-8
"""

import os
import glob
import re
import unicodedata

def remove_invisible_chars(text):
    """Rimuove caratteri invisibili e speciali dal testo"""
    # Rimuovi caratteri di controllo Unicode (eccetto tab, newline, carriage return)
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\t\n\r')
    
    # Rimuovi spazi non-breaking e altri spazi Unicode speciali
    text = re.sub(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]', ' ', text)
    
    # Rimuovi zero-width characters
    text = re.sub(r'[\u200B-\u200D\u2060\uFEFF]', '', text)
    
    # Normalizza caratteri tipografici
    # Converti apostrofi curvi in apostrofi dritti
    text = re.sub(r'[’]', "'", text)
    
    # Converti virgolette curve in virgolette dritte
    text = re.sub(r'[“”]', '"', text)
    
    # Converti lineette lunghe in trattini normali
    text = re.sub(r'[–]', '-', text)
    
    # Normalizza Unicode (NFD -> NFC)
    text = unicodedata.normalize('NFC', text)
    
    return text

def clean_markdown_file(filepath):
    """Pulisce un singolo file markdown"""
    try:
        # Leggi il file con encoding UTF-8 esplicito
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Rimuovi caratteri invisibili dal contenuto completo
        content = remove_invisible_chars(content)
        
        # Dividi in righe
        lines = content.splitlines()
        
        cleaned_lines = []
        for line in lines:
            # Se la linea contiene solo spazi o tab, rendila vuota
            if line.strip() == '':
                cleaned_lines.append('')
            else:
                # Rimuovi spazi a inizio riga e fai trim della fine
                cleaned_line = line.lstrip(' \t').rstrip()
                cleaned_lines.append(cleaned_line)
        
        # Scrivi il file con terminatori CRLF e encoding UTF-8
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            for i, line in enumerate(cleaned_lines):
                if i < len(cleaned_lines) - 1:
                    f.write(line + '\r\n')
                else:
                    # Ultima riga con newline finale
                    f.write(line + '\r\n')
        
        print(f"✓ Pulito: {filepath}")
        
    except Exception as e:
        print(f"✗ Errore nel processare {filepath}: {e}")

def main():
    """Funzione principale"""
    # Trova tutti i file .md nella directory corrente
    md_files = glob.glob('*.md')
    
    if not md_files:
        print("Nessun file .md trovato nella directory corrente")
        return
    
    print(f"Trovati {len(md_files)} file .md da processare:")
    for file in md_files:
        print(f"  - {file}")
    
    print("\nInizio pulizia...")
    print("- Rimozione caratteri invisibili e speciali")
    print("- Normalizzazione caratteri tipografici (' -> ', \" -> \", —/– -> -)")
    print("- Normalizzazione spazi e indentazione")
    print("- Applicazione terminatori CRLF")
    print("- Encoding UTF-8")
    
    for md_file in md_files:
        clean_markdown_file(md_file)
    
    print(f"\nCompletato! Processati {len(md_files)} file.")

if __name__ == "__main__":
    main()
