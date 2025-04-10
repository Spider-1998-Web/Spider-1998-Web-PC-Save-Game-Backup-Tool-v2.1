import os
import shutil
import json
import urllib.parse
from datetime import datetime

CONFIG_FILE = "game_backup_config.json"
DEFAULT_ROOT = r"C:\save game"
SAVEGAME_PRO_URL = "https://savegame.pro/"

class GameBackupCore:
    def __init__(self):
        self.config = self._load_config()
        self._ensure_root_structure()

    def _load_config(self):
        """Load configuration with robust error handling"""
        config_path = os.path.abspath(CONFIG_FILE)
        default_config = {
            'root_backup_dir': DEFAULT_ROOT,
            'games': {}
        }

        try:
            if not os.path.exists(config_path):
                self._create_new_config(config_path, default_config)
                return default_config

            with open(config_path, 'r') as f:
                if os.stat(config_path).st_size == 0:
                    raise json.JSONDecodeError("Empty config file", "", 0)

                config = json.load(f)
                return self._validate_config(config, default_config)

        except Exception as e:
            print(f"⚠️ Config error: {str(e)} - Reinitializing")
            return self._reinitialize_config(config_path, default_config)

    def _create_new_config(self, path, default_config):
        """Create new config file"""
        with open(path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    def _validate_config(self, config, default_config):
        """Ensure required keys exist"""
        if 'root_backup_dir' not in config:
            config['root_backup_dir'] = default_config['root_backup_dir']
        if 'games' not in config:
            config['games'] = default_config['games']
        return config

    def _reinitialize_config(self, path, default_config):
        """Handle config recovery"""
        try:
            backup_path = f"{path}.bak"
            shutil.copy(path, backup_path)
            print(f"💾 Original config backed up to {backup_path}")
        except Exception as e:
            print(f"⚠️ Config backup failed: {str(e)}")

        self._create_new_config(path, default_config)
        return default_config.copy()

    def _save_config(self):
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def _ensure_root_structure(self):
        """Create root directory if missing"""
        root_dir = self.config.get('root_backup_dir', DEFAULT_ROOT)
        os.makedirs(root_dir, exist_ok=True)

    def create_backup(self, game_name):
        """Core backup creation logic"""
        try:
            cfg = self.config['games'][game_name]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(cfg['backup_dir'], f"backup_{timestamp}")
            
            os.makedirs(cfg['backup_dir'], exist_ok=True)
            if os.path.isdir(cfg['source_path']):
                shutil.copytree(cfg['source_path'], backup_path)
            else:
                shutil.copy2(cfg['source_path'], backup_path)
            return True, f"Backup created: {os.path.basename(backup_path)}"
        except Exception as e:
            return False, str(e)

    def restore_backup(self, game_name, backup_path):
        """Core restore logic"""
        try:
            cfg = self.config['games'][game_name]
            if os.path.isdir(cfg['source_path']):
                shutil.rmtree(cfg['source_path'])
            elif os.path.exists(cfg['source_path']):
                os.remove(cfg['source_path'])
                
            if os.path.isdir(backup_path):
                shutil.copytree(backup_path, cfg['source_path'])
            else:
                shutil.copy2(backup_path, cfg['source_path'])
            return True, None
        except Exception as e:
            return False, str(e)

    def get_backups(self, game_name):
        """Get sorted backups with timestamp info"""
        backup_dir = self.config['games'][game_name]['backup_dir']
        if not os.path.exists(backup_dir):
            return []
            
        backups = []
        for entry in os.listdir(backup_dir):
            if entry.startswith("backup_"):
                entry_path = os.path.join(backup_dir, entry)
                mtime = os.path.getmtime(entry_path)
                dt = datetime.fromtimestamp(mtime)
                backups.append({
                    'path': entry_path,
                    'name': entry,
                    'timestamp': mtime,
                    'formatted_date': dt.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

    def search_save_locations(self, game_name):
        """Generate proper search URL"""
        encoded_query = urllib.parse.quote_plus(game_name)
        return {
            'search_url': f"{SAVEGAME_PRO_URL}?s={encoded_query}",
            'game': game_name
        }

    def update_all_backups(self):
        """Update backups for all configured games"""
        results = {}
        for game_name in self.config['games'].keys():
            success, message = self.create_backup(game_name)
            results[game_name] = {
                'success': success,
                'message': message
            }
        return results

    def restore_all_backups(self):
        """Restore all games to their latest backups"""
        results = {}
        for game_name in self.config['games'].keys():
            backups = self.get_backups(game_name)
            if not backups:
                results[game_name] = {
                    'success': False,
                    'message': 'No backups available'
                }
                continue
                
            latest_backup = backups[0]
            success, message = self.restore_backup(game_name, latest_backup['path'])
            results[game_name] = {
                'success': success,
                'message': message or f"Restored from {latest_backup['formatted_date']}"
            }
        return results