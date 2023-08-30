#include <cstdlib>

int main() {
    // Replace "your_script.py" with the actual path to your Python script
    const char* pythonScriptPath = "finalcif\\finalcif_start.py";

    // Construct the command to run the Python script using the "python" command
    // If you're using Python 3, replace "python" with "python3"
    std::string command = "python " + std::string(pythonScriptPath);

    // Execute the Python script using the system() function
    int result = system(command.c_str());

    // Check the result of the system call
    if (result == 0) {
        std::cout << "Python script executed successfully." << std::endl;
    } else {
        std::cerr << "Error executing Python script." << std::endl;
    }

    return 0;
}
