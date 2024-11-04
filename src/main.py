from nicegui import ui as u
from psutil import disk_partitions, disk_usage, virtual_memory, cpu_percent
import platform


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
        with u.tab_panels(tabs, value=os_info).classes("w-left"):
            with u.tab_panel(pc_manager):
                # Tab za pracenje upotrebe CPU RAMA i diska
                u.label("CPU RAM Disk info")

                ram_info = self.manager.show_ram_info()

                u.label(f"Upotreba RAM memorije: {ram_info['used']} GB / {ram_info['total']} GB")

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

    # Funkcija koja prikazuje info o upotrebi procesora
    def show_cpu_info(self):
        pass

    # Funkcija koja prikazuje info o upotrebi procesora
    def show_disk_info(self):
        pass

    # Funkcija koja prikazuje info o operativnom sistemu
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
