#define PY_SSIZE_T_CLEAN
#define _SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING

#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdlib>
#include <locale>
#include <format>
#include <codecvt>
#include <windows.h>
#include "finalcif.h"
#include <Python.h>


using namespace std;


std::string getParentDirectory(const std::string& filePath) {
    size_t found = filePath.find_last_of("/\\");
    if (found != std::string::npos) {
        return filePath.substr(0, found);
    }
    // No parent directory found or empty string if already in root
    return "";
}


std::string to_utf8(const std::wstring& wstr) {
    std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> converter;
    return converter.to_bytes(wstr);
}

int wmain(int argc, wchar_t* argv[]) {

    cout << "Starting FinalCif..." << endl;

    // This dir may not be the path of the Python installation!
    char current_dir[MAX_PATH];
    GetCurrentDirectory(MAX_PATH, current_dir);

    char current_executable_filepath[MAX_PATH];
    DWORD len = GetModuleFileName(NULL, current_executable_filepath, MAX_PATH);
    string parent_dir = getParentDirectory(current_executable_filepath);
    // Not good, because ShelXle wants to start it from the res file directory:
    // SetCurrentDirectory(parent_dir.c_str());

    wchar_t* program = Py_DecodeLocale(to_utf8(argv[0]).c_str(), NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    string runscript_path = parent_dir + "/finalcif/finalcif_start.py";

    FILE* fp = fopen(runscript_path.c_str(), "rb");
    if (fp == NULL)
    {
        cout << "Error opening file: " << runscript_path << endl;
        exit(1);
    }

    Py_Initialize();
   
    // Add the first argument to the arglist first:
    if (argc > 1) {
        string arg_command = format("import sys\nsys.argv.append(r'{}')", to_utf8(argv[1]));
        PyRun_SimpleString(arg_command.c_str());
    }

    // Then execute the python script:
    PyRun_SimpleFileEx(fp, runscript_path.c_str(), true);

    if (Py_FinalizeEx() < 0) {
        exit(1);
    }

    PyMem_RawFree(program);

    return 0;
}



