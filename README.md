# PC Save Game Backup Tool

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful CLI tool for managing PC game save backups with version control and automated safety features. Never lose your game progress again!

## Features

- 💾 **Version-controlled backups** with timestamps
- 🛡️ **Automatic corruption detection** and recovery
- 🚀 **Bulk operations** for managing multiple games
- ⚙️ **Simple configuration** via JSON or CLI interface
- 🔄 **Safety first** with automatic backup before restore
- 📁 **Flexible storage** with custom backup locations
- 🔒 **Zero dependencies** for maximum compatibility

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python's standard library only)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PC-Save-Game-Backup-Tool.git

# Navigate to the project directory
cd PC-Save-Game-Backup-Tool

# Run the application
python main.py
```

## Quick Start Guide

1. **Launch the application**: `python main.py`
2. **Add a new game**:
   - Select Option 1 from the main menu
   - Enter the game name
   - Provide the save file location

3. **Create a backup**:
   - Select Option 2 from the main menu
   - Choose your game from the list

4. **Restore a backup**:
   - Select Option 3 from the main menu
   - Choose your game and the version to restore

## Usage Guide

### Main Menu Options

1. **Add New Game**: Configure a new game for backup
2. **Create Backup**: Make a timestamped backup of a game's saves
3. **Restore Backup**: Restore a save from a previous backup
4. **List Games**: View all configured games
5. **List Backups**: View all backups for a specific game
6. **Delete Game**: Remove a game from the configuration
7. **Delete Backup**: Remove a specific backup
8. **Exit**: Close the application

### Common Save File Locations

| Platform | Common Save Location |
|----------|----------------------|
| Steam    | `C:\Program Files (x86)\Steam\userdata\[user-id]\[game-id]\remote` |
| Epic     | `C:\Users\[Username]\AppData\Local\[GameName]` |
| GOG      | `C:\Users\[Username]\AppData\Local\GOG.com\Galaxy\Games\[GameName]` |
| Windows Store | `C:\Users\[Username]\AppData\Local\Packages\[GameID]\SystemAppData\wgs` |
| Origin   | `C:\Users\[Username]\Documents\[GameName]` |

## Configuration File

The application uses `game_backup_config.json` to store configuration:

```json
{
    "root_backup_dir": "C:\\save game",
    "games": {
        "Game Name": {
            "source_path": "C:\\Path\\To\\Original\\Save",
            "backup_dir": "C:\\save game\\Game Name"
        }
    }
}
```

### Configuration Options:

- `root_backup_dir`: Base directory for all backups
- `games`: Dictionary of game configurations
  - `source_path`: Location of original save files
  - `backup_dir`: Destination for backups (defaults to `root_backup_dir/game_name`)

## Best Practices

- Close games before backing up or restoring saves
- Run the tool as administrator if you encounter permission issues
- Regular backups are recommended before major game events

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission errors | Run the application as administrator |
| Missing saves | Ensure the game is closed and correct path is configured |
| Configuration problems | Delete or edit `game_backup_config.json` |
| Backup fails | Check disk space and file permissions |

## Project Structure

```
PC-Save-Game-Backup-Tool/
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies (none required)
├── game_backup_config.json     # Configuration file
├── core/                       # Core functionality
│   └── backup_manager.py       # Backup logic implementation
└── ui/                         # User interface
    └── cli_interface.py        # Command-line interface
```

## License

Released under the MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



