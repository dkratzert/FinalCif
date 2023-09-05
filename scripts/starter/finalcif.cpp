#include <iostream>
#include <cstdlib>
#include <windows.h>
#include "finalcif.h"

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

int main(int argc, char* argv[]) {

	cout << "Starting FinalCif..." << endl;

	char current_dir[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, current_dir);

	char current_executable_filepath[MAX_PATH];
	DWORD len = GetModuleFileName(NULL, current_executable_filepath, MAX_PATH);
	string parent_dir = getParentDirectory(current_executable_filepath);
	// Not good, because ShelXle wants to start it from the res file directory:
	// SetCurrentDirectory(parent_dir.c_str());

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

	WinExec(command.c_str(), SW_HIDE);
	
	return 0;
}



