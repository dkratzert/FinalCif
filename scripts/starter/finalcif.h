#pragma once

void add_argvalues(std::string& command, int argc, char* argv[]);

void hide_console_window();

void should_window_hide(int argc, char* argv[], bool& hide);
