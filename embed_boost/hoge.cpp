
#include <cstdlib>

#include <iostream>
#include <string>

//
// #define BOOST_PYTHON_STATIC_LIB
// #define BOOST_LIB_DIAGNOSTIC
// #define BOOST_LIB_TOOLSET "vc100"

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

// #define BOOST_LIB_NAME boost_numpy
// #include <boost/config/auto_link.hpp>



namespace py = boost::python;
namespace np = boost::python::numpy;

//
typedef py::return_internal_reference<>                                PyReturnInternalRef;
typedef py::return_self<>                                              PyReturnSelf;
typedef py::return_value_policy<py::reference_existing_object>         PyReturnExistingObj;
typedef py::return_value_policy<py::copy_non_const_reference>          PyReturnCopyRef;
typedef py::return_value_policy<py::copy_const_reference>              PyReturnCopyConstRef;
typedef py::return_value_policy<py::return_opaque_pointer>             PyReturnWrapPointer;
typedef py::return_value_policy<py::return_by_value>                   PyReturnByValue;
typedef py::return_value_policy<py::manage_new_object>                 PyReturnNewObj;



//
#include "hoge.h"




std::string hello_to(const std::string &name) {
	return ("Hello to " + name);
}

void greet() {
	std::cout << "hello you" << std::endl;
}


// std::ostream& operator<<(std::ostream &os, const Vector3d &vec) {
	// os << "Vector3d(" << vec.x << "," << vec.y << "," << vec.z << ")";
	// return os;
// }




// int BigDataGetInt(BigData &self, int idx) {
	// return self.iarr[idx];
// }
// void BigDataSetInt(BigData &self, int idx, int val) {
	// self.iarr[idx] = val;
// }

// double BigDataGetDouble(BigData &self, int idx) {
	// return self.darr[idx];
// }
// void BigDataSetDouble(BigData &self, int idx, double val) {
	// self.darr[idx] = val;
// }

// Vector3d& BigDataGetVec(BigData &self, int idx) {
	// return self.varr[idx];
// } 


// np::ndarray BigDataIntArray(BigData &self) {
	// const int nlen = self.n;
	// np::ndarray pyarr = np::from_data(self.iarr, 
		// np::dtype::get_builtin<int>(),
		// py::make_tuple(nlen),
		// py::make_tuple(sizeof(self.iarr[0])),
		// py::object());
	// return pyarr;
// }

// np::ndarray BigDataDoubleArray(BigData &self) {
	// const int nlen = self.n;
	// np::ndarray pyarr = np::from_data(self.darr, 
		// np::dtype::get_builtin<double>(),
		// py::make_tuple(nlen),
		// py::make_tuple(sizeof(self.darr[0])),
		// py::object());
	// return pyarr;
// }

// np::ndarray BigDataVector3dArray(BigData &self) {
	// const int nlen = self.n;
	// np::ndarray pyarr = np::from_data(self.varr, 
		// np::dtype::get_builtin<double>(),
		// py::make_tuple(nlen,3),
		// py::make_tuple(sizeof(Vector3d),sizeof(double)),
		// py::object());
	// return pyarr;
// }




/**Define the cpp module.
 * 
 * It defines an initialization function 
 */
BOOST_PYTHON_MODULE(mymod)
{
	//
	// some tests
	//
	py::def("greet", greet);
	py::def("hello_to", hello_to);

	//
	//
	//
	// py::class_<Vector3d>("Vector3d")
		// .def_readwrite("x", &Vector3d::x)
		// .def_readwrite("y", &Vector3d::y)
		// .def_readwrite("z", &Vector3d::z)
		// .def(py::self_ns::str(py::self_ns::self))
		// ;

	//
	// big data
	//

	// py::class_<BigData>("BigData")
		// .def_readonly("n", &BigData::n)
		// .def("iarr", BigDataGetInt/*, PyReturnCopyRef()*/)
		// .def("darr", BigDataGetDouble/*, PyReturnCopyRef()*/)
		// .def("varr", BigDataGetVec, PyReturnInternalRef())
		// .def("intArray", BigDataIntArray)
		// .def("vecArray", BigDataVector3dArray)
		// ;

	// singleton method
	// py::def("getBigData", getBigData, PyReturnExistingObj());
	


}





int main(int argc, char *argv[]) {
	
	std::cout << "hello boost" << std::endl;

	// c initialize
	{
		// allocBigData(50);
	}

	try {

		//
		Py_SetProgramName(argv[0]);
		std::cout << "program name = " << argv[0] << std::endl;

		// set python home, important!!!
		if (0) {
			char pyhome[] = "C:\\Users\\sun\\Anaconda2";
			//char pyhome[] = ".";
			Py_SetPythonHome(pyhome);
			std::cout << "PythonHome=" << pyhome << std::endl;
		}

		// python core bootstrap
		Py_Initialize();

		if (!Py_IsInitialized()) {
			std::cout << "Py_Initialize failed" << std::endl;
			exit(1);
		} else {
			std::cout << "Py_Initialize" << std::endl;

			PyRun_SimpleString("import sys; print(sys.version)");
		}

		py::numpy::initialize();
		{
			PyRun_SimpleString("import numpy as np; print(np.__config__)");
		}

		if (0) {
			py::object main_module(py::handle<>(py::borrowed(PyImport_AddModule("__main__"))));

			py::object main_namespace = main_module.attr("__dict__");

			py::handle<> ignored(PyRun_String(
				"print('Hello world')", 
				Py_file_input, 
				main_namespace.ptr(),
				main_namespace.ptr()));
		} else {
			py::object main_module = py::import("__main__");

			py::object main_ns = main_module.attr("__dict__");

			py::exec("print('Hello world2')", main_ns, main_ns);
		}

		{
			initmymod();

			PyRun_SimpleString("import mymod");
			PyRun_SimpleString("mymod.greet()");
			PyRun_SimpleString("print(mymod.hello_to('homu'))");
		}

		// exec files
		// we can use methods/data provided by MYMOD
		for (int i=1; i<argc; i++) {
			py::object main_module = py::import("__main__");

			py::object main_ns = main_module.attr("__dict__");

			py::exec_file(argv[i], main_ns, main_ns);
		}


		// python close
		Py_Finalize();

	} catch (py::error_already_set const &pyerr) {
		PyErr_Print();
		PyErr_Clear();
	} catch (std::exception const &e) {
		std::cerr << e.what() << std::endl;
	} catch (...) {
		std::cerr << "Something wrong!!!" << std::endl;
	}

	{
		// std::cout << "Finally" << std::endl;
		// std::cout << getBigData()->varr[0] << std::endl;
	}


	// c finalize
	{
		// freeBigData();
	}


	return 0;
}







