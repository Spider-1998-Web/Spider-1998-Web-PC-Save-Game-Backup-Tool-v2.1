import os
from datetime import datetime

class BackupUI:
    def __init__(self, core):
        self.core = core
        self.version = "3.0"

    def show_main_menu(self):
        """Display main menu interface"""
        while True:
            print(f"\n=== Game Backup Manager v{self.version} ===")
            print(f"Current Root: {self.core.config['root_backup_dir']}")
            print("1. Create New Backup")
            print("2. Update Existing Backup")
            print("3. Restore Backup")
            print("4. List All Games/Backups")
            print("5. Change Root Directory")
            print("6. Update All Game Backups")
            print("7. Restore All Games")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.create_backup_flow()
            elif choice == '2':
                self.update_backup_flow()
            elif choice == '3':
                self.restore_backup_flow()
            elif choice == '4':
                self.list_games_and_backups()
            elif choice == '5':
                self.change_root_directory()
            elif choice == '6':
                self.update_all_backups_flow()
            elif choice == '7':
                self.restore_all_backups_flow()
            elif choice == '8':
                print("\nGoodbye!")
                return
            else:
                print("Invalid choice, please try again")

    def _get_valid_path(self, prompt):
        """Get validated path input"""
        while True:
            path_input = input(prompt).strip()
            path = os.path.expanduser(path_input)
            if os.path.exists(path):
                return os.path.normpath(path)
            print("Path does not exist! Please try again.")

    def _select_game(self):
        """Select from existing games"""
        games = list(self.core.config['games'].keys())
        if not games:
            return None
            
        print("\nConfigured games:")
        for idx, game in enumerate(games, 1):
            print(f"{idx}. {game}")
            
        choice = input("Select game (number): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(games):
            return games[int(choice)-1]
        return None

    def create_backup_flow(self):
        """Handle new backup creation"""
        print("\n=== Create New Backup ===")
        game_name = input("Enter game name: ").strip()
        
        if game_name in self.core.config['games']:
            print("Game already exists! Use Update Backup instead.")
            return
            
        source_path = self._get_valid_path("Enter game save location: ")
        backup_dir = os.path.join(self.core.config['root_backup_dir'], game_name)
        
        self.core.config['games'][game_name] = {
            'source_path': source_path,
            'backup_dir': backup_dir
        }
        self.core._save_config()
        
        success, message = self.core.create_backup(game_name)
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")

    def update_backup_flow(self):
        """Handle backup updates"""
        print("\n=== Update Backup ===")
        if not self.core.config['games']:
            print("No games configured!")
            return
            
        game = self._select_game()
        if game:
            success, message = self.core.create_backup(game)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

    def restore_backup_flow(self):
        """Handle backup restoration"""
        print("\n=== Restore Backup ===")
        if not self.core.config['games']:
            print("No games configured!")
            return
            
        game = self._select_game()
        if game:
            backups = self.core.get_backups(game)
            if not backups:
                print("No backups available!")
                return
                
            print("\nAvailable backups (sorted by newest first):")
            for idx, backup in enumerate(backups, 1):
                print(f"{idx}. {backup['formatted_date']} - {backup['name']}")
                
            choice = input("Select backup to restore (number): ").strip()
            if not choice.isdigit():
                return
                
            selected_backup = backups[int(choice)-1]
            success, message = self.core.restore_backup(game, selected_backup['path'])
            if success:
                print(f"\n✅ Successfully restored {game} from {selected_backup['formatted_date']}")
            else:
                print(f"\n❌ {message}")

    def list_games_and_backups(self):
        """Display all configured games and backups"""
        print("\n=== Configured Games ===")
        for idx, game in enumerate(self.core.config['games'].keys(), 1):
            print(f"{idx}. {game}")
            
        game_choice = input("\nEnter game number to see backups (or press Enter to return): ").strip()
        if game_choice.isdigit():
            game_list = list(self.core.config['games'].keys())
            selected_game = game_list[int(game_choice)-1]
            self._list_backups(selected_game)

    def _list_backups(self, game_name):
        """Display detailed backup list"""
        backups = self.core.get_backups(game_name)
        print(f"\n📂 Backups for {game_name}:")
        for backup in backups:
            size = os.path.getsize(backup['path'])
            print(f"• {backup['formatted_date']} - {backup['name']}")
            print(f"  Size: {size/1024:.2f} KB\n")

    def change_root_directory(self):
        """Change root backup directory"""
        print("\n=== Change Root Directory ===")
        new_root = input("Enter new root directory: ").strip()
        new_root = os.path.normpath(os.path.expanduser(new_root))
        
        try:
            os.makedirs(new_root, exist_ok=True)
            self.core.config['root_backup_dir'] = new_root
            self.core._save_config()
            print(f"\n✅ Root directory changed to: {new_root}")
        except Exception as e:
            print(f"\n❌ Failed to change root directory: {str(e)}")

    def update_all_backups_flow(self):
        """Handle mass update with confirmation"""
        if not self.core.config['games']:
            print("No games configured!")
            return
            
        print("\n⚠️ This will create new backups for ALL configured games!")
        print(f"Total games: {len(self.core.config['games'])}")
        confirmation = input("Type 'YES' to confirm: ").strip()
        
        if confirmation == 'YES':
            results = self.core.update_all_backups()
            print("\nBackup results:")
            for game, result in results.items():
                status = "✅ Success" if result['success'] else "❌ Failed"
                print(f"{game}: {status} - {result['message']}")
        else:
            print("Operation canceled")

    def restore_all_backups_flow(self):
        """Handle mass restore with confirmation"""
        if not self.core.config['games']:
            print("No games configured!")
            return
            
        print("\n⚠️ WARNING: This will overwrite ALL game saves with their latest backups!")
        print(f"Affected games: {len(self.core.config['games'])}")
        print("This cannot be undone!")
        confirmation = input("Type 'CONFIRM' to proceed: ").strip()
        
        if confirmation == 'CONFIRM':
            results = self.core.restore_all_backups()
            print("\nRestore results:")
            for game, result in results.items():
                status = "✅ Success" if result['success'] else "❌ Failed"
                print(f"{game}: {status} - {result['message']}")
        else:
            print("Operation canceled")