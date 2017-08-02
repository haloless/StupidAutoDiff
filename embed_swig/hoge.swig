%module hoge

%include "carrays.i"

%include "std_vector.i"
%include "std_string.i"


%{
#include "hoge.h"
%}


%array_class(int, IntArray)
%array_class(double, DoubleArray)
%array_class(Vector3d, Vector3dArray)






// grab the whole header
%include "hoge.h"


