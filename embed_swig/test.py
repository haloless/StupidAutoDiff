
import os, sys

print('In test.py')

print(sys.path)
# sys.path.append('.')


try:
    import hoge
except ImportError as e:
    print('Failed to import hoge module')
    print(e)
    sys.exit(1)
else:
    print('Imported module hoge')

#
# test hoge module
#

print('hoge.myTime')
print(hoge.myTime())

print('hoge.myFact')
print(hoge.myFact(5))

print('hoge.myvar=', hoge.cvar.MyVar)
hoge.cvar.MyVar = 30

v1 = hoge.Vector3d()
v1.x = 1
v1.y = 2
v1.z = 3
print(v1)


data = hoge.getBigData()
print('data.n=', data.n)
print(data.darr)
print(data.iarr)
print(data.varr)

iarr = hoge.IntArray_frompointer(data.iarr)
print(iarr[0])
iarr[0] = 1000

varr = hoge.Vector3dArray_frompointer(data.varr)
print(varr[10].x,varr[10].y,varr[10].z,)

