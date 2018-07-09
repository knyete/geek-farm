"""Welcome View."""
import gc
import picoweb

from geek_farm import models
from geek_farm.app import APP
from geek_farm.utils import get_info
from geek_farm.utils import wifi_scan
from geek_farm.utils import is_first_time
from geek_farm.utils import connect_wifi
from geek_farm.utils import disconnect


@APP.route("/")
def welcome(req, res):
    """welcome view."""
    if req.method == "POST":
        yield from req.read_form_data()
        print("postadooo")
        print(req.form)
        connect_wifi(req.form['ssid'][0], req.form['password'][0])
        gc.collect()
    info = get_info()
    stations = wifi_scan()
    gc.collect()
    # if not is_first_time():
    #     welcomeid = models.WelcomeModel.create(firsttime=1)
    #     print("Criado: ", welcomeid)
    # else:
    #     print("Ja nao precisa exibir umas informacoes.")
    yield picoweb.start_response(res)
    yield APP.render_template(res, "base.html", (info,))
    yield APP.render_template(res, "welcome.html", (stations,))
    yield APP.render_template(res, "end.html", ())

@APP.route("/disconnect")
def disconnect_network(req, res):
    """disconnect network view."""
    disconnect()
    gc.collect()
    yield from res.awrite("HTTP/1.0 301 Moved Permanently\r\n")
    yield from res.awrite("Location: /\r\n")
    yield from res.awrite("Content-Type: text/html\r\n")
    yield from res.awrite("<html><head><title>Moved</title></head><body><h1>Moved</h1></body></html>\r\n")