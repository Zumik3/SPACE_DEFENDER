class EventManager:
    """Класс для управления событиями и реализации паттерна Observer"""
    
    def __init__(self):
        self.listeners = {}
        
    def subscribe(self, event_type, listener):
        """Подписка на события определенного типа"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
        
    def unsubscribe(self, event_type, listener):
        """Отписка от событий определенного типа"""
        if event_type in self.listeners:
            if listener in self.listeners[event_type]:
                self.listeners[event_type].remove(listener)
                
    def notify(self, event_type, data=None):
        """Уведомление всех подписчиков о событии"""
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(event_type, data)
                
    def clear(self):
        """Очистка всех подписчиков"""
        self.listeners.clear()