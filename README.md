# PPTP Brute-Force Script
```
 █████╗ ██████╗  █████╗ ██████╗  █████╗ ███╗   ██╗ █████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗
███████║██████╔╝███████║██║  ██║███████║██╔██╗ ██║███████║
██╔══██║██╔═══╝ ██╔══██║██║  ██║██╔══██║██║╚██╗██║██╔══██║
██║  ██║██║     ██║  ██║██████╔╝██║  ██║██║ ╚████║██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
https://www.amnafzar.net/
By: @KalhorAlireza
```
## Overview

RoundCube Brute-Forcer is a Python-based script designed to perform brute force attacks on RoundCube webmail login panels. It supports multi-threading, handles session tokens automatically, and provides the capability to brute force multiple targets, usernames, and passwords. The script outputs successful login credentials (hits) to a specified file.

## Features

- Multi-threaded brute-forcing for efficiency.
- Supports individual or file-based inputs for usernames, passwords, and targets.
- Automatically retrieves session tokens for login attempts.
- Handles "too many failed login attempts" errors gracefully with retries.
- Saves successful login credentials (hits) to a specified output file.
- Built-in user-friendly command-line interface with detailed help.

## Requirements

- Python 3.6+
- Required Python libraries:
  - `rich`
  - `beautifulsoup4`
  - `urllib3`
  - `requests`
You can install the required dependencies using pip:
```bash
pip3 install rich beautifulsoup4 requests
```

## Usage

### Command Syntax

```bash
python3 RC-Brute.py [options]
```

### Options

- `-u` or `--username`: Single username or a file containing usernames (one per line).
- `-p` or `--password`: Single password or a file containing passwords (one per line).
- `-t` or `--target`: Single URL or a file containing URLs (one per line).
- `-o` or `--output`: File to save successful login credentials (default: `results.txt`).
- `-n` or `--thread`: Number of threads to use for brute-forcing (default: 5).

### Example Usage

- **Single Target, Single Username, and Password List**
```bash
python3 RC-Brute.py -u admin -p passwords.txt -t https://example.com
```
- **Multiple Targets, Usernames, and Passwords**
```bash
python3 RC-Brute.py -u usernames.txt -p passwords.txt -t targets.txt -o hits.txt
```

### Example Output
Successful login attempts are saved in the output file in the following format:
```text
https://example.com:::admin:::password123
https://mail.example.com:::user1:::password456
```