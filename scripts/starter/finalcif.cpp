#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <windows.h>
#include <iostream>
#include <string>


void attach_console()
{
    if (AttachConsole(ATTACH_PARENT_PROCESS))
    {
        FILE* dummy;
        freopen_s(&dummy, "CONOUT$", "w", stdout);
        freopen_s(&dummy, "CONOUT$", "w", stderr);
        freopen_s(&dummy, "CONIN$", "r", stdin);
    }
}


std::string get_parent_dir(const std::string& path)
{
    size_t pos = path.find_last_of("\\/");
    if (pos == std::string::npos)
        return "";
    return path.substr(0, pos);
}

int wmain(int argc, wchar_t* argv[])
{
    attach_console();
    std::cout << "Starting FinalCif...\n";

    wchar_t exe_path[MAX_PATH];
    GetModuleFileNameW(NULL, exe_path, MAX_PATH);

    std::wstring exe_w(exe_path);
    std::string exe_utf8(Py_EncodeLocale(exe_w.c_str(), NULL));

    std::string parent = get_parent_dir(exe_utf8);
    std::string script = parent + "\\finalcif\\finalcif_start.py";

    Py_Initialize();

    // sys.argv setzen
    PyObject* sys = PyImport_ImportModule("sys");
    PyObject* argv_list = PyList_New(0);

    PyList_Append(argv_list, PyUnicode_FromString(script.c_str()));

    if (argc > 1) {
        char* arg = Py_EncodeLocale(argv[1], NULL);
        PyList_Append(argv_list, PyUnicode_FromString(arg));
        PyMem_RawFree(arg);
    }

    PyObject_SetAttrString(sys, "argv", argv_list);
    Py_DECREF(argv_list);
    Py_DECREF(sys);

    FILE* fp = fopen(script.c_str(), "rb");
    if (!fp) {
        std::cerr << "Cannot open script: " << script << "\n";
        return 1;
    }

    PyRun_SimpleFile(fp, script.c_str());
    fclose(fp);

    Py_Finalize();

    return 0;
}