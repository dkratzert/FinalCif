#include <iostream>
#include <cstdlib>
using namespace std;

#ifdef _WIN32
#include <windows.h>
#include "finalcif.h"
#endif


int main(int argc, char* argv[]) {
	
	cout << "Starting FinalCif..." << endl;

#ifdef _WIN32
	_putenv_s("PYTHONPATH", ".");

	bool hide = true;
	for (int i = 1; i < argc; ++i) {
		if (strcmp(argv[i], "-nohide") == 0) {
			hide = false;
			argv[i] = "";
			break;
		}
	}
	if (hide) {
		HWND hWnd = GetConsoleWindow();
		ShowWindow(hWnd, SW_HIDE);  // Hide the console window
	}
#else
	setenv("PYTHONPATH", ".", 1);
#endif
	string command = "venv\\Scripts\\pythonw finalcif/finalcif_start.py";
	add_argvalues(command, argc, argv);
	// cout << command << endl;
	system(command.c_str());
	return 0;
}

void add_argvalues(string& command, int argc, char* argv[])
{
	for (int i = 1; i < argc; ++i) {
		command += " ";
		command += argv[i];
	}
}



