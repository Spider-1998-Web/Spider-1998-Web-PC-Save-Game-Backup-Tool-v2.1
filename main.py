from core.backup_manager import GameBackupCore
from ui.cli_interface import BackupUI

def main():
    # Initialize core functionality
    backup_core = GameBackupCore()
    
    # Initialize UI with core dependency
    ui = BackupUI(backup_core)
    
    # Start the application
    ui.show_main_menu()

if __name__ == "__main__":
    main()