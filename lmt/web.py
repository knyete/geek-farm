import picoweb

class LabMetApp(picoweb.WebApp):

    def init(self):
        super().init()

app = LabMetApp(__name__)

@app.route("/api/v1", methods=['GET'])
def home(request, response):
    yield from picoweb.jsonify(response, {"message":"i love you ;-)", "version": "0.1"})
    return