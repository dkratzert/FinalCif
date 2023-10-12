#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <windows.h>
#include "finalcif.h"
#define PY_SSIZE_T_CLEAN
#include <Python.h>

using namespace std;


void add_argvalues(string& command, int argc, char* argv[])
{
	for (int i = 1; i < argc; ++i) {
		command += " ";
		command += argv[i];
	}
}


std::string getParentDirectory(const std::string& filePath) {
	size_t found = filePath.find_last_of("/\\");
	if (found != std::string::npos) {
		return filePath.substr(0, found);
	}
	// No parent directory found or empty string if already in root
	return "";
}


void hide_console_window()
{
	HWND hWnd = GetConsoleWindow();
	ShowWindow(hWnd, SW_HIDE);
}

void should_window_hide(int argc, char* argv[], bool& hide)
{
	for (int i = 1; i < argc; ++i) {
		if (strcmp(argv[i], "-nohide") == 0) {
			hide = false;
			argv[i] = "";
			break;
		}
	}
}

void run_from_commandline(int argc, char* argv[], std::string& parent_dir, char  current_dir[260])
{
	bool hide = true;
	should_window_hide(argc, argv, hide);
	if (hide) {
		hide_console_window();
	}

	string command = "\"" + parent_dir + "\\python.exe" + "\" \"" + parent_dir + "\\finalcif\\finalcif_start.py\"";
	add_argvalues(command, argc, argv);
	if (!hide) {
		cout << "Running command: '" << command.c_str() << "' Inside of: " << std::string(current_dir) << endl;
	}

	WinExec(command.c_str(), SW_SHOW);
}

std::string readFileIntoString(const std::string& path) {
	std::ifstream fileStream(path);
	cout << path << endl;;
	if (!fileStream) {
		std::cerr << "Datei konnte nicht geöffnet werden: " << path << std::endl;
		return "";
	}

	std::stringstream stringStream;
	stringStream << fileStream.rdbuf();

	return stringStream.str();
}

int main(int argc, char* argv[]) {

	//cout << "Starting FinalCif..." << endl;

	// This dir may not be the path of the Python installation!
	char current_dir[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, current_dir);

	char current_executable_filepath[MAX_PATH];
	DWORD len = GetModuleFileName(NULL, current_executable_filepath, MAX_PATH);
	string parent_dir = getParentDirectory(current_executable_filepath);
	// Not good, because ShelXle wants to start it from the res file directory:
	// SetCurrentDirectory(parent_dir.c_str());

	//run_from_commandline(argc, argv, parent_dir, current_dir);

	wchar_t* program = Py_DecodeLocale(argv[0], NULL);
	if (program == NULL) {
		fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
		exit(1);
	}
	string runscript = readFileIntoString(parent_dir + "/finalcif/finalcif_start.py");
	Py_Initialize();
	if (argc > 1) {
		string arg_command = string("import sys\nsys.argv.append(r'") + argv[1] + "')";
		PyRun_SimpleString(arg_command.c_str());
	}
	PyRun_SimpleString(runscript.c_str());
	if (Py_FinalizeEx() < 0) {
		exit(-1);
	}
	PyMem_RawFree(program);
	
	return 0;
}



