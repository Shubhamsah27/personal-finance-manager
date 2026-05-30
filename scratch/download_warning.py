import requests
import re

url = "https://drive.google.com/uc?export=download&id=1tRFx3e59Wo5W-_oORY4nEvXFvh-DLm7B"
output_path = r"d:\Assessment\financial_manager_tests.sh"

try:
    session = requests.Session()
    # 1. Fetch the warning page
    r = session.get(url)
    html = r.text
    
    # 2. Extract values using regex
    uuid_match = re.search(r'name="uuid"\s+value="([^"]+)"', html)
    confirm_match = re.search(r'name="confirm"\s+value="([^"]+)"', html)
    
    if uuid_match:
        uuid = uuid_match.group(1)
        confirm = confirm_match.group(1) if confirm_match else "t"
        
        # Construct the direct download URL with the dynamic tokens!
        download_url = f"https://drive.usercontent.google.com/download?id=1tRFx3e59Wo5W-_oORY4nEvXFvh-DLm7B&export=download&confirm={confirm}&uuid={uuid}"
        print(f"Constructed download URL: {download_url}")
        
        r2 = session.get(download_url, stream=True)
        if r2.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in r2.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download successful!")
        else:
            print(f"Failed download: Status {r2.status_code}")
    else:
        print("Could not find UUID token in HTML! Fallback to direct parameters...")
        download_url = f"{url}&confirm=t"
        r2 = session.get(download_url, stream=True)
        if r2.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in r2.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download successful on fallback!")
        else:
            print(f"Failed download on fallback: Status {r2.status_code}")
except Exception as e:
    print(f"Error: {e}")
