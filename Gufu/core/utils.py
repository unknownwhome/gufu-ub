import os
import importlib
import sys

from .exceptions.modules import ModuleNotInheritedError

def get_args_raw(message):
    if not message.text:
        return ""
    
    parts = message.text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ""


def unload_module(loader, module_name: str) -> str:
    if module_name in loader.userbot_modules:
        return "❌ Нельзя удалить системный модуль"

    module_info = loader.modules.get(module_name)
    if not module_info:
        return f"❌ Модуль <code>{module_name}</code> не найден среди загруженных модулей"

    module_class = module_info.get("module")

    full_module_name = module_class.__module__

    spec = importlib.util.find_spec(full_module_name)
    module_file_path = spec.origin

    try:
        os.remove(module_file_path)
    except Exception as e:
        return f"❌ Ошибка при удалении файла модуля: {e}"

    if full_module_name in sys.modules:
        del sys.modules[full_module_name]

    del loader.modules[module_name]

    return f"Модуль <code>{module_name}</code> успешно выгружен"

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
                        return _register_module(loader, item, is_userbot=False)
                except Exception as e:
                    print(f"❌ Ошибка при регистрации модуля {item.__name__}: {e}")
            elif isinstance(item, type):
                raise ModuleNotInheritedError(module_name, item.__name__)
        
        return None, None
    except Exception as e:
        print(f"❌ Ошибка при загрузке модуля: {e}")
        return None, None


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
                            try:
                                _register_module(loader, item, is_userbot=True)
                                loaded_modules.append(item.__name__)
                            except Exception as e:
                                print(f"Ошибка при регистрации модуля {item.__name__}: {e}")
                except Exception as e:
                    print(e)
        
        for filename in os.listdir(loaded_modules_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                full_module_name = f"{loaded_package_name}.{module_name}"
                try:
                    module = importlib.import_module(full_module_name)
                    
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, loader.Module):
                            try:
                                _register_module(loader, item, is_userbot=False)
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


def _register_module(loader, module, is_userbot=True):
    if _check_module(loader, module):
        target_dict = loader.userbot_modules if is_userbot else loader.modules
        instance = module()

        target_dict[module.__name__] = {
            "module": module,
            "instance": instance,
            "type": "userbot_module" if is_userbot else "module",
            "commands": []
        }

        commands = []
        for item_name in dir(module):
            item = getattr(module, item_name)
            if callable(item) and hasattr(item, '__name__') and item.__name__.endswith('cmd'):
                cmd_name = item.__name__.removesuffix('cmd')
                target_dict[module.__name__]["commands"].append(cmd_name)
                if item.__doc__:
                    commands.append(f"{cmd_name} | {item.__doc__}")
                else:
                    commands.append(f"{cmd_name}")

        return module.__name__, commands
    return None, None



async def answer(message, text, parse_mode="HTML"):
    if isinstance(text, dict):
        response_text = ""
        for key, value in text.items():
            response_text += f"<b>{key}: </b>{value}\n"
        await message.edit(response_text, parse_mode=parse_mode)
    else:
        await message.edit(text, parse_mode=parse_mode)

async def send_file(message, file, caption=None, parse_mode="HTML", **kwargs):
    if isinstance(caption, dict):
        response_text = ""
        for key, value in caption.items():
            response_text += f"<b>{key}: </b>{value}\n"
        caption = response_text

    await message.client.send_file(
        message.chat_id,
        file,
        caption=caption,
        parse_mode=parse_mode,
        **kwargs
    )
