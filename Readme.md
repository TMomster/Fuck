# Fuck

---

如果您是中文使用者，请阅读 [中文版说明](./ReadmeCN.md) 。

---

Fuck is a tool for quickly launching programs by adding the fuck deirectory to the environment variable.

To start a program using Fuck, you need to register the path of target exe file. Taking an application as example.

```bash
fuck -m new example "C:\Program Files (x86)\example\example.exe"
```

Now, you can quickly start it by using Fuck.

```bash
fuck example
```

This program mainly solves the problem of slow response of Windows search boxes at times.

---

##### Fuck Command

If you have already set some upath in Fuck's memory, using `fuck + upath-name` is the way to activate an upath.

However, when you first use Fuck, there's no upath in the directory. To manage the memory of Fuck, and also the configs, you need the Fuck command to tell the program what you want to do.

Using `fuck -m` as a statement of you are using codes under the command mode.

```bash
fuck -m
```

Now, let's see what the commands can do.

```bash
fuck -m new [upath-name] [upath-content]
fuck -m del [upath-name]
fuck -m update [upath-name] [new-content]
fuck -m rename [upath-name] [new-name]
fuck -m list
fuck -m cat [upath-name]
fuck -m browser set [browser-path]
```

`new` creates a new upath memory in the memory.

`del` deletes an existed upath file from the memory.

`update` updates the content of upath.

`rename` updates the name of upath.

`list` shows all the existed upath.

`cat` shows content of a single upath.

`browser set` is to set the path of a default web browser that Fuck uses.

---

##### Web URL

Upath file could save a file path or a web URL in the same way.

```bash
fuck -m new google "www.google.com"
```

When you're activating a upath file with web URL, the program will call the browser to search the website.

It means you need to set the browser path at first. Using command `fuck -m browser set ...` to set the default browser of program.

```
fuck -m browser set "path/to/browser"
```

---

##### Using Command with Parameter

Sometimes exe files require one or more parameters when you are call them.

Fuck allows you to use command with extra parameters.

For example, here is a `repeator.exe` compiled from C language.

```c
// C:\programs\repeator.exe
#include <stdio.h>
int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; i ++) {
        printf("%s ", argv[i]);
    }
    return 0;
}
```

This program will repeat any strings you send to it.

Now we try to register and use the program in Fuck.

```bash
fuck -m new repeator "C:\program\repeator.exe"
fuck repeator hello world
```

In this case, we send 2 strings as the program's parameters.

This calling is same as:

```bash
start "C:\program\repeator.exe" hello world
```

Therefore, the result is to repeat the message "hello world" once.

---

TMomster, 2025.05.21
