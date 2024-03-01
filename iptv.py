import requests
import datetime
import urllib.parse
import json
import os

# Parse the URL
def parse(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    # Extract hostname and port
    hostname = parsed_url.hostname
    port = parsed_url.port or 80
    # Extract query parameters
    query_params = urllib.parse.parse_qs(parsed_url.query)
    # Extract username and password
    username = query_params['username'][0]
    password = query_params['password'][0]
    return hostname, port, username, password

# Custom headers
def custom_headers():
    # Set headers
    headers = {
        "Accept": "image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
        "Accept-Language": "en-US",
        "Connection": "Keep-Alive"
    }
    return headers

# The postData as a payload
def create_payload(username, password):
    # Set payload
    payload = {
        "username": username,
        "password": password
    }
    return payload

# Make a post request to the hotname
def login(hostname, port, headers, payload):
    try:
        # Make POST request
        response = requests.post(f"http://{hostname}:{port}/player_api.php", headers=headers, data=payload, allow_redirects=False, timeout=10)
        return response
    except requests.ConnectionError:
        print(f"Connection to {hostname} timed out.")
        return None
    except requests.Timeout:
        print("The request failed to complete. Timeout has ended.")
        return None

# Parse the response data
def data(response):
    max_connections = response.text.split("ections\":\"")[1].split("\"")[0]
    if max_connections == "0":
        max_connections = "Unlimited"
    text = response.text
    data = json.loads(text)
    active_connections = data["user_info"]["active_cons"]
    trial = response.text.split("trial\":\"")[1].split("\"")[0]
    if trial == "0":
        trial = "No"
    elif trial == "1":
        trial = "Yes"
    expire_values = response.text.split("exp_date\":\"")
    if len(expire_values) > 1:
        expire = expire_values[1].split("\"")[0]
        expire = datetime.datetime.fromtimestamp(
            int(expire)).strftime("%Y-%m-%d:%H-%M-%S")
    else:
        # Handle the error here
        expire = "Unlimited"
    status = response.text.split("status\":\"")[1].split("\"")[0]
    return trial, expire, status, max_connections, active_connections

# Make a post request to get channel categories
def channels(hostname, port, username, password, headers):
    try:
        resp = requests.get(f"http://{hostname}:{port}/player_api.php?username={username}&password={password}&action=get_live_categories", headers=headers, timeout=10)
        return resp
    except requests.Timeout:
        print("The request failed to complete. Timeout has ended.")

# Getting channels categories
def category(resp):
    tex = resp.text
    dat = json.loads(tex)
    try:
        category_names = list(map(lambda x: x.get('category_name'), dat))
        return category_names
    except AttributeError as e:
        print(e)

# Write to file
def write(hostname, port, username, password, max_connections, active_connections, trial, status, expire, category_names, working):
    with open(working, "a", encoding="utf-16") as f:
        try:
            f.write(f"Host: http://{hostname}:{port}\nUser: {username}:{password}\nM3U: http://{hostname}:{port}/get.php?username={username}&password={password}&type=m3u_plus\nMax Connections: {max_connections}\nActive Connections: {active_connections}\nTrial: {trial}\nStatus: {status}\nExpiry: {expire}\nCategory Names: {category_names}\n\n")
        except NameError as e:
            print("There was an error!" + e)

# Key check and capture
def condition(working, response):
    try:
        # Login failed
        if "{\"user_info\":{\"auth\":0}}" in response.text or response.status_code == 404 or response.status_code == 500 or response.status_code == 511 or "INVALID_CREDENTIALS" in response.text or "auth\":0" in response.text or response.status_code == 403:
            print("Login Failed")
        # Account is free
        elif "\"Banned\"" in response.text or "\"Expired\"" in response.text or "is_trial\":\"1\"" in response.text:
            print("Account is free")
        # Banned hostname
        elif "Line has been banned" in response.text or response.text == "Redirecting" or "521: Web server is down" in response.text or response.text == "":
            print("Hostname does not exist, down or banned.")
        # Login success
        elif "Success" in response.text or "Active" in response.text or "EXTINF" in response.text or "auth\":1" in response.text:
            trial, expire, status, max_connections, active_connections = data(
            response)
            if "Banned" in status or "Disabled" in status:
                print("Status banned or disabled")
            else:
                print("Login Success\n")
                resp = channels(hostname, port, username, password, headers)
                category_names = category(resp)
                try:
                    # Print the data to console
                    print(f"Host: http://{hostname}:{port}\nUser: {username}:{password}\nM3U: http://{hostname}:{port}/get.php?username={username}&password={password}&type=m3u_plus\nMax Connections: {max_connections}\nActive Connections: {active_connections}\nTrial: {trial}\nStatus: {status}\nExpiry: {expire}\nCategory Names: {category_names}")
                    write(hostname, port, username, password, max_connections,
                      active_connections, trial, status, expire, category_names, working)
                except NameError as e:
                    print("There was an error!")
    except AttributeError:
        print("The request failed to complete. Timeout has ended.")

# Main process
if __name__ == "__main__":
    while True:
        try:
            # Input prompt for the user to enter a URL or 'exit' to quit
            url = input("Enter an m3u URL (type 'exit' to quit): ").strip()

            # Check if the user wants to exit the script
            if url.lower() == 'exit':
                break

            # Ensure a URL was entered
            if not url:
                raise ValueError("No URL entered. Please try again.")

            # Basic validation to check for a common URL pattern
            if "http://" not in url and "https://" not in url:
                raise ValueError("Invalid URL format. Please include http:// or https://")

            # Parse the URL to extract necessary components
            hostname, port, username, password = parse(url)

            # Validate that all required components were successfully extracted
            if not all([hostname, port, username, password]):
                raise ValueError("URL must include hostname, port, username, and password.")

            # Prepare headers and payload for the request
            headers = custom_headers()
            payload = create_payload(username, password)

            # Attempt to log in using the extracted details
            response = login(hostname, port, headers, payload)

            # Check if a response was received
            if response is None:
                print("Unable to get a response from the server. Please try again.")
                continue

            # Get the script's directory for output file storage
            script_dir = os.path.dirname(os.path.abspath(__file__))
            working = os.path.join(script_dir, "working.txt")

            # Process the server's response based on login success or failure
            condition(working, response)
            print("\nProcess finished. Ready for the next URL.")

        except ValueError as e:
            # Handle user input and validation errors
            print(e)
            continue
        except Exception as e:
            # Catch-all for any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            continue