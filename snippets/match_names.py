import zipfile
import xml.etree.ElementTree as ET
import os

def get_excel_names(file_path):
    names = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        shared_strings = []
        try:
            with zip_ref.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in root.findall('.//ns:t', ns):
                    shared_strings.append(t.text)
        except KeyError:
            pass

        try:
            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                # B column is usually index 1
                for row_elem in root.findall('.//ns:row', ns):
                    c_elem = row_elem.find("ns:c[@r^='B']", ns) # This is not standard xpath, need better logic
                    # Let's just find the cell with reference starting with 'B'
                    for c in row_elem.findall('ns:c', ns):
                        if c.get('r').startswith('B'):
                            v_elem = c.find('ns:v', ns)
                            if v_elem is not None:
                                val = v_elem.text
                                if c.get('t') == 's':
                                    val = shared_strings[int(val)]
                                names.append(val)
        except Exception as e:
            print(f"Error reading sheet: {e}")
    return names

def match_files():
    excel_path = "lista de entrevistas.xlsx"
    transcricoes_dir = "05. Transcrições Integrais"
    
    excel_names = get_excel_names(excel_path)
    # Remove header if it exists (usually "Nome")
    if "Nome" in excel_names:
        excel_names.remove("Nome")
    
    files = os.listdir(transcricoes_dir)
    
    matches = []
    not_found = []
    
    for full_name in excel_names:
        if not full_name or full_name == '0': continue
        found = False
        # Normalize name for matching: lowercase, split into parts
        name_parts = full_name.lower().split()
        
        for f in files:
            f_lower = f.lower()
            # If all parts of a name are in the filename (even if shortened)
            # OR if the first and last name are in the filename
            if len(name_parts) >= 2:
                if name_parts[0] in f_lower and name_parts[-1] in f_lower:
                    matches.append((full_name, f))
                    found = True
                    break
            elif len(name_parts) == 1:
                if name_parts[0] in f_lower:
                    matches.append((full_name, f))
                    found = True
                    break
        
        if not found:
            not_found.append(full_name)
            
    print(f"Found {len(matches)} matches out of {len(excel_names)} names from Excel.")
    print("\nMatches:")
    for name, filename in matches:
        print(f"- {name}  ==>  {filename}")
        
    print("\nNames from Excel with no matching file (yet):")
    for name in not_found:
        print(f"- {name}")

if __name__ == "__main__":
    match_files()
