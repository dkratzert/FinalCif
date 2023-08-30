#include <iostream>
#include <cstdlib>
/*
For the windows icon:
windres -i icon.rc -o resource.o
g++ -o finalcif.exe finalcif.cpp resource.o
*/

#ifdef _WIN32
    #include <windows.h>
    #include "resource.h"
#endif

int main() {
    std::cout << "Starting FinalCif..." << std::endl;
    #ifdef _WIN32
        SetEnvironmentVariableA("PYTHONPATH", ".");
    #else
        setenv("PYTHONPATH", ".", 1);
    #endif
    std::system("python3 finalcif/finalcif_start.py");
    return 0;
}


