import os
import importlib
import sys

from .exceptions.modules import ModuleNotInheritedError

def load_module(loader, module_path):
    try:
        module_name = os.path.basename(module_path)[:-3]
        
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        loaded_package_name = os.path.basename(project_dir) + '.loaded_modules'
        full_module_name = f"{loaded_package_name}.{module_name}"
        
        package_dir = os.path.join(os.path.dirname(module_path), '__init__.py')
        if not os.path.exists(package_dir):
            with open(package_dir, 'w') as f:
                f.write('')
        
        sys.path.insert(0, os.path.dirname(os.path.dirname(module_path)))
        
        module = importlib.import_module(full_module_name)
        
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, type) and issubclass(item, loader.Module):
                try:
                    if _check_module(loader, item):
                        _register_module(loader, item)
                        return True
                except Exception as e:
                    print(f"Ошибка при регистрации модуля {item.__name__}: {e}")
            elif isinstance(item, type):
                raise ModuleNotInheritedError(module_name, item.__name__)
        
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
        for dir_path in [modules_dir, loaded_modules_dir]:
            for filename in os.listdir(dir_path):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    full_module_name = f"{package_name}.{module_name}" if dir_path == modules_dir else f"{loaded_package_name}.{module_name}"
                    try:
                        module = importlib.import_module(full_module_name)
                        
                        for item_name in dir(module):
                            item = getattr(module, item_name)
                            if isinstance(item, type) and issubclass(item, loader.Module):
                                try:
                                    _register_module(loader, item)
                                    loaded_modules.append(item.__name__)
                                except Exception as e:
                                    print(f"Ошибка при регистрации модуля {item.__name__}: {e}")
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)

    print("Загруженные модули:")
    for module in loaded_modules:
        print(module)


def _check_module(loader, module):
    if not issubclass(module, loader.Module):
        raise ModuleNotInheritedError(module.__name__, module.__name__)
    
    for item_name in dir(module):
        item = getattr(module, item_name)
        if callable(item) and hasattr(item, '__name__') and item.__name__.endswith('cmd'):
            original_func = getattr(item, '__wrapped__', item)
            if not (hasattr(original_func, '__self__') or 
                    (original_func.__code__.co_argcount > 0 and original_func.__code__.co_varnames[0] == 'self')):
                raise ValueError(f"Функция {item.__name__} должна иметь параметр 'self'")
    
    return True


def _register_module(loader, module):
    if _check_module(loader, module):
        loader.modules[module.__name__] = {"module": module, "type": "module", "commands": []}
        
        commands = []
        for item_name in dir(module):
            item = getattr(module, item_name)
            if callable(item) and hasattr(item, '__name__') and item.__name__.endswith('cmd'):
                loader.modules[module.__name__]["commands"].append(item.__name__.removesuffix('cmd'))
                commands.append(f"{item.__name__.removesuffix('cmd')} | {item.__doc__ or 'Описание команды не найдено'}")
        
        return module.__name__, commands
    return None, None

async def answer(message, text, parse_mode="HTML"):
    await message.edit(text, parse_mode=parse_mode)