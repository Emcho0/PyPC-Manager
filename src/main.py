from nicegui import ui as u
import platform
import subprocess
from psutil import cpu_freq, virtual_memory
import psutil
import time


class UI:
    def __init__(self):
        self.manager = Manager()
        self.tabs_general_ui()

    def tabs_general_ui(self):
        # Osnovni izgled aplikacije
        u.add_css("styles/style.css")
        u.page_title("PyPC Manager")

        with u.tabs().classes("w-left") as tabs:
            pc_manager = u.tab("PC Manager")
            os_info = u.tab("OS Info")

        with u.tab_panels(tabs, value=pc_manager).classes("h-left"):
            with u.tab_panel(pc_manager):
                # Pokazi CPU i RAM informacije
                u.button("Refresh disk list", icon="refresh")
                cpu_info = self.manager.show_cpu_info()
                ram_info = self.manager.show_ram_info()
                u.label(f"RAM usage: {ram_info['used']} GB / {ram_info['total']} GB")

            with u.tab_panel(os_info):
                os_info = self.manager.os_info()


class Manager:
    def __init__(self):
        super().__init__()

    def bytes_to_gb(self, byte):
        one_gb = 1073741824  # bytes
        giga = byte / one_gb
        return "{0:.1f}".format(giga)

    def show_ram_info(self):
        ram_usage = virtual_memory()
        ram_usage = dict(ram_usage._asdict())
        for key in ram_usage:
            if key != "percent":
                ram_usage[key] = self.bytes_to_gb(ram_usage[key])

        return ram_usage

    def show_cpu_info(self):
        u.label("CPU Info")
        os_name = platform.system()

        cpu_name = self.get_cpu_name()
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count(logical=True)
        cpu_f = cpu_freq()
        u.html(f"""
            Detected OS: {os_name} <br>
            CPU Name: {cpu_name} <br>
            Cores: {cpu_count} <br>
            Threads: {logical_cpu_count} <br>
            Frequency: {cpu_f}
              """)

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
