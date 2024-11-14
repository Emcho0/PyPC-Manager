import platform
import subprocess

import psutil
from nicegui import ui as u
from psutil import cpu_freq, disk_partitions, disk_usage, virtual_memory


class UI:
    def __init__(self):
        self.manager = Manager()
        self.tabs_general_ui()

    def tabs_general_ui(self):
        # Stil web aplikacije
        u.add_css("styles/style.css")
        u.page_title("PyPC Manager")

        with u.tabs().classes("w-left").classes("tabs") as tabs:
            pc_manager = u.tab("PC Manager", icon="home")
            os_info = u.tab("OS Info", icon="info")

        with u.tab_panels(tabs, value=pc_manager).classes("h-left"):
            with u.tab_panel(pc_manager).classes("tab_panel"):
                # Prikazivanje informacija o procesoru
                self.manager.show_cpu_info()

                # Prikazivanje informacija o RAM upotrebi
                self.ram_label = u.label("RAM usage: Loading...").classes(
                    "text-positive"
                )

                # Timer za osvjezavanje memorije svake sekunde
                u.timer(1.0, self.refresh_ram_info)

                # Displaying disk information
                self.disk_ui()

            # Dodajemo .classes("tab_panel") za stil informacija unutar taba
            with u.tab_panel(os_info).classes("tab_panel"):
                self.manager.os_info()
                self.show_os_info()

    def refresh_ram_info(self):
        ram_info = self.manager.show_ram_info()
        ram_used_percentage = ram_info["percent"]

        ram_text = f"RAM usage: {ram_info['used']} GB / {ram_info['total']} GB ({ram_used_percentage}%)"
        self.ram_label.text = ram_text

        if ram_used_percentage > 80:
            self.ram_label.classes(remove="text-warning")
            self.ram_label.classes(remove="text-positive")
            self.ram_label.classes(add="text-negative")  # Visoka upotreba RAM memorije
        elif 50 <= ram_used_percentage <= 80:
            self.ram_label.classes(remove="text-positive")
            self.ram_label.classes(remove="text-negative")
            self.ram_label.classes(add="text-warning")  # Umjerena upotreba RAM memorije
        else:
            self.ram_label.classes(remove="text-warning")
            self.ram_label.classes(remove="text-negative")
            self.ram_label.classes(add="text-positive")  # Niska upotreba RAM memorije

    def disk_ui(self):
        disk_info = self.manager.show_disk_info()

        # Prikazi informacije o svakom disku unutar tabele (staticki)
        u.table(
            columns=[
                {"name": "device", "label": "Device", "field": "device"},
                {"name": "total", "label": "Total Space", "field": "total"},
                {"name": "used", "label": "Used Space", "field": "used"},
                {"name": "free", "label": "Free Space", "field": "free"},
                {"name": "percent", "label": "% Used", "field": "percent"},
            ],
            rows=disk_info,
        ).classes("w-full").classes("table")

    def show_os_info(self):
        os = platform.system()
        release = platform.release()

        if os == "Windows" and release.startswith("10"):
            u.label("Windows 10")
        elif os == "Windows" and release.startswith("11"):
            u.label("Windows 11")
        else:
            u.label("Unsupported OS")


class Manager:
    def __init__(self):
        super().__init__()

    def bytes_to_gb(self, byte):
        one_gb = 1073741824
        giga = byte / one_gb
        return "{0:.1f}".format(giga)

    def show_disk_info(self):
        # Informacije su smjestene kao niz
        disk_info = []
        partitions = disk_partitions(all=False)
        for partition in partitions:
            usage = disk_usage(partition.mountpoint)
            disk_info.append(
                {
                    "device": partition.device,
                    "total": f"{self.bytes_to_gb(usage.total)} GB",
                    "used": f"{self.bytes_to_gb(usage.used)} GB",
                    "free": f"{self.bytes_to_gb(usage.free)} GB",
                    "percent": f"{usage.percent} %",
                }
            )
        return disk_info

    def show_ram_info(self):
        ram_usage = virtual_memory()
        ram_usage = dict(ram_usage._asdict())

        for key in ram_usage:
            if key != "percent":
                ram_usage[key] = self.bytes_to_gb(ram_usage[key])

        return ram_usage

    def show_cpu_info(self):
        # Prikazi info o procesoru
        self.cpu_label = u.label("CPU Info: Loading...").classes("text-left")
        self.update_cpu_info()

    def update_cpu_info(self):
        cpu_f = cpu_freq()
        current_cpu_freq = f"{cpu_f.current:.2f} MHz"

        cpu_name = self.get_cpu_name()
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count(logical=True)

        self.cpu_label.text = f"CPU: {cpu_name} | Cores: {cpu_count} | Threads: {logical_cpu_count} | Frequency: {current_cpu_freq}"

    def get_cpu_name(self):
        system = platform.system()

        if system == "Windows":
            try:
                # Powershell komanda koja prikazuje tacne informacije o nazivu procesora
                result = subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name",
                    ],
                    capture_output=True,
                    text=True,
                )
                cpu_name = result.stdout.strip()

                if not cpu_name:
                    return "No CPU info found (PowerShell command failed)."
                return cpu_name

            except Exception as e:
                return f"Error retrieving CPU info on Windows: {e}"

        elif system == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("model name"):
                            return line.split(":")[1].strip()
                return "CPU model name not found in /proc/cpuinfo"
            except Exception as e:
                return f"Error retrieving CPU info on Linux: {e}"

        return "Unsupported OS"

    def os_info(self):
        system_info = platform.uname()

        u.label("System Information:")
        u.html(f"""
            System: {system_info.system} <br>
            Node name: {system_info.node} <br>
            Release: {system_info.release} <br>
            Version: {system_info.version} <br>
            Machine: {system_info.machine} <br>
        """)


def main():
    app = UI()
    u.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
