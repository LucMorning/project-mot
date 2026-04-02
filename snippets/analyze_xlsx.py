import zipfile
import xml.etree.ElementTree as ET
import os

def analyze_xlsx(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Load Shared Strings
        shared_strings = []
        try:
            with zip_ref.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                # The namespace for sharedStrings is usually 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in root.findall('.//ns:t', ns):
                    shared_strings.append(t.text)
        except KeyError:
            # Maybe there are no shared strings
            pass

        # Load Sheet1
        rows = []
        try:
            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for row_elem in root.findall('.//ns:row', ns):
                    row_data = {}
                    for c in row_elem.findall('ns:c', ns):
                        cell_ref = c.get('r')
                        v_elem = c.find('ns:v', ns)
                        if v_elem is not None:
                            val = v_elem.text
                            # Check if the type is 's' (shared string)
                            if c.get('t') == 's':
                                val = shared_strings[int(val)] if int(val) < len(shared_strings) else val
                            row_data[cell_ref] = val
                    rows.append(row_data)
        except KeyError:
            print("Sheet1 not found.")
            return

        # Simple display
        header = None
        for r in rows:
            if not header:
                header = r
                print("Header:", header)
            else:
                print(r)

if __name__ == "__main__":
    analyze_xlsx("lista de entrevistas.xlsx")
