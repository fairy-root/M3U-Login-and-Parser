# Python M3U Login and Parser

This project provides a Python script that facilitates logging into services provided via M3U URLs, extracting, and parsing the necessary information such as host, port, username, password, status, trial information, active connections, maximum connections, expiry date, and category names. It also writes these details into a file for further processing or use.

## Description

The script makes use of the `requests` library to handle HTTP requests and parses URL data to extract login credentials and service details. It then attempts to log in to the specified service, retrieves user information, and categorizes available channels. The output is stored in a text file, providing a convenient way to access service details.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the `requests` library using pip:

```bash
pip install requests
```

## Usage

To use this script, follow these steps:

1. Run the script using Python:

```bash
python iptv.py
```

2. When prompted, enter an M3U URL or type 'exit' to quit the script.

The script will parse the provided URL, attempt to log in, retrieve service details, and output the results into a file named `working.txt` in the script's directory.

## Legality

This script is intended for educational purposes and for use with services for which you have legitimate access rights. Unauthorized access to or use of telecommunication services is illegal and unethical. It is the user's responsibility to comply with all applicable laws and terms of service.

## License

MIT License

Copyright (c) [2024] [fairysubsteam]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Suggestions for Improvement

- **Security Enhancements:** Implement additional checks to ensure that the script is used in compliance with legal and ethical standards. This could include verifying user rights to access the M3U URL before proceeding with the login and parsing process.
- **Error Handling:** Expand error handling to cover more specific scenarios, such as handling invalid JSON responses or unexpected data structures within the response. This can improve the script's robustness and user experience by providing more informative error messages.
- **User Interface:** Consider adding a simple graphical user interface (GUI) for non-technical users. This could make the tool more accessible to a broader audience by allowing users to input details and receive feedback through a user-friendly interface.
- **Performance Optimization:** Analyze the script's performance for potential bottlenecks, especially in handling large numbers of channel categories. Optimizations could include asynchronous requests or parallel processing to improve the script's efficiency.
