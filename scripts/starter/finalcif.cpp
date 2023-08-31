#include <iostream>
#include <cstdlib>

#ifdef _WIN32
    #include <windows.h>
#endif


int main() {
    std::cout << "Starting FinalCif..." << std::endl;
#ifdef _WIN32
    _putenv_s("PYTHONPATH", ".");
    HWND hWnd = GetConsoleWindow();
    ShowWindow(hWnd, SW_HIDE);  // Hide the console window
#else
    setenv("PYTHONPATH", ".", 1);
#endif
    std::system("venv\\Scripts\\pythonw finalcif/finalcif_start.py");
    return 0;
}



