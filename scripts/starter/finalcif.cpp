#include <stdio.h>
#include <conio.h>
#include <Python.h>

int main()
{
	char filename[] = ("finalcif/finalcif_start.py");

	FILE* fp;

	Py_Initialize();

	//fp = _Py_fopen(filename, "r");
	//PyRun_SimpleFile(fp, filename);
	PyRun_SimpleString("from time import time,ctime\n"
		"print('Today is', ctime(time()))\n");

	Py_Finalize();
	return 0;
}