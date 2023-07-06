import paramiko
from art import *
from colorama import init, Fore, Style

# Menginisialisasi Colorama
init(autoreset=True)

# Fungsi untuk menjalankan perintah pada MikroTik
def execute_command(ssh, command):
    ssh.exec_command(command)

# Fungsi untuk mengatur konfigurasi dasar MikroTik
def configure_mikrotik(ssh):
    # Tambahkan konfigurasi dasar yang sering digunakan di sini
    commands = [
        'interface wireless set [find] mode=ap-bridge ssid=MyNetwork',
        'ip address add address=192.168.1.1/24 interface=ether1',
        'ip dhcp-server network add address=192.168.1.0/24 gateway=192.168.1.1',
        'ip pool add name=dhcp-pool ranges=192.168.1.100-192.168.1.200',
        'ip dhcp-server add interface=ether1 address-pool=dhcp-pool lease-time=1h',
        'system identity set name=MyRouter'
    ]

    # Menjalankan perintah konfigurasi satu per satu
    for command in commands:
        execute_command(ssh, command)

# Fungsi untuk menambahkan konfigurasi IP address
def configure_ip_address(ssh):
    # Konfigurasi IP address
    command = 'ip address add address=192.168.1.2/24 interface=ether2'
    execute_command(ssh, command)

# Fungsi untuk mengatur konfigurasi bridge
def configure_bridge(ssh):
    # Konfigurasi bridge
    command = 'interface bridge add name=bridge1'
    execute_command(ssh, command)

# Fungsi untuk mengatur konfigurasi DNS
def configure_dns(ssh):
    # Konfigurasi DNS
    command = 'ip dns set servers=8.8.8.8'
    execute_command(ssh, command)

# Fungsi untuk mengatur konfigurasi NAT
def configure_nat(ssh):
    # Konfigurasi NAT
    command = 'ip firewall nat add chain=srcnat action=masquerade out-interface=ether1'
    execute_command(ssh, command)

# Fungsi untuk mengatur konfigurasi Firewall
def configure_firewall(ssh):
    # Konfigurasi Firewall
    command = 'ip firewall filter add chain=input action=drop'
    execute_command(ssh, command)

# Fungsi untuk mencetak logo banner
def print_banner():
    banner = text2art("Andhika", font='block')
    print(Fore.CYAN + banner)

# Fungsi untuk menghubungkan ke MikroTik melalui SSH
def connect_to_mikrotik(hostname, username, password):
    # Membuat koneksi SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    # Mencetak logo banner
    print_banner()

    # Memilih pilihan konfigurasi
    select_template(ssh)

    # Menutup koneksi SSH
    ssh.close()

# Fungsi untuk memilih template konfigurasi
def select_template(ssh):
    print("Pilih template konfigurasi:")
    print("1. Konfigurasi Dasar")
    print("2. Tambah IP Address")
    print("3. Tambah DHCP Client")
    print("4. Konfigurasi Bridge")
    print("5. Konfigurasi DNS")
    print("6. Konfigurasi NAT")
    print("7. Konfigurasi Firewall")

    choice = input("Pilihan: ")

    if choice == '1':
        # Mengatur konfigurasi dasar
        configure_mikrotik(ssh)
    elif choice == '2':
        # Menambahkan konfigurasi IP address
        configure_ip_address(ssh)
    elif choice == '3':
        # Menambahkan konfigurasi DHCP client
        configure_dhcp_client(ssh)
    elif choice == '4':
        # Mengatur konfigurasi bridge
        configure_bridge(ssh)
    elif choice == '5':
        # Mengatur konfigurasi DNS
        configure_dns(ssh)
    elif choice == '6':
        # Mengatur konfigurasi NAT
        configure_nat(ssh)
    elif choice == '7':
        # Mengatur konfigurasi Firewall
        configure_firewall(ssh)
    else:
        print("Pilihan tidak valid!")

# Memanggil fungsi untuk memilih template konfigurasi
connect_to_mikrotik('hostname', 'username', 'password')
