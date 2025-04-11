import os
import importlib

def load_module(loader, module_path):
    try:
        module_name = os.path.basename(module_path)[:-3]
        
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        loaded_package_name = os.path.basename(project_dir) + '.loaded_modules'
        full_module_name = f"{loaded_package_name}.{module_name}"
        
        module = importlib.import_module(full_module_name)
        
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, type) and issubclass(item, loader.Module):
                _register_module(loader, item)
                return True
            elif isinstance(item, type):
                print(f"Класс {item.__name__} в модуле {module_name} не наследуется от loader.Module и не будет загружен")
        
        return False
    except Exception as e:
        print(f"Ошибка при загрузке модуля: {e}")
        return False

def register_and_load_modules(loader):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modules_dir = os.path.join(project_dir, 'modules')
    loaded_modules_dir = os.path.join(project_dir, 'loaded_modules')

    package_name = os.path.basename(project_dir) + '.modules'
    loaded_package_name = os.path.basename(project_dir) + '.loaded_modules'

    loaded_modules = []

    try:
        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                full_module_name = f"{package_name}.{module_name}"
                try:
                    module = importlib.import_module(full_module_name)
                    
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, loader.Module):
                            _register_module(loader, item)
                            loaded_modules.append(module_name)
                        elif isinstance(item, type):
                            print(f"Класс {item.__name__} в модуле {module_name} не наследуется от loader.Module и не будет загружен")
                except Exception as e:
                    print(f"Ошибка при загрузке модуля {module_name}: {e}")

        for filename in os.listdir(loaded_modules_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                full_module_name = f"{loaded_package_name}.{module_name}"
                try:
                    module = importlib.import_module(full_module_name)
                    
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, loader.Module):
                            _register_module(loader, item)
                            loaded_modules.append(module_name)
                        elif isinstance(item, type):
                            print(f"Класс {item.__name__} в модуле {module_name} не наследуется от loader.Module и не будет загружен")
                except Exception as e:
                    print(f"Ошибка при загрузке модуля {module_name}: {e}")
    except Exception as e:
        print(f"Ошибка при работе с пакетами: {e}")

    print("Загруженные модули:")
    for module in loaded_modules:
        print(module)

def _register_module(loader, module):
    if isinstance(module, type) and issubclass(module, loader.Module):
        loader.modules[module.__name__] = {"module": module, "type": "module", "commands": []}
        
        for item_name in dir(module):
            item = getattr(module, item_name)
            if callable(item) and hasattr(item, '__name__') and item.__name__.endswith('cmd'):
                loader.modules[module.__name__]["commands"].append(item.__name__.removesuffix('cmd'))
    else:
        print(f"Модуль {module.__name__} не наследуется от loader.Module и не будет загружен")

async def answer(message, text, parse_mode="HTML"):
    await message.edit(text, parse_mode=parse_mode)