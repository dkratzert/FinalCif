#pragma once

void add_argvalues(std::string& command, int argc, char* argv[]);

void hide_console_window();

void should_window_hide(int argc, char* argv[], bool& hide);

void run_from_commandline(int argc, char* argv[], std::string& parent_dir, char  current_dir[260]);

int main(int argc, char* argv[]);
