import tkinter as tk
from tkinter import messagebox
import ctypes
import sys
import subprocess
import time

test = False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Hata", "Komut çalıştırma sırasında bir hata oluştu.")

def select_windows_version():
    if not test and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        messagebox.showwarning("Yönetici İzni Gerekli", "Bu uygulamayı kullanmak için yönetici izni gereklidir.")
        sys.exit(0)

    root = tk.Tk()
    root.title("Windows Sürümü Seçin")

    def select_version(version):
        root.destroy()
        select_windows_details(version)

    label = tk.Label(root, text="Lütfen bir Windows sürümü seçin:")
    label.pack()

    button_win10 = tk.Button(root, text="Windows 10", command=lambda: select_version("Windows 10"))
    button_win10.pack()

    button_win11 = tk.Button(root, text="Windows 11", command=lambda: select_version("Windows 11"))
    button_win11.pack()

    root.mainloop()

def select_windows_details(version):
    root = tk.Tk()
    root.title(f"{version} Detay Seçin")

    label = tk.Label(root, text=f"Lütfen {version} için bir detay seçin:")
    label.pack()

    if version == "Windows 10":
        details = {
            "Professional": "slmgr.vbs /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX",
            "Home Single Language": "slmgr.vbs /ipk 7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
            "Home": "slmgr.vbs /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
            "Enterprise": "slmgr.vbs /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43",
            "Education": "slmgr.vbs /ipk NW6C2-QMPVW-D7KKK-3GKT6-VCFB2"
        }
    elif version == "Windows 11":
        details = {
            "Home Single Language": "slmgr /ipk 7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
            "Professional": "slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX",
            "Education": "slmgr /ipk NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
            "Enterprise": "slmgr /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43"
        }

    def select_detail(detail):
        root.destroy()
        command = details.get(detail)
        if command:
            run_command(command)
            time.sleep(3)
            run_command("slmgr /skms kms8.msguides.com")
            time.sleep(3)
            run_command("slmgr.vbs /ato")
            messagebox.showinfo("Başarılı", f"{detail} seçildi ve etkinleştirildi.")
        else:
            messagebox.showerror("Hata", "Geçerli bir detay seçilmedi veya komut bulunamadı.")

    for detail in details:
        button = tk.Button(root, text=detail, command=lambda d=detail: select_detail(d))
        button.pack()

    root.mainloop()

if __name__ == "__main__":
    select_windows_version()
