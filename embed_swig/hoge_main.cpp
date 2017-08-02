
// must keep Python first
#include <Python.h>

#include <cstdio>
#include <cstdlib>

#include <iostream>
#include <string>

// c hoge
#include "hoge.h"

// python hoge
// init function copied from hoge_wrap.cxx
#if PY_VERSION_HEX >= 0x03000000
#  define SWIG_init    PyInit__hoge
#else
#  define SWIG_init    init_hoge
#endif
extern "C" void SWIG_init();

int simple_run(int argc, char *argv[]) {
    
    return 0;
}


void py_append_path(char modpath[]) {
    PyObject *sysmod = PyImport_ImportModule("sys");
    PyObject *syspath = PyObject_GetAttrString(sysmod, "path");
    PyList_Append(syspath, PyString_FromString(modpath));
}

int main(int argc, char *argv[]) {
    
	{
		const int nmax = 100;
		allocBigData(nmax);
	}
	
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    
    // set user module 
    {
        char modpath[256] = ".";
        
        // do not directly do this, which will clean the sys.path with ['.'] only
        // PySys_SetPath(modpath);
        
        py_append_path(modpath);
    }
    
	// load user module
	{
		SWIG_init();
	}
	
    {
        std::string script = 
        "from time import time, ctime\n"
        "print 'Today is', ctime(time())\n"
        ;
        PyRun_SimpleString(script.c_str());
    }
    
	if (argc > 1) {
		std::string pyfilename = argv[1];
		std::cout << "Begin run " << pyfilename << std::endl;
		
		FILE *fp = fopen(pyfilename.c_str(), "r");
		
		PyRun_SimpleFile(fp, pyfilename.c_str());
		
		fclose(fp);
		
		std::cout << "End run " << pyfilename << std::endl;
		
		std::cout << "MyVar = " << MyVar << std::endl;
		
		BigData* data = getBigData();
		std::cout << data->iarr[0] << std::endl;
	}
	
    Py_Finalize();
    
	{
		freeBigData();
	}
	
    return 0;
}

