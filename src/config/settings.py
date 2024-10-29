import json
import os

class SettingsManager:
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as f:
                return json.load(f)
        return {
            "api_keys": {
                "openai": ""
            },
            "history_limit": 15,
            "startup_enabled": True,
            "hotkeys": {
                "capture_area": "Ctrl+Shift+A",
                "capture_window": "Ctrl+Shift+W"
            },
            "theme": "light"
        }

    def save_settings(self):
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

# Example usage
if __name__ == "__main__":
    settings_manager = SettingsManager(os.path.join('data', 'settings.json'))
    settings_manager.set_setting('api_keys', {'openai': 'your_api_key_here'})
    print(settings_manager.get_setting('api_keys'))
