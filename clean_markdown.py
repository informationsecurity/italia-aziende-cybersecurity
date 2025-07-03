#!/usr/bin/env python3
"""
Script per pulire i file Markdown:
- Rimuove spazi a inizio riga
- Rende vuote le linee composte solo da spazi/tab
- Fa trim delle righe (rimuove spazi in fondo)
- Normalizza gli a capo con \r\n (CRLF)
"""

import os
import glob

def clean_markdown_file(filepath):
    """Pulisce un singolo file markdown"""
    try:
        # Leggi il file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cleaned_lines = []
        for line in lines:
            # Rimuovi \n e \r dalla fine
            line = line.rstrip('\n\r')
            
            # Se la linea contiene solo spazi o tab, rendila vuota
            if line.strip() == '':
                cleaned_lines.append('')
            else:
                # Rimuovi spazi a inizio riga e fai trim della fine
                cleaned_line = line.lstrip(' \t').rstrip()
                cleaned_lines.append(cleaned_line)
        
        # Scrivi il file con terminatori CRLF
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            for i, line in enumerate(cleaned_lines):
                if i < len(cleaned_lines) - 1:
                    f.write(line + '\r\n')
                else:
                    # Ultima riga senza newline finale se era vuota
                    if line:
                        f.write(line + '\r\n')
                    else:
                        f.write(line)
        
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
    
    for md_file in md_files:
        clean_markdown_file(md_file)
    
    print(f"\nCompletato! Processati {len(md_files)} file.")

if __name__ == "__main__":
    main()
