import socket
import sys
from ipaddress import IPv4Network


def scan_ports(ip, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)

            sock.close()
        except:
            pass

    return open_ports


def main():
    print("-" * 60)
    print("   Python Network Tabanlı Port Tarama Aracı")
    print("-" * 60)

    # Network alma
    network = input("Taranacak ağ (örn: 192.168.1.0/24): ").strip()
    if not network:
        print("[!] Hata: Ağ adresi boş bırakılamaz.")
        sys.exit(1)

    # Port aralığı alma
    try:
        start_port = int(input("Başlangıç Portu (örn: 1): "))
        end_port = int(input("Bitiş Portu (örn: 1024): "))

        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError
    except ValueError:
        print("[!] Hata: Geçerli bir port aralığı giriniz (1–65535).")
        sys.exit(1)

    # Network doğrulama
    try:
        net = IPv4Network(network, strict=False)
    except:
        print("[!] Hata: Geçersiz network formatı.")
        sys.exit(1)

    print("\n[+] Tarama başlatıldı...\n")

    for ip in net.hosts():
        ip = str(ip)
        print(f"[*] {ip} taranıyor...")

        open_ports = scan_ports(ip, start_port, end_port)

        if open_ports:
            print(f"[✓] {ip} ERİŞİLEBİLİR")
            print(f"    Açık portlar: {open_ports}\n")
        else:
            print(f"[✗] {ip} erişilemedi\n")

    print("--- Tarama Tamamlandı ---")


if __name__ == "__main__":
    main()
