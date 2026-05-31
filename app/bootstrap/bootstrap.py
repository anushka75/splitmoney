from app.config import init_config, load_config
from app.services.db.service import setup as init_db_service


def bootstrap():
    config = load_config()
    init_config(config)
    init_db_service(config)
    return config
