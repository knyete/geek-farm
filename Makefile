TARGET = unix

.PHONY: lib mpy

all:

clean-htmlpy:
	find . | grep -E "(\_html\.py$\)" | xargs rm -rf

requirements: requirements.txt
	micropython -m upip install -p lib -r requirements.txt

run:
	MICROPYPATH=lib micropython -X heapsize=150wK -m geek_farm

res:
	cd geek_farm; mpy_bin2res.py static/css/styles.css static/img/logo.jpg >R.py

mpy:
	mpy_cross_all.py geek_farm -o mpy/geek_farm --target=$(TARGET)
	mpy_cross_all.py lib -o mpy/lib --target=$(TARGET)
	cp -r geek_farm/static mpy/geek_farm

run-mpy:
	cd mpy; MICROPYPATH=lib micropython -X heapsize=50wK -m geek_farm

clean:
	rm -rf lib mpy

