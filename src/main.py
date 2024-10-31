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

        with u.tabs().classes('w-left') as tabs:
            pc_manager = u.tab("PC Manager")
            settings = u.tab("Settings")
        with u.tab_panels(tabs,value=settings).classes('w-left'):
            with u.tab_panel(pc_manager):
                u.label("CPU RAM Disk info")
                
                ram_info = self.manager.show_ram_info()

                u.label(f"Upotreba RAM memorije: {ram_info['used']} GB / {ram_info['total']} GB")



            with u.tab_panel(settings):
                u.label("General settings")

class Manager:
    def __init__(self):
        super().__init__()

    def bytes_to_gb(self,byte):
        one_gb = 1073741824 # bajtovi
        giga = byte/one_gb
        giga='{0:.1f}'.format(giga)
        return giga
    # Funkcija koja prikazuje info o upotrebi RAM memorije i sl.
    def show_ram_info(self):
        ram_usage = virtual_memory()
        ram_usage = dict(ram_usage._asdict())
        for key in ram_usage:
            if key!= 'percent':
                ram_usage[key]=self.bytes_to_gb(ram_usage[key])

        return ram_usage







def main():
    app = UI()
    u.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
