import requests

url = "http://localhost:8000/check_zip"  # Change this to the appropriate URL

file_path = "C:\\Users\\Syrym.Nurbaturov\\PycharmProjects\\storage\\zip.zip"
files = {'zip_file': open(file_path, 'rb')}  # Create a dictionary with field name and file object

response = requests.post(url, files=files)

if response.status_code == 200:
    data = response.json()
    found_languages = data.get('found_languages', [])
    found_configurations = data.get('found_configurations', [])
    other_extensions = data.get('other_extensions', [])

    print("Found Languages:", found_languages)
    print("Found Configurations:", found_configurations)
    print("Other Extensions:", other_extensions)
else:
    print("Error:", response.status_code)
