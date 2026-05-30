import re

pdf_path = r"C:\Users\Lenovo\Downloads\Personal Finance Manager - Assignment (4).pdf"

with open(pdf_path, 'rb') as f:
    content = f.read()

# Search for /URI (http...) or /URI (https...)
# In PDFs, URIs are typically enclosed in parentheses or hex encoded
uris = re.findall(b'/URI\\s*\\(([^)]+)\\)', content)

print("Found URIs:")
seen = set()
for uri in uris:
    decoded = uri.decode('utf-8', errors='ignore')
    if decoded not in seen:
        print(f"- {decoded}")
        seen.add(decoded)
