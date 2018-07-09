"""Main."""
import gc

from geek_farm.app import APP
from geek_farm.views import welcome


def main(**params):
    """main"""
    import logging
    logging.basicConfig(level=logging.INFO)
    gc.collect()
    APP._load_template('welcome.html')
    gc.collect()

    import micropython
    micropython.mem_info()
    APP.run(debug=True, **params)

if __name__ == '__main__':
    main()
