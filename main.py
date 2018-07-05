import gc

from lmt import shared
from lmt.start import Start
from lmt.web import app

def main():
    # auto collect garbage
    gc.enable()
    # Max 1/4 heap used: start auto collect
    gc.threshold((gc.mem_free() + gc.mem_alloc()) // 4)

    # start = Start()
    # s.run()

    while True:
        app.run(host='0.0.0.0', debug=True, log=shared._log)
        
if __name__ == '__main__':
    main()