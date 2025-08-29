#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define MAX_COMMAND_LENGTH 2048
#define MAX_PATH_LENGTH    1024

int main(int argc, char *argv[]) {
    // 检查参数
    if (argc < 2) {
        fprintf(stderr, "[[FUCK]] Missing Parameter...\n");
        fprintf(stderr, "Usage: fuck <command> [args...]\n");
        fprintf(stderr, "[[FUCK]] Use \"fuck -m help\" to check help.\n");
        return 1;
    }

    // 获取当前可执行文件的完整路径
    char exe_path[MAX_PATH_LENGTH];
    if (GetModuleFileNameA(NULL, exe_path, MAX_PATH_LENGTH) == 0) {
        fprintf(stderr, "[[FUCK]] Failed to get executable path.\n");
        return 1;
    }

    // 提取目录路径（去掉文件名）
    char *last_slash = strrchr(exe_path, '\\');
    if (last_slash == NULL) {
        fprintf(stderr, "[[FUCK]] Invalid executable path format.\n");
        return 1;
    }
    *last_slash = '\0'; // 此时 exe_path 只保留目录部分

    // 构建 root.txt 的完整路径
    char root_path[MAX_PATH_LENGTH];
    snprintf(root_path, sizeof(root_path), "%s\\root.txt", exe_path);

    // 打开 root.txt 读取 Python 主脚本路径
    FILE *root_file = fopen(root_path, "r");
    if (root_file == NULL) {
        fprintf(stderr, "[[FUCK]] Cannot open root.txt at: %s\n", root_path);
        fprintf(stderr, "Please run initializer.py first to set up the environment.\n");
        return 1;
    }

    char python_core_path[MAX_PATH_LENGTH];
    if (fgets(python_core_path, sizeof(python_core_path), root_file) == NULL) {
        fprintf(stderr, "[[FUCK]] Failed to read path from root.txt.\n");
        fclose(root_file);
        return 1;
    }
    fclose(root_file);

    // 去除换行符
    python_core_path[strcspn(python_core_path, "\n\r")] = '\0';

    // 检查读取的路径是否存在
    FILE *test = fopen(python_core_path, "r");
    if (test == NULL) {
        fprintf(stderr, "[[FUCK]] Python script not found: %s\n", python_core_path);
        fprintf(stderr, "Check the path in root.txt.\n");
        return 1;
    }
    fclose(test);

    // 构建最终命令：python "script_path" arg1 arg2 ...
    char command[MAX_COMMAND_LENGTH];
    int offset = 0;
    offset += snprintf(command, sizeof(command), "python \"%s\"", python_core_path);

    for (int i = 1; i < argc; i++) {
        // 检查剩余空间
        if (offset >= MAX_COMMAND_LENGTH - 1) {
            fprintf(stderr, "[[FUCK]] Command too long, truncation avoided.\n");
            return 1;
        }

        int space_needed = strlen(argv[i]) + 3; // 最坏情况：加空格 + 双引号
        if (offset + space_needed >= MAX_COMMAND_LENGTH) {
            fprintf(stderr, "[[FUCK]] Argument '%s' makes command too long.\n", argv[i]);
            return 1;
        }

        // 添加空格
        command[offset++] = ' ';

        // 如果参数含空格，用双引号包裹
        if (strchr(argv[i], ' ') != NULL || strchr(argv[i], '"') != NULL) {
            command[offset++] = '"';
            for (int j = 0; argv[i][j] != '\0'; j++) {
                // 转义双引号: " -> \"
                if (argv[i][j] == '"')
                    command[offset++] = '\\';
                command[offset++] = argv[i][j];
            }
            command[offset++] = '"';
        } else {
            // 无空格，直接复制
            strcpy(command + offset, argv[i]);
            offset += strlen(argv[i]);
        }
    }
    command[offset] = '\0';

    // 执行命令
    int result = system(command);
    if (result == -1) {
        perror("[[FUCK]] system() failed");
        return 1;
    }

    return 0;
}