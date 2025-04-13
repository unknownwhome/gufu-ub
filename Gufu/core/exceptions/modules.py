class ModuleNotInheritedError(Exception):
    """Если класс не наследуется от loader.Module"""
    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name
        super().__init__(f"Класс {class_name} в модуле {module_name} не наследуется от loader.Module")