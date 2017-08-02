
#include <ctime>

#include "hoge.h"

double MyVar = 3.0;

int myFact(int n) {
	int val = 1;
	for (int i=1; i<=n; i++) {
		val *= i;
	}
	return val;
}

int myMod(int x, int y) {
	return x % y;
}

char* myTime() {
	time_t ltime;
	time(&ltime);
	return ctime(&ltime);
}

///
/// instance 
static BigData *data = NULL;


void allocBigData(int n) {
	if (data) return;
	
	data = new BigData;
	
	data->n = n;
	
	data->iarr = new int[n];
	data->darr = new double[n];
	data->varr = new Vector3d[n];
	
	for (int i=0; i<n; i++) {
		data->iarr[i] = i;
		data->darr[i] = i;
		data->varr[i].x = i;
		data->varr[i].y = i;
		data->varr[i].z = i;
	}
}

void freeBigData() {
	if (!data) return;
	delete[] data->iarr;
	delete[] data->darr;
	delete[] data->varr;
	delete data;
	data = NULL;
}

BigData* getBigData() {
	return data;
}




