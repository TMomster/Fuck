# Fuck

---

Fuck is a tool for quickly launching programs by adding the fuck deirectory to the environment variable.

To start a program using Fuck, you need to register the path of target exe file. Taking an application as example.

```bash
fuck -m new example C:\Program Files (x86)\example\example.exe
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

---

TMomster, 2025.05.21
