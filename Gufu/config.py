import json

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_config(api_id, api_hash):
    config_data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "app_name": "Gofu UB"
    }
    
    with open('config.json', 'w') as f:
        json.dump(config_data, f, indent=4)


