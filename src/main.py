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

        with u.tabs().classes("w-left") as tabs:
            pc_manager = u.tab("PC Manager")
            os_info = u.tab("OS Info")

        with u.tab_panels(tabs, value=pc_manager).classes("h-left"):
            with u.tab_panel(pc_manager):
                self.manager.show_cpu_info()

                self.ram_label = u.label("RAM usage: Loading...").classes(
                    "text-positive"
                )

                # Tajmer za osvjezavanje ram memorije svake sekunde
                u.timer(1.0, self.refresh_ram_info)

                # Tajmer za osvjezavanje informacije o disku svake 2 sekunde
                u.timer(2.0, self.update_disk_info)

                # Display the disk info using the refreshable function
                self.disk_ui()

            with u.tab_panel(os_info):
                self.manager.os_info()

    def refresh_ram_info(self):
        ram_info = self.manager.show_ram_info()
        ram_used_percentage = ram_info["percent"]

        ram_text = f"RAM usage: {ram_info['used']} GB / {ram_info['total']} GB ({ram_used_percentage}%)"

        self.ram_label.text = ram_text

        if ram_used_percentage > 80:
            self.ram_label.classes(
                replace="text-negative"
            )  # Za visoku upotrebu RAM memorije
        else:
            self.ram_label.classes(
                replace="text-positive"
            )  # Za nisku upotrebu RAM memorije

    """ Dekorator u pythonu koji osvjezava informacije o novom disk
    uredjaju ako je iskljucen"""

    @u.refreshable
    def disk_ui(self):
        # Fetch the updated disk information
        disk_info = self.manager.show_disk_info()

        # Create a table for disk info dynamically
        u.table(
            columns=[
                {"name": "device", "label": "Uredjaj", "field": "device"},
                {"name": "total", "label": "Ukupan prostor", "field": "total"},
                {"name": "used", "label": "Upotrijebljen prostor", "field": "used"},
                {"name": "free", "label": "Slobodan prostor", "field": "free"},
                {"name": "percent", "label": "% Upotrijebljeno", "field": "percent"},
            ],
            rows=disk_info,
        ).classes("w-full")

    def update_disk_info(self):
        self.disk_ui.refresh()


class Manager:
    def __init__(self):
        super().__init__()

    def bytes_to_gb(self, byte):
        one_gb = 1073741824  # bytes
        giga = byte / one_gb
        return "{0:.1f}".format(giga)

    # Prikazuje informacije o svakom disku kao tabelu
    def show_disk_info(self):
        disk_info = []
        partitions = disk_partitions(all=False)
        for partition in partitions:
            # Get disk usage for each partition
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

    # Prikazuje informacije o ram memoriji
    def show_ram_info(self):
        ram_usage = virtual_memory()
        ram_usage = dict(ram_usage._asdict())

        for key in ram_usage:
            if key != "percent":
                ram_usage[key] = self.bytes_to_gb(ram_usage[key])

        return ram_usage

    def show_cpu_info(self):
        self.cpu_label = u.label("CPU Info: Loading...").classes(
            "text-center"
        )  # Initial label
        u.timer(1.0, self.update_cpu_info)

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
        os = platform.system()
        release = platform.release()

        if os == "Windows" and release.startswith("10"):
            u.label("System Information:")
            u.html(f"""
                System: {system_info.system} <br>
                Node name: {system_info.node} <br>
                Release: {system_info.release} <br>
                Version: {system_info.version} <br>
                Machine: {system_info.machine} <br>
            """)
            ascii_art = """
            """
            u.html(f"<pre>{ascii_art}</pre>")

        elif os == "Windows" and release.startswith("11"):
            u.label("System Information:")
            u.html(f"""
                System: {system_info.system} <br>
                Node name: {system_info.node} <br>
                Release: {system_info.release} <br>
                Version: {system_info.version} <br>
                Machine: {system_info.machine} <br>
            """)
            ascii_art = """
            ############    ############
            ############    ############
            ############    ############
            ############    ############

            ############    ############
            ############    ############
            ############    ############
            ############    ############
            """
            u.html(f"<pre>{ascii_art}</pre>")

        else:
            u.label("Unsupported OS or Version")
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
