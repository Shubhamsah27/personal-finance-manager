import requests

url = "https://drive.google.com/uc?export=download&id=1tRFx3e59Wo5W-_oORY4nEvXFvh-DLm7B"
output_path = r"d:\Assessment\financial_manager_tests.sh"

print("Downloading financial_manager_tests.sh from Google Drive...")
try:
    session = requests.Session()
    # First, request the URL to get the warning page and cookies
    response = session.get(url)
    
    # Extract the confirmation code from the cookies or page content
    confirm_token = None
    for cookie in session.cookies:
        if cookie.name.startswith("download_warning"):
            confirm_token = cookie.value
            break
            
    if confirm_token:
        # Request with confirmation token
        download_url = f"{url}&confirm={confirm_token}"
    else:
        # Try a direct fallback with common confirm=t
        download_url = f"{url}&confirm=t"
        
    print(f"Requesting download URL: {download_url}")
    response = session.get(download_url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download successful!")
    else:
        print(f"Failed to download, HTTP status: {response.status_code}")
except Exception as e:
    print(f"Error during download: {e}")
