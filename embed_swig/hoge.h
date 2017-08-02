#pragma once

#include <vector>
#include <string>



/// global variable
extern double MyVar;

int myFact(int n);

int myMod(int x, int y);

char* myTime();


///
struct Vector3d
{
	double x, y, z;
};


struct BigData
{
	int n;
	
	int *iarr;
	double *darr;
	Vector3d *varr;
};	

///
void allocBigData(int n);
void freeBigData();


///
BigData* getBigData();




