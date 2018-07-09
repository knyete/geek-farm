"""App."""
import picoweb

from geek_farm import models


class GeekFarmApp(picoweb.WebApp):  # pylint: disable=too-few-public-methods
    """Geek Farm App."""

    def init(self):
        models.db.connect()
        models.WelcomeModel.create_table(True)
        super().init()


APP = GeekFarmApp(__name__)
