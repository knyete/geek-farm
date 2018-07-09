"""Welcome View."""
import picoweb

from geek_farm import models
from geek_farm.app import APP
from geek_farm.utils import get_info
from geek_farm.utils import wifi_scan
from geek_farm.utils import is_first_time
from geek_farm.utils import connect_wifi


@APP.route("/")
def welcome(req, res):
    """welcome view."""
    if req.method == "POST":
        yield from req.read_form_data()
        print("postadooo")
        print(req.form)
        connect_wifi(req.form['ssid'][0], req.form['password'][0])
    info = get_info()
    stations = wifi_scan()
    # if not is_first_time():
    #     welcomeid = models.WelcomeModel.create(firsttime=1)
    #     print("Criado: ", welcomeid)
    # else:
    #     print("Ja nao precisa exibir umas informacoes.")
    yield picoweb.start_response(res)
    yield APP.render_template(res, "base.html", (info,))
    yield APP.render_template(res, "welcome.html", (stations,))
    yield APP.render_template(res, "end.html", ())

