import platform
import subprocess

from nicegui import ui as u
from psutil import virtual_memory


class UI:
    def __init__(self):
        self.manager = Manager()
        self.tabs_general_ui()

    def tabs_general_ui(self):
        # Stil WEB aplikacije
        u.add_css("styles/style.css")
        u.page_title("PyPC Manager")

        # Dodavanje tabova u lijevu stranu

        with u.tabs().classes("w-left") as tabs:
            pc_manager = u.tab("PC Manager")
            settings = u.tab("Settings")
            os_info = u.tab("OS Info")
        with u.tab_panels(tabs, value=pc_manager).classes("h-left"):
            with u.tab_panel(pc_manager):
                # Tab za pracenje upotrebe CPU RAMA i diska

                ram_info = self.manager.show_ram_info()

                u.label(
                    f"Upotreba RAM memorije: {ram_info['used']} GB / {ram_info['total']} GB"
                )

                cpu_info = self.manager.show_cpu_info()

            # Tab za generalne postavke
            with u.tab_panel(settings):
                u.label("General settings")

            with u.tab_panel(os_info):
                os_info = self.manager.os_info()


class Manager:
    def __init__(self):
        super().__init__()

    def bytes_to_gb(self, byte):
        one_gb = 1073741824  # bajtovi
        giga = byte / one_gb
        giga = "{0:.1f}".format(giga)
        return giga

    # Funkcija koja prikazuje info o upotrebi RAM memorije
    def show_ram_info(self):
        ram_usage = virtual_memory()
        ram_usage = dict(ram_usage._asdict())
        for key in ram_usage:
            if key != "percent":
                ram_usage[key] = self.bytes_to_gb(ram_usage[key])

        return ram_usage

    # Funkcija koja prikazuje info o upotrebi procesora kao i osnovni info o procesoru
    def show_cpu_info(self):
        u.label("CPU Info")
        os_name = platform.system()
        cpu_name = self.get_cpu_name()

        u.html(f"""
            Detected OS: {os_name} <br>
            CPU Name: {cpu_name} """)

    def get_cpu_name(self):
        system = platform.system()

        if system == "Windows":
            try:
                result = subprocess.run(
                    ["wmic", "cpu", "get", "caption"], capture_output=True, text=True
                )
                cpu_name = result.stdout.splitlines()[1].strip()
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

    # Funkcija koja prikazuje info o upotrebi diska
    def show_disk_info(self):
        pass

    # Funkcija koja prikazuje info o operativnom sistemu
    import platform

    # Funkcija koja prikazuje info o operativnom sistemu
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

            # ASCII art for Windows 10
            ascii_art = """
            Insert ascii art here for win 10
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

            # ASCII art for Windows 11
            ascii_art = """
            Insert ascii art here for win 11
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
