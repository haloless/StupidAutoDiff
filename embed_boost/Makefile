
# usually looks like -I/usr/include/python2.7
CFLAGS = $(shell pkg-config --cflags python2)

# usually looks like -lpython2.7
LIBS = $(shell pkg-config --libs python2)
LIBS += -lboost_python -lboost_numpy

hoge: hoge.cpp hoge.h
	g++ $(CFLAGS) hoge.cpp $(LIBS)




