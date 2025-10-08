import sys
try:
    import PyPDF2
    with open('Informe.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Total de páginas: {len(reader.pages)}\n")
        print("=" * 80)
        for i in range(min(10, len(reader.pages))):
            print(f"\n{'=' * 80}")
            print(f"PÁGINA {i+1}")
            print(f"{'=' * 80}\n")
            text = reader.pages[i].extract_text()
            print(text)
except Exception as e:
    print(f"Error: {e}")
    print("\nIntentando con método alternativo...")
    # Método alternativo
    with open('Informe.pdf', 'rb') as f:
        content = f.read()
        # Buscar texto entre streams
        import re
        texts = re.findall(b'/Title \((.*?)\)', content)
        for t in texts[:20]:
            try:
                print(t.decode('utf-8', errors='ignore'))
            except:
                pass
