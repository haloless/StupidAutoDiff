
PYINCDIR ?= /usr/include/python2.7

PYLIB ?= -lpython2.7

.PHONY: help
help:
	@echo "Usage: make hoge etc."

# NOTE remember to set PYTHONPATH otherwise do not work
.PHONY: hoge
hoge:
	# swig -c++ -python hoge.swig
	g++ -I$(PYINCDIR) -c hoge.cpp
	g++ -I$(PYINCDIR) -c hoge_wrap.cxx
	g++ -I$(PYINCDIR) -c hoge_main.cpp
	g++ -o $@ hoge.o hoge_wrap.o hoge_main.o $(PYLIB)

.PHONY: test
test: hoge
	./hoge.exe test.py

