# Fuck

---

##### 快速开始

        Fuck 是一个快速启动程序的工具，将 fuck 目录添加到环境变量，即可快速启动程序。Fuck 本身是一个快捷方式管理工具，您可以将程序路径注册到 Fuck 中，这样只需要通过命令行即可管理您的程序，从而避免在桌面堆放大量快捷方式，节省屏幕空间。

        使用 Fuck 启动程序，您需要注册目标 exe 程序的路径，以 steam 应用为例：

```bash
fuck -m new steam "C:\Program Files (x86)\Steam\steam.exe"
```

        这样就可以快速在 Fuck 中注册这个程序，以后就可以在命令行中快速地启动：

```bash
fuck steam
```

---

##### Fuck 的命令

        在命令行中输入 fuck 后，会提示 Missing Parameter，然后就可以看到 fuck 的用法：

```bash
[[FUCK]] Missing Parameter...
Usage: fuck <command> [args...]
```

        Fuck 有两种基本用法，一种是 `fuck + 名称` 可以直接启动已经在 Fuck 中注册的程序；另一种则是用 `fuck + -m + 指令` 的形式进入命令模式。在命令模式下可以对 Fuck 进行管理。

        Fuck 的原理是将您需要使用的程序路径注册为一个 UPATH 文件，您可以在 Fuck 根目录下的 memory/UPATH 处找到所有已经注册的 UPATH，在您第一次使用 Fuck 的时候，这个目录应该是空的。

        现在我们来看如何通过命令创建一个 UPATH：

```bash
fuck -m new steam "C:\Program Files (x86)\Steam\steam.exe"
---------->>>
UPATH 'steam' created successfully.
---------->>>
```

        像这样，我们就建立了一个名为 steam 的 UPATH，即 `memory/UPATH/steam.upath`。

        通过 del、update、rename 命令，可以对已有的 UPATH 进行删除、修改内容、重命名的操作。

        我们来演示一下，如果创建了错误的文件，如何通过命令来删除它：

```bash
fuck -m new err "wrong path"
---------->>>
UPATH 'err' created successfully.
---------->>>

fuck -m del err
---------->>>
UPATH 'err' has been deleted successfully.
---------->>>
```

        就像这样，只需要在命令行中进入 del 模式，然后指定文件名即可删除。

---

TMomster, 2025.05.19
