class RenderComponent:
    """Базовый класс для компонентов отрисовки"""
    def __init__(self, renderer):
        self.renderer = renderer
        
    def draw(self, entity):
        """Метод отрисовки сущности"""
        pass