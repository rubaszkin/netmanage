import subprocess
import os
import sys

try:
    import psutil
except ImportError:
    print("Trying to install required module: foo")
    os.system('python -m pip install psutil')
    # Now import the module again for global access
    import psutil

def get_available_network_adapters():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    available_networks = []
    for intface, addr_list in addresses.items():
        if any(getattr(addr, 'address').startswith("169.254") for addr in addr_list):
            continue
        elif intface in stats and getattr(stats[intface], "isup"):
            available_networks.append(intface)
    return available_networks

def enable_network_adapter(adapter_index):
    subprocess.call(f'wmic path win32_networkadapter where index={adapter_index} call enable', shell=True)

def disable_network_adapter(adapter_index):
    subprocess.call(f'wmic path win32_networkadapter where index={adapter_index} call disable', shell=True)

def enable_wifi():
    os.system("netsh interface set interface 'Wi-Fi' enabled")

def disable_wifi():
    os.system("netsh interface set interface 'Wi-Fi' disabled")

def print_colored(text, color="white"):
    colors = {
        "white": "\033[0m",
        "green": "\033[92m"
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['white']}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python my_script.py [D/d] or [E/e]")
        sys.exit(1)

    action = sys.argv[1].lower()
    available_adapters = get_available_network_adapters()

    if action == "d":
        for adapter in available_adapters:
            disable_network_adapter(available_adapters.index(adapter) + 1)
        disable_wifi()
        print("All network adapters and Wi-Fi are now disabled.")
    elif action == "e":
        for adapter in available_adapters:
            enable_network_adapter(available_adapters.index(adapter) + 1)
        enable_wifi()
        print("All network adapters and Wi-Fi are now enabled.")
    else:
        print("Invalid argument. Please provide 'D' or 'E'.")

if __name__ == "__main__":
    main()