import json
import os

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "music_volume": 0.5,
            "sfx_volume": 0.5,
            "difficulty": "normal"
        }
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Загрузка настроек из файла"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()
            
    def save_settings(self):
        """Сохранение настроек в файл с округлением значений громкости"""
        try:
            # Округляем значения громкости до 2 знаков после запятой
            if 'music_volume' in self.settings:
                self.settings['music_volume'] = round(self.settings['music_volume'], 2)
            if 'sfx_volume' in self.settings:
                self.settings['sfx_volume'] = round(self.settings['sfx_volume'], 2)
                
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError:
            print("Не удалось сохранить настройки")
            
    def get(self, key, default=None):
        """Получение значения настройки"""
        return self.settings.get(key, default)
        
    def set(self, key, value):
        """Установка значения настройки"""
        self.settings[key] = value
        self.save_settings()
        
    def reset_to_default(self):
        """Сброс настроек к значениям по умолчанию"""
        self.settings = self.default_settings.copy()
        self.save_settings()