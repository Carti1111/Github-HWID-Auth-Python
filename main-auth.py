# put this above all your code (except imports)
#Strings
hardwareid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
site = requests.get('https://raw.githubusercontent.com/Carti1111/HWID-Auth/main/auth.txt')

try:
    if hardwareid in site.text:
        pass
    else:
        print(f'{Fore.RED}[ERROR] {Fore.WHITE}Whitelist Secret Not Found')
        print(f'{Fore.RED}[HWID] {Fore.WHITE}Your HWID:' + hardwareid)
        time.sleep(1.35) 
        os._exit()
except:
    print(f'{Fore.RED}[ERROR] {Fore.WHITE}Code: 404')
    time.sleep(1.35) 
    os._exit()
    # your program goes below 