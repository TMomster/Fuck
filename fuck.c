#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_COMMAND_LENGTH 1024

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "[[FUCK]] Missing Parameter...\nUsage: fuck <command> [args...]\n");
        return 1;
    }

    char command[MAX_COMMAND_LENGTH];
    command[0] = '\0';

    strcat(command, "python G:\\fuck\\core.py");

    for (int i = 1; i < argc; i++) {
        strcat(command, " ");
        strcat(command, argv[i]);
    }

    // printf("Executing command: %s\n\n", command);

    int status = system(command);

    if (status == -1) {
        perror("system");
        return 1;
    }

    return 0;
}