import subprocess
import json
import socket

def ping_pc():
    command = ["ping", "-c", "1", "192.168.1.27"]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        return "Online"
    else :
        return "Offline"

def ping_vpn():
    command = ["ping", "-c", "1", "100.73.127.41"]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        return "Online"
    else :
        return "Offline"
    
def get_cpu(json_data):
    if json_data.get("Text") == "CPU Core" and json_data.get("Type") == "Temperature":
        return json_data
    for elem in json_data.get("Children", []):
        temp = get_cpu(elem)
        if temp:
            return temp

def check_cpu():
    output = subprocess.check_output(["curl", "-s", "http://192.168.1.27:8085/data.json"], text=True)
    data = json.loads(output)
    cpu = get_cpu(data)
    return cpu["Value"]

def get_ram(json_data):
    if json_data.get("Text") == "Memory" and json_data.get("Type") == "Load":
        return json_data
    for c in json_data.get("Children", []):
        temp = get_ram(c)
        if temp:
            return temp

def check_ram():
    output = subprocess.check_output(["curl", "-s", "http://192.168.1.27:8085/data.json"], text=True)
    data = json.loads(output)
    ram = get_ram(data)
    return ram["Value"]

def wake_on_lan(mac_address: str):

    packet = bytes.fromhex("FF" * 6 + mac_address * 16)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, ("<broadcast>", 9))