#include <iostream>
#include <cstdlib>

int main() {
    std::cout << "Starting FinalCif..." << std::endl;
    setenv("PYTHONPATH", ".", 1);
    std::system("python3 finalcif/finalcif_start.py");
    return 0;
}


