import pygame
import os
from .constants import *
import time


class SoundManager:
    def __init__(self, settings_manager=None):
        pygame.mixer.init()
        self.settings_manager = settings_manager
        
        # Пути к звуковым файлам
        script_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(os.path.dirname(script_dir), 'assets')
        
        # Словарь для хранения загруженных звуков
        self.sounds = {}
        
        # Словарь каналов для управления воспроизведением
        self.channels = {}
        
        # Инициализируем громкость из настроек или значениями по умолчанию
        if self.settings_manager:
            self.music_volume = self.settings_manager.get("music_volume", 0.5)
            self.sfx_volume = self.settings_manager.get("sfx_volume", 0.5)
        else:
            self.music_volume = 0.5
            self.sfx_volume = 0.5
            
        # Словарь для отслеживания времени последнего использования звуков
        self.last_used = {}
        
        # Словарь приоритетов звуков (чем выше значение, тем выше приоритет)
        self.sound_priorities = {
            "music": 10,
            "menu": 10,
            "explosion": 9,  # Высокий приоритет для звука взрыва
            "shoot": 7   # Средний приоритет для звука выстрела
        }
        
        # Максимальное количество звуков в кэше
        self.max_cache_size = 15  # Увеличил размер кэша
        
        # Время жизни звука в кэше (в секундах)
        self.sound_ttl = 120  # Увеличил до 2 минут
        
        # Максимальное количество одновременных воспроизведений для каждого звука
        self.max_concurrent_playbacks = {
            "shoot": 3,  # Ограничим количество одновременных выстрелов
            "explosion": 5,
            "music": 1,
            "menu": 1
        }
        
        # Кэш для каналов
        self._channels_cache = []
        
    def _get_channels(self):
        """Получение списка каналов с кэшированием"""
        # Проверяем, изменилось ли количество каналов
        current_num_channels = pygame.mixer.get_num_channels()
        if len(self._channels_cache) != current_num_channels:
            # Обновляем кэш каналов
            self._channels_cache = [pygame.mixer.Channel(i) for i in range(current_num_channels)]
        return self._channels_cache
        
    def _load_sound(self, sound_name):
        """Ленивая загрузка звука по имени"""
        # Проверяем, нужно ли освободить место в кэше
        self._manage_cache()
        
        if sound_name not in self.sounds:
            sound_path = os.path.join(self.assets_dir, f"{sound_name}.wav")
            if os.path.exists(sound_path):
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                self.last_used[sound_name] = time.time()
            else:
                self.sounds[sound_name] = None
                
        # Обновляем время последнего использования
        if self.sounds[sound_name]:
            self.last_used[sound_name] = time.time()
            
        return self.sounds[sound_name]
        
    def _manage_cache(self):
        """Управление кэшем звуков для предотвращения переполнения"""
        if len(self.sounds) >= self.max_cache_size:
            # Находим звуки с наименьшим приоритетом и самым старым временем использования
            sounds_to_remove = sorted(
                [name for name in self.sounds.keys() if name in self.last_used],
                key=lambda x: (self.sound_priorities.get(x, 0), -self.last_used.get(x, 0))
            )[:len(self.sounds) - self.max_cache_size + 1]
            
            for sound_name in sounds_to_remove:
                if sound_name in self.sounds:
                    del self.sounds[sound_name]
                if sound_name in self.last_used:
                    del self.last_used[sound_name]
        
    def _get_sound(self, sound_name):
        """Получение звука с ленивой загрузкой"""
        # Проверяем, не истекло ли время жизни звука
        if sound_name in self.last_used:
            if time.time() - self.last_used[sound_name] > self.sound_ttl:
                # Звук устарел, удаляем его из кэша
                if sound_name in self.sounds:
                    del self.sounds[sound_name]
                if sound_name in self.last_used:
                    del self.last_used[sound_name]
                    
        # Загружаем звук, если он еще не загружен
        return self._load_sound(sound_name)
        
    def play_music(self, loops=-1):
        music_sound = self._get_sound("music")
        if music_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            music_sound.set_volume(self.music_volume)
            music_sound.play(loops)

    def play_menu_music(self, loops=-1):
        """Воспроизведение музыки меню"""
        menu_sound = self._get_sound("menu")
        if menu_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            menu_sound.set_volume(self.music_volume)
            menu_sound.play(loops)

    def stop_music(self):
        music_sound = self._get_sound("music")
        if music_sound:
            music_sound.stop()

    def stop_menu_music(self):
        """Остановка музыки меню"""
        menu_sound = self._get_sound("menu")
        if menu_sound:
            menu_sound.stop()

    def stop_all_music(self):
        """Остановка всей музыки"""
        self.stop_music()
        self.stop_menu_music()

    def set_music_volume(self, volume):
        # Ограничиваем значение между 0 и 1
        volume = max(0, min(1, volume))
        # Округляем до 2 знаков после запятой
        self.music_volume = round(volume, 2)
        
        # Устанавливаем громкость для всех музыкальных звуков
        music_sound = self._get_sound("music")
        menu_sound = self._get_sound("menu")
        
        if music_sound:
            music_sound.set_volume(self.music_volume)
        if menu_sound:
            menu_sound.set_volume(self.music_volume)
            
        # Сохраняем настройку, если есть SettingsManager
        if self.settings_manager:
            self.settings_manager.set("music_volume", self.music_volume)

    def set_sfx_volume(self, volume):
        # Ограничиваем значение между 0 и 1
        volume = max(0, min(1, volume))
        # Округляем до 2 знаков после запятой
        self.sfx_volume = round(volume, 2)
        
        # Устанавливаем громкость для всех SFX звуков
        shoot_sound = self._get_sound("shoot")
        explosion_sound = self._get_sound("explosion")
        
        if shoot_sound:
            shoot_sound.set_volume(self.sfx_volume)
        if explosion_sound:
            explosion_sound.set_volume(self.sfx_volume)
            
        # Сохраняем настройку, если есть SettingsManager
        if self.settings_manager:
            self.settings_manager.set("sfx_volume", self.sfx_volume)

    def get_music_volume(self):
        return self.music_volume

    def play_shoot(self):
        shoot_sound = self._get_sound("shoot")
        if shoot_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            shoot_sound.set_volume(self.sfx_volume)
            
            # Проверяем, не превышено ли максимальное количество одновременных воспроизведений
            max_playbacks = self.max_concurrent_playbacks.get("shoot", 5)
            
            # Используем pygame mixer для воспроизведения с ограничением
            if pygame.mixer.get_busy():
                # Если все каналы заняты, пытаемся остановить самый старый звук выстрела
                channels = self._get_channels()
                shoot_channels = [ch for ch in channels if ch.get_sound() == shoot_sound]
                
                if len(shoot_channels) >= max_playbacks:
                    # Останавливаем самый старый канал
                    shoot_channels[0].stop()
                    
            # Воспроизводим звук
            shoot_sound.play()

    def play_explosion(self):
        explosion_sound = self._get_sound("explosion")
        if explosion_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            explosion_sound.set_volume(self.sfx_volume)
            
            # Для звука взрыва используем отдельный подход - пытаемся прервать менее важные звуки
            channels = self._get_channels()
            
            # Ищем свободный канал
            free_channel = None
            for channel in channels:
                if not channel.get_busy():
                    free_channel = channel
                    break
                    
            # Если нет свободных каналов, пытаемся остановить звуки с меньшим приоритетом
            if free_channel is None:
                for channel in channels:
                    current_sound = channel.get_sound()
                    if current_sound:
                        # Проверяем приоритет текущего звука
                        current_priority = 0
                        for name, sound in self.sounds.items():
                            if sound == current_sound:
                                current_priority = self.sound_priorities.get(name, 0)
                                break
                                
                        # Если приоритет текущего звука меньше, чем у взрыва, останавливаем его
                        if current_priority < self.sound_priorities.get("explosion", 9):
                            channel.stop()
                            free_channel = channel
                            break
                            
            # Если нашли канал (свободный или освободили), воспроизводим звук
            if free_channel:
                free_channel.set_volume(self.sfx_volume)
                free_channel.play(explosion_sound)
            else:
                # Если все еще нет свободных каналов, воспроизводим на основном mixer
                explosion_sound.play()
            
    def cleanup_unused_sounds(self):
        """Очистка неиспользуемых звуков из кэша"""
        current_time = time.time()
        expired_sounds = []
        
        for sound_name, last_used_time in self.last_used.items():
            if current_time - last_used_time > self.sound_ttl:
                expired_sounds.append(sound_name)
                
        for sound_name in expired_sounds:
            if sound_name in self.sounds:
                del self.sounds[sound_name]
            if sound_name in self.last_used:
                del self.last_used[sound_name]
                
    def get_cache_stats(self):
        """Получение статистики кэша звуков"""
        return {
            "cached_sounds": len(self.sounds),
            "last_used_entries": len(self.last_used),
            "sound_ttl": self.sound_ttl,
            "max_cache_size": self.max_cache_size
        }
        
    def set_sound_priority(self, sound_name, priority):
        """Установка приоритета для звука"""
        self.sound_priorities[sound_name] = priority
        
    def get_sound_priority(self, sound_name):
        """Получение приоритета звука"""
        return self.sound_priorities.get(sound_name, 0)