### 1. 命令行启动

出现：
[me@linuxbox ~]$
括号里代表用户名@主机名紧接着当前工作目录（稍后会有更多介绍）和一个美元符号。
如果提示符的最后一个字符是“#”, 而不是“$”, 那么这个终端会话就有超级用户权限。 

### 2. shell简单命令行示例

1.显示时期
[me@linuxbox ~]$ date
Thu Oct 25 13:51:54 EDT 2007

查看磁盘剩余空间的数量
输入 df

同样地，显示空闲内存的数量
输入命令 free

结束中断会话
我们可以通过关闭终端仿真器窗口，或者是在 shell 提示符下输入 exit 命令来终止一个终端会话：

访问虚拟终端
即使终端仿真器没有运行，在后台仍然有几个终端会话运行着。它们叫做虚拟终端 或者是虚拟控制台。在大多数 Linux 发行版中，这些终端会话都可以通过按下 Ctrl-Alt-F1 到 Ctrl-Alt-F6 访问。当一个会话被访问的时候， 它会显示登录提示框，我们需要输入用户名和密码。要从一个虚拟控制台转换到另一个， 按下 Alt 和 F1-F6(中的一个)。返回图形桌面，按下 Alt-F7。

### 3. shell文件操作命令行

pwd — 打印出当前工作目录名  （print work directory）

cd — 更改目录

ls — 列出目录内容，目录包含的文件及子目录


cd
路径名可通过两种方式来指定，一种是绝对路径， 另一种是相对路径。我们先来介绍绝对路径。

绝对路径
从根目录开始
例：
[me@linuxbox ~]$ cd /usr/bin
[me@linuxbox bin]$ pwd
/usr/bin
[me@linuxbox bin]$ ls
...Listing of many, many files ...
它意味着从根目录（用开头的”/”表示）开始，有一个叫 “usr” 的 目录包含了目录 “bin”。我们把工作目录转到 /usr/bin 目录下

相对路径
， 我们在文件系统树中用一对特殊符号来表示相对位置。 这对特殊符号是 “.”工作目录 和 “. .” 工作目录父目录
比方说我们想更改工作目录到 /usr/bin 的父目录 /usr。可以通过两种方法来实现。可以使用以下绝对路径名：

[me@linuxbox bin]$ cd /usr
[me@linuxbox usr]$ pwd
/usr

或者， 也可以使用相对路径：

[me@linuxbox bin]$ cd `..`
[me@linuxbox usr]$ pwd
/usr

#### cd快捷键

| cd            | 更改工作目录到你的家目录。                                   |
| ------------- | ------------------------------------------------------------ |
| cd -          | 更改工作目录到先前的工作目录。                               |
| cd ~user_name | 更改工作目录到用户家目录。例如, cd ~bob 会更改工作目录到用户“bob”的家目录。 |



#### 关于文件名的重要规则

1. 以 “.” 字符开头的文件名是隐藏文件。这仅表示，ls 命令不能列出它们， 用 ls -a 命令就可以了。当你创建帐号后，几个配置帐号的隐藏文件被放置在 你的家目录下。稍后，我们会仔细研究一些隐藏文件，来定制你的系统环境。 另外，一些应用程序也会把它们的配置文件以隐藏文件的形式放在你的家目录下面。

   ![img](https://img-blog.csdnimg.cn/img_convert/873adbaa442fc0b5ad2b4b9fcb129756.png)

2. 文件名和命令名是大小写敏感的。文件名 “File1” 和 “file1” 是指两个不同的文件名。

3. Linux 没有“文件扩展名”的概念，不像其它一些系统。可以用你喜欢的任何名字 来给文件起名。文件内容或用途由其它方法来决定。虽然类 Unix 的操作系统， 不用文件扩展名来决定文件的内容或用途，但是有些应用程序会。

4. 虽然 Linux 支持长文件名，文件名可能包含空格，标点符号，但标点符号仅限 使用 “.”，“－”，下划线。最重要的是，不要在文件名中使用空格。如果你想表示词与 词间的空格，用下划线字符来代替。过些时候，你会感激自己这样做。

### 4. 操作系统

#### Linux系统常用命令

- ls — 列出目录内容
- file — 确定文件类型
- less — 浏览文件内容

#### ls用法详解

- ls

列出文件内容

- ls  [（多个）文件路径，空格隔开]

  ![](https://img-blog.csdnimg.cn/img_convert/4d8d3a773b132121a85bf0115ac7e057.png)

（其中~指用户家目录）

- ls -l 以长格式输出

![](https://img-blog.csdnimg.cn/img_convert/da584d54c43158b8ef8053acdce0b910.png)

- ls -lt ls 命令有两个选项， “l” 选项产生长格式输出，“t”选项按文件修改时间的先后来排序。
- ls -lt --reverse  其中长选项--reverse的作用使得输出结果反序

常用ls命令选项

| 选项 | 长选项           | 描述                                                         |
| :--- | :--------------- | :----------------------------------------------------------- |
| -a   | --all            | 列出所有文件，甚至包括文件名以圆点开头的默认会被隐藏的隐藏文件。 |
| -d   | --directory      | 通常，如果指定了目录名，ls 命令会列出这个目录中的内容，而不是目录本身。 把这个选项与 -l 选项结合使用，可以看到所指定目录的详细信息，而不是目录中的内容。 |
| -F   | --classify       | 这个选项会在每个所列出的名字后面加上一个指示符。例如，如果名字是 目录名，则会加上一个'/'字符。 |
| -h   | --human-readable | 当以长格式列出时，以人们可读的格式，而不是以字节数来显示文件的大小。 |
| -l   |                  | 以长格式显示结果。                                           |
| -r   | --reverse        | 以相反的顺序来显示结果。通常，ls 命令的输出结果按照字母升序排列。 |
| -S   |                  | 命令输出结果按照文件大小来排序。                             |
| -t   |                  | 按照修改时间来排序。                                         |

#### 长格式列表的含义

例如：

![](https://img-blog.csdnimg.cn/img_convert/cdff659de2462063a74e32691dffcb71.png)

**1-10位所代表的含义**

- d:第一位表示文件类型。d是目录文件，l是链接文件，-是普通文件，p是管道
- rwx:第2-4位表示这个文件的属主拥有的权限，r是读，w是写，x是执行。
- r-x:第5-7位表示和这个文件属主所在同一个组的用户所具有的权限。
- r-x:第8-10位表示其他用户所具有的权限。

**2 aei aei 4096 3月 2 21:50 视频**  含义：

| 字段        | 含义                                             |
| ----------- | ------------------------------------------------ |
| 2           | 文件的硬链接数目。参考随后讨论的关于链接的内容。 |
| aei         | 文件所有者的用户名。                             |
| aei         | 文件所属用户组的名字                             |
| 4096        | 以字节数表示的文件大小。                         |
| 3月 2 21:50 | 上次修改文件的时间和日期。                       |
| 视频        | 文件名。                                         |

#### 确定文件类型

在 Linux 系统中，并不要求文件名来反映文件的内容。即类似于Windows的.jpg后缀名并不可以决定文件类型。然而类似于picture.jpg的文件名，我们为了使其包含图片，可调用命令：

```shell
file filename #文件内容陈述
```

![](https://img-blog.csdnimg.cn/img_convert/e9b91bd4c0d8ff2b523c76312993bb49.png)

#### less用法详解

less filename

查询txt文档

常用命令

| 字段                         | 含义                                                     |
| ---------------------------- | -------------------------------------------------------- |
| ↑或下                        | 向上或下翻滚一行                                         |
| ←（b）或0→（space）          | 向前或后滚动一页                                         |
| G                            | 移动到最后一行                                           |
| 1G或g                        | 移动到开头                                               |
| /characters（/后直接加字符） | 向前查找指定字符串                                       |
| character？（字符后直接加?） | 向后查找指定字符串                                       |
| n                            | 向前查找下一个出现的字符串，这个字符串是之前所指定查找的 |
| h                            | 显示帮助屏幕                                             |
| q                            | 推出less程序                                             |

#### 链接文件 

例：

```
lrwxrwxrwx 1 aei aei 1024 2021-03-06 07:34 lizi -> lizi-1.0.so
```

上述代码第一位为l，表明此文件为链接文件；**lizi -> lizi-1.0.so**表明lizi为一个符号链接，用来指向lizi-1.0.so 当我们寻找lizi时，实际上找到的是lizi-1.0.so 

这种做法的用处之一：当我们更新lizi-1.0.so时，只需要消除lizi的链接，然后更新lizi.1.1.so，再用lizi链接到新的文件。那么其他文件对此文件的引用就不需要随着文件版本号的更新而改变了（一直是lizi）。

### 5. 操作文件和目录

学习命令简介：

- cp — 复制文件和目录
- mv — 移动/重命名文件和目录
- mkdir — 创建目录
- rm — 删除文件和目录
- ln — 创建硬链接和符号链接

#### cp(复制)选项

```shell
-a, --archive  #复制文件和目录，以及它们的属性，包括拥有者和所有权。 通常，副本具有用户所操作文件的默认属性。

-i, --interactive #在重写已存在文件之前，提示用户确认。如果这个选项不指定， cp 命令会默认重写文件。
-r, --recursive  #递归地复制目录及目录中的内容。当复制目录时， 需要这个选项（或者-a 选项）。
-u, --update #当把文件从一个目录复制到另一个目录时，仅复制 目标目录中不存在的文件，或者是文件内容新于目标目录中已经存在的文件。
-v, --verbose #显示翔实的命令操作信息
```



#### cp 常用

```shell
cp file1 file2 #复制文件 file1 内容到文件 file2。如果 file2 已经存在， file2 的内容会被 file1 的内容重写。如果 file2 不存在，则会创建 file2。
cp -i file1 file2 #这条命令和上面的命令一样，除了如果文件 file2 存在的话，在文件 file2 被重写之前， 会提示用户确认信息。
cp file1 （file2） dir1  #复制文件 file1 和(文件 file2) 到目录 dir1。目录 dir1 必须存在。
cp dir1/* dir2    #使用一个通配符，在目录 dir1 中的所有文件都被复制到目录 dir2 中。 dir2 必须已经存在。
cp -r dir1 dir2  #复制目录 dir1 中的内容到目录 dir2。如果目录 dir2 不存在， 创建目录 dir2，操作完成后，目录 dir2 中的内容和 dir1 中的一样。 如果目录 dir2 存在，则目录 dir1 (和目录中的内容)将会被复制到 dir2 中。
```

#### mkdir 创建目录

```shell
mkdir  [文件目录/文件名+后缀] #创建
```



#### touch 创建文件

```shell
touch 文件名字.后缀类型   #创建
```



#### mv（移动或重命名）

```shell
#mv选项
-i --interactive #在重写一个已经存在的文件之前，提示用户确认信息。 如果不指定这个选项，mv 命令会默认重写文件内容。
-u --update #当把文件从一个目录移动另一个目录时，只是移动不存在的文件， 或者文件内容新于目标目录相对应文件的内容。
-v --verbose #当操作 mv 命令时，显示翔实的操作信息。

#mv实例
mv file1 file2 #移动 file1 到 file2。如果 file2 存在，它的内容会被 file1 的内容重写。 如果 file2 不存在，则创建 file2。 这两种情况下，file1 都不再存在。
mv file1 file2 dir1 #移动 file1 和 file2 到目录 dir1 中。dir1 必须已经存在。
mv dir1 dir2 #如果目录 dir2 不存在，创建目录 dir2，并且移动目录 dir1 的内容到 目录 dir2 中，同时删除目录 dir1。如果目录 dir2 存在，移动目录 dir1（及它的内容）到目录 dir2。
```



#### rm（删除文件和目录）

```shell
#rm选项
-i, --interactive  #在删除已存在的文件前，提示用户确认信息。 如果不指定这个选项，rm 会默默地删除文件（y/n）
-r, --recursive #递归地删除文件，这意味着，如果要删除一个目录，而此目录 又包含子目录，那么子目录也会被删除。要删除一个目录，必须指定这个选项。
-f, --force #忽视不存在的文件，不显示提示信息。这选项覆盖了“--interactive”选项。
-v, --verbose #在执行 rm 命令时，显示翔实的操作信息。

#rm实例
rm file1 #默默地删除文件
rm -r file1 dir1 #删除文件 file1, 目录 dir1，及 dir1 中的内容。
rm -rf file1 dir1 #同上，除了如果文件 file1，或目录 dir1 不存在的话，rm 仍会继续执行。
```



#### 创建链接

创建方法：

```shell
ln file link #创建硬链接
ln -s item link #创建符号链接，其中“item”文件或者目录
```

[硬链接和软链接的不同](https://www.linuxprobe.com/soft-hard-links-comments.html)

#### 通配符（快速指定文件）

| 通配符        | 意义                               |
| :------------ | :--------------------------------- |
| *             | 匹配任意多个字符（包括零个或一个） |
| ?             | 匹配任意一个字符（不包括零个）     |
| [characters]  | 匹配任意一个属于字符集中的字符     |
| [!characters] | 匹配任意一个不是字符集中的字符     |
| [[:class:]]   | 匹配任意一个属于指定字符类中的字符 |

### 6. shell命令详解

#### 命令解析

```shell
type command #显示命令类型
```

![](https://img-blog.csdnimg.cn/img_convert/ee5ebe043717a3c6069ecbd05d698018.png)

```shell
which command  #显示可执行程序位置
```

```shell
help command #介绍程序用法
command --help  #同上
```

![](https://img-blog.csdnimg.cn/img_convert/38e02992bb73b939a3cc4800b0374a46.png)

```shell
不常用：
man program #程序手册
apropos 字符 #利用关键词或者模糊匹配相关命令
whatis command #简洁的命令说明
info command #显示程序Info条目（可控制）
```

#### 用别名创建自己的命令

储备知识：

- 同行命令写法

```shell
command1; command2; command3...
```

- 语法结构

  ```shell
   alias aliasname='command; command; command' #创建别名
   unlias aliasname #删除别名
  ```

例：

![](https://img-blog.csdnimg.cn/img_convert/6407ca0768c9cf139d5d266c937de9e8.png)

### 7. I/O输出重定向

作用：将I/O的标准输出重新定向到除了屏幕之外的另一个文件。

完成这种操作我们可以使用“>”重定向符后接文件名（可以不存在）将标准输出保存在另一文件中。

例：![](https://img-blog.csdnimg.cn/img_convert/00d42f5c7c4fdb57d01f7acb3a29522d.png)

在这个过程中 我们将w1.png的文件长格式的信息保存到了output.txt中，在新建的txt文件中，我们看到其内容为：

-rw-rw-r-- 1 aei aei 8216194  3月  5 12:42 ./w1.png

表明本该在终端输出的内容最终在w1.txt中保存下来。

**注意** ：错误的shell命令或错误提示不会保存在重定向的txt文件中，并且会将txt文件的内容清空。

#### >>操作符

与>用法相同，但不同于>会将文件内容清空后再存储标

准输出，>>会将标准输出内容存储在目标文件的文件内容之后。

#### 重定向错误输出到文件

由上可知，当我们的命令执行发生错误的时候，使用>>和>都不会将错误保存在文件中，而是在终端直接输出。其原因在于shell中定义了文件操作符0，1，2分别表示输入，输出，错误。当我们直接使用>>或>时，shell默认只存储标准输出。

重定向标准输出和错误到同一个文件：

```shell
ls -l /bin/usr 2> ls-error.txt #只将错误存储在目标文件中
ls -l /bin/usr > ls-output.txt 2>&1 #将错误信息和标准输出同时存储在输出文件中（老版）
ls -l /bin/usr &> ls-output.txt #将错误信息和标准输出同时存储在输出文件中（新版）
```

#### 黑洞/dev/null

当我们想要丢掉一些不必要的输出时，我们可以重定向输出结果到/dev/null的特殊文件，其作用可以比作一个黑洞，通常用于丢弃不需要的数据输出， 或者用于输入流的空文件。

例如：

```shell
ls -l /bin/usr 2> /dev/null #将错误信息丢入到/dev/null中，并且不在终端输出。
```

###  8. I/O输入重定向

#### cat （连接文件）

```shell
cat [file]  #读取一个或多个文件然后复制到标准输出（不说明即输出到终端）
cat [file1] [file2] > [file3] #将几个文件的内容连接起来（每个文件之间开头末尾之间隔一行）并储存在目标文件

例：
cat test* > tests.txt 
#将所有开头为test的文件合并并保存在tests.txt中
```

#### 利用cat来输入文件

```shell
cat > testcin.txt #不带输入文件的命令，默认从键盘读入文件
#输入内容后，CTRL+d告诉cat结束输入

#例
cat > testcin.txt
hello linux
hello fanlulu #输入CTRL+d结束输入
```

结果：

![](https://img-blog.csdnimg.cn/img_convert/0fc8ddf111c5a588b62100ef895af4ae.png)

可以看到最终testcin.txt存储了从键盘输入的流。

同时我们还可以重定向其他文件读入

```shell
cat < file1 > file2 #从file1里读入文件输入到file2 虽然和cat file >file2功能类似但是实现过程是不一样的
```

#### 管道线

用来将一个命令的输出作为输入传入下个命令

用法：

```shell
command1 | command2
例子：
ls -l | less   #将所在文档的文件用less预览
ls -l | sort | less #将所在文档的文件排序并且用less预览
```

例：

分别输入上述代码后的less预览结果：

![](https://img-blog.csdnimg.cn/img_convert/b4f9f42007a4120f0c24eb97f2cda751.png)

![](https://img-blog.csdnimg.cn/img_convert/231d24fe08a61ee1ce8bc56d818ccde6.png)

其中sort命令作为一个过滤器的作用给要预览的内容进行编辑或过滤。

#### 拓展：[Linux的高效过滤器](https://www.linuxprobe.com/linux-filter-cmd.html)

| 过滤器                 | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| sort                   | 排序                                                         |
| uniq                   | 忽略重复行（-d会显示重复行的数据列表）                       |
| wc file  或 \| wc      | 打印行数 字数 字节数（-l限制只输出行数）                     |
| grep pattern [file...] | 打印匹配字段                                                 |
| head / tail            | 打印文件开头/末尾10行（-n调节行数）                          |
| tee                    | 从 Stdin 读取数据，并同时输出到 Stdout 和文件 （捕捉终端内容存到文件） |

i.e.

![](https://img-blog.csdnimg.cn/img_convert/b70e44c59c08eef7ff290131e5419ad3.png)

### 9. echo  ——显示文本

```shell
echo string #显示一串字符。会在终端显示string
echo d* #显示所有d开头的该目录下的文件
echo ~ #显示家目录 （/home/user）
echo $((expression)) #expression为算数表达式例如1+2 会输出算术结果
echo head-{a,b}-tail #输出head-a-tail  head-b-tail  
echo a{1..5}b  #输出a1b a2b a3b a4b a5b
```

#### 参数展开（$）

相当于是一个变量，供我们更加方便地引用和检查。

使用方法： 

```shell
 $ 变量名
#可使用 printenv | less 来查看有效的变量列表
#例如 echo $USER 可以显示出本机的用户名称
```

#### 命令替换

命令替换让我们将一个命名的输出作为一个展开模式使用。

使用方法

```shell
$(command)
#作用：将一个命令的结果作为输出
例：
ls  $(which cp)
结果： /bin/cp
```

#### 引用

作用：禁止不必要的展开

```shell
echo $10.00 #会输出0.00 因为$1并不是一个有意义的变量

ls i you.txt #将报错出现无i 和 you.txt的提示，而其实i you.txt才是一个文件（linux系统中支持文件名出现空格）

#禁止单词分割和展开的方法：

#双引号：
ls "i you.txt" #注意在引号内参数展开、算术表达式展开和命令替换仍然有效

#单引号：
echo '$10.00' #输出￥10.00，单引号内的所有展开和单词分割都被禁用



```



效果：

![](https://img-blog.csdnimg.cn/img_convert/6690ca2ee7ac5d5bfee181ccf07b8734.png)

#### 转义字符

和c语言中的转义字符类似，\加$，！,"",'',\，等可以将其变为普通字符。

当然还有我们熟悉的转义普通字符作为控制字符：

| 转义序列 | 含义                                   |
| -------- | -------------------------------------- |
| \a       | 响铃（”警告”－导致计算机嘟嘟响）       |
| \b       | 退格符                                 |
| \n       | 新的一行。在类 Unix 系统中，产生换行。 |
| \r       | 回车符                                 |
| \t       | 制表符                                 |

**注意:**使用转义字符的时候需要在echo后加-e，并且在双引号""内，才会将转义序列特别加以处理，而不会将它当成一般文字输出

例： echo -e "\a"



### 10.  脚本简介

脚本 script
许多 Linux 发行版包括一个叫做 script 的程序， 这个程序可以记录整个 shell 会话，并把 shell 会话存在一个文件里面。这个命令的基本语法是：script [file]
命令中的 file 是指用来存储 shell 会话记录的文件名。如果没有指定文件名，则使用文件 typescript。查看脚本的手册页，可以得到一个关于 script 程序选项和特点的完整列表。(man script)




### 11.  权限

Linux系统中存在权限管理，主要体现在用户组对文件的读写操作的权限
例如rwxr--r--说明文件所有者可读可写可操作,同组用户和其他所有用户都只可读

#### chmod － 更改文件模式

chmod 命令支持两种不同的方法来改变文件模式：八进制数字表示法或 符号表示法。

1.八进制数字表示法
Octal	Binary	File Mode
0	  000 	  ---
1	  001 	 --x
2  	010 	 -w-
3  	011  	-wx
4	  100  	r--
5	  101  	r-x
6	  110  	rw-
7	  111	   rwx
通过三个8进制表达，可以设置文件所有者、用户组和其他人的权限。
例子:
chmod 611 test.txt  
再用ls -l test.txt  就可以发现文件的权限被改变了

2.符号表示法
chmod 命令支持一种符号表示法，来指定文件模式。符号表示法分为三部分：更改会影响谁， 要执行哪个操作。既用户执行操作 权限这样的形式。u	"user"的简写，意思是文件或目录的所有者。g	用户组。o	"others"的简写，意思是其他所有的人。a	"all"的简写，是"u","g"和“o”三者的联合。如果没有指定字符，则假定使用”all”。执行的操作可能是一个“＋”字符，表示加上一个权限， 一个“－”，表示删掉一个权限，或者是一个“＝”，表示只有指定的权限可用，其它所有的权限被删除。权限由 “r”、“w”和 “x” 来指定。

例子:
u+x	为文件所有者添加可执行权限。
u-x	删除文件所有者的可执行权限。
+x	为文件所有者，用户组，和其他所有人添加可执行权限。 等价于 a+x。
o-rw	除了文件所有者和用户组，删除其他人的读权限和写权限。
go=rw	给文件所属的组和文件所属者/组以外的人读写权限。如果文件所属组或其他人已经拥有执行的权限，执行权限将被移除。
u+x,go=rw	给文件拥有者执行权限并给组和其他人读和执行的权限。多种设定可以用逗号分开。



#### umask － 设置默认权限

当创建一个文件时，umask 命令控制着文件的默认权限。umask 命令使用八进制表示法来表达从文件模式属性中删除一个位掩码, 具体用法和掩码意义：https://baike.sogou.com/m/v54497252.htm


#### 特殊权限

在Linux系统中，除了读写操作权限，还有一些特殊权限，具体内容可参考：

https://www.cnblogs.com/dabai-wang09/articles/11123435.html



#### UBuntu更改用户(获得超级用户权限) sudo

https://www.cnblogs.com/holynn/articles/1448658.html
https://blog.csdn.net/linuxshine/article/details/50478503

#### 多用户组操作

chown － 更改文件所有者和用户组

chgrp － 更改用户组所有权

因为我现在并没有多个用户，也暂时不需要处理多用户问题，这里相关内容，大家可以自行百度了解具体相关内容。

### 12.  进程

Linux 内核通过使用进程来 管理多任务。进程，就是Linux 组织安排正在等待使用 CPU的各种程序的方式。
Linux提供给我们与进程有关的命令行工具，这些工具帮助我们查看程序的执行状态，以及怎样终止行为不当的进程。

```shell
ps – 报告当前进程快照

top – 显示任务

jobs – 列出活跃的任务

bg – 把一个任务放到后台执行

fg – 把一个任务放到前台执行

kill – 给一个进程发送信号

killall – 杀死指定名字的进程

shutdown – 关机或重启系统


```

当系统启动的时候，内核先把一些它自己的活动初始化为进程，然后运行一个叫做 init 的程序。init， 依次地，再运行一系列的称为 init 脚本的 shell 脚本（位于/etc），它们可以启动所有的系统服务。 其中许多系统服务以守护（daemon）程序的形式实现，守护程序仅在后台运行，没有任何用户接口(User Interface)。 这样，即使我们没有登录系统，至少系统也在忙于执行一些例行事务。

内核维护每个进程的信息，以此来保持事情有序。例如，系统分配给每个进程一个数字，这个数字叫做 进程(process) ID 或 PID。PID 号按升序分配，init 进程的 PID 总是1。内核也对分配给每个进程的内存和就绪状态进行跟踪以便继续执行这个进程。 像文件一样，进程也有所有者和用户 ID，有效用户 ID，等等。

#### ps 查看进程

结果:显示出与当前终端界面有关的进程
PID        TTY         TIME            CMD
5198      pts/1       00:00:00        bash
10129    pts/1       00:00:00        ps

PID  进程id
TTY  进程的控制终端
TIME 进程所需要的CPU时间
CMD 命令提示符

```shell
ps x  查看所有进程(可通过管道用less查看)
```

![](https://img-blog.csdnimg.cn/img_convert/62adf67972c516a46eefd9ada4e23f92.png)

其中的新增的一栏STAT表示进程的当前状态

| 状态 | 含义                                                         |
| :--- | :----------------------------------------------------------- |
| R    | 运行中。这意味着，进程正在运行或准备运行。                   |
| S    | 正在睡眠。进程没有运行，而是，正在等待一个事件， 比如说，一个按键或者网络分组。 |
| D    | 不可中断睡眠。进程正在等待 I/O，比方说，一个磁盘驱动器的 I/O。 |
| T    | 已停止. 已经指示进程停止运行。稍后介绍更多。                 |
| Z    | 一个死进程或“僵尸”进程。这是一个已经终止的子进程，但是它的父进程还没有清空它。 （父进程没有把子进程从进程表中删除） |
| <    | 一个高优先级进程。这可能会授予一个进程更多重要的资源，给它更多的 CPU 时间。 进程的这种属性叫做 niceness。具有高优先级的进程据说是不好的（less nice）， 因为它占用了比较多的 CPU 时间，这样就给其它进程留下很少时间。 |
| N    | 低优先级进程。 一个低优先级进程（一个“nice”进程）只有当其它高优先级进程被服务了之后，才会得到处理器时间。 |

```shell
ps aux
```

![](https://img-blog.csdnimg.cn/img_convert/ca81d11c72ce075cb6db34a92fa2dd70.png)

| 标题  | 含义                                             |
| :---- | :----------------------------------------------- |
| USER  | 用户 ID. 进程的所有者。                          |
| %CPU  | 以百分比表示的 CPU 使用率                        |
| %MEM  | 以百分比表示的内存使用率                         |
| VSZ   | 虚拟内存大小                                     |
| RSS   | 进程占用的物理内存的大小，以千字节为单位。       |
| START | 进程启动的时间。若它的值超过24小时，则用天表示。 |

#### top 动态查看进程

top 程序以进程活动顺序显示连续更新的系统进程列表。（默认情况下，每三秒钟更新一次）

![](https://img-blog.csdnimg.cn/img_convert/2ee2b5cb7053964db1fadec60277b387.png)

#### Ctrl-c   中断程序

例：

尝试在终端输入xlogo打开一个窗口，后使用Ctrl-c关闭窗口。

**注：**小部分的进程是不可以用Ctrl-c终止的。

#### command &    后台运行

假如说我们想让 shell 提示符返回，却不终止 xlogo 程序。我们可以把 这个程序放到后台(background)执行。把终端想象是一个有前台（包含在表层可见的事物，像 shell 提示符） 和后台（包含表层之下的隐藏的事物）（的设备）。为了启动一个程序并让它立即在后台 运行，我们在程序命令之后，加上”&”字符：

```shell
xlogo &
```

之后终端将会打印出任务号[1]和他的PID，我们在执行ps后，可以发现，xlogo已经在执行当中。

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-vOXbefDn-1617349513918)(C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1615287740935.png)]

同时，使用命令jobs，可以看到也在终端已经执行的命令。

#### fg %任务号      将进程回到前台

一个在后台运行的进程对一切来自键盘的输入都免疫，也不能用 Ctrl-c 来中断它。 为了让一个进程返回前台 (foreground)，这样使用 fg 命令：

```shell
fg %命令号 #例如 fg  %1
```

####  Ctrl-z  停止一个进程

有时候，我们想要停止一个进程，而不是终止它。我们这么做通常是为了允许前台进程被移动到后台。 输入 Ctrl-z，可以停止一个前台进程。

此后我们可以将程序使用fg命令回到前台，或者使用bg命令将程序移到后台

#### kill 杀死命令

kill 命令被用来“杀死”程序。这样我们就可以终止需要杀死的程序。

```shell
kill PID
```

我们可以先用ps等命令得知一个程序的PID，然后通过kill命令终止程序

#### 通过kill命令给进程发送信号

```shell
kill [-signal] PID
例：
kill -1 12345 #给PID为12345的程序发送挂起信号
```

默认时TERM终止信号，我们也可以发布下列信号

| 编号 | 名字 | 含义                                                         |
| :--- | :--- | :----------------------------------------------------------- |
| 1    | HUP  | 挂起（Hangup）。这是美好往昔的残留部分，那时候终端机通过电话线和调制解调器连接到 远端的计算机。这个信号被用来告诉程序，控制的终端机已经“挂断”。 通过关闭一个终端会话，可以展示这个信号的作用。在当前终端运行的前台程序将会收到这个信号并终止。许多守护进程也使用这个信号，来重新初始化。这意味着，当一个守护进程收到这个信号后， 这个进程会重新启动，并且重新读取它的配置文件。Apache 网络服务器守护进程就是一个例子。 |
| 2    | INT  | 中断。实现和 Ctrl-c 一样的功能，由终端发送。通常，它会终止一个程序。 |
| 9    | KILL | 杀死。这个信号很特别。尽管程序可能会选择不同的方式来处理发送给它的 信号，其中也包含忽略信号，但是 KILL 信号从不被发送到目标程序。而是内核立即终止 这个进程。当一个进程以这种方式终止的时候，它没有机会去做些“清理”工作，或者是保存工作。 因为这个原因，把 KILL 信号看作最后一招，当其它终止信号失败后，再使用它。 |
| 15   | TERM | 终止。这是 kill 命令发送的默认信号。如果程序仍然“活着”，可以接受信号，那么 这个它会终止。 |
| 18   | CONT | 继续。在一个停止信号后，这个信号会恢复进程的运行。           |
| 19   | STOP | 停止。这个信号导致进程停止运行，而不是终止。像 KILL 信号，它不被 发送到目标进程，因此它不能被忽略。 |

同时我们可以利用 kill -l 获得完整的信号列表。



#### 其他与进程相关的命令

| 命令名 | 命令描述                                                     |
| :----- | :----------------------------------------------------------- |
| pstree | 输出一个树型结构的进程列表(processtree)，这个列表展示了进程间父/子关系。 |
| vmstat | 输出一个系统资源使用快照，包括内存，交换分区和磁盘 I/O。 为了看到连续的显示结果，则在命令名后加上更新操作延时的时间（以秒为单位）。例如，“vmstat 5”。 ，按下 Ctrl-c 组合键, 终止输出。 |
| xload  | 一个图形界面程序，可以画出系统负载随时间变化的图形。         |
| tload  | terminal load与 xload 程序相似，但是在终端中画出图形。使用 Ctrl-c，来终止输出。 |

### 13. shell环境详解

shell 在 shell 会话中保存着大量信息。这些信息被称为 (shell 的) 环境。 程序获取环境中的数据（即环境变量）来了解本机的配置。 

 shell 在环境中存储了两种基本类型的数据，它们是环境变量和 shell 变量。Shell 变量是 bash 存放的少量数据。剩下的都是 环境变量。除了变量，shell 也存储了一些可编程的数据，即别名（6章shell命令详解）和 shell 函数（脚本）。

#### printenv 检查环境变量

```shell
printenv | less  #预览环境变量及其数值
printenv [环境变量名]  #查看具体变量的数值
```

![环境变量](https://img-blog.csdnimg.cn/img_convert/5a46d142b3ebf114386a1205315e847a.png)

执行了第一条命令后，我们看到了很多类似于 [环境变量]=[环境变量的数值] 这样的类型。

**以下是常见的一些环境变量：**

| 变量    | 内容                                                         |
| :------ | :----------------------------------------------------------- |
| DISPLAY | 如果你正在运行图形界面环境，那么这个变量就是你显示器的名字。通常，它是 ":0"， 意思是由 X 产生的第一个显示器。 |
| EDITOR  | 文本编辑器的名字。                                           |
| SHELL   | shell 程序的名字。                                           |
| HOME    | 用户家目录。                                                 |
| LANG    | 定义了字符集以及语言编码方式。                               |
| OLD_PWD | 先前的工作目录。                                             |
| PAGER   | 页输出程序的名字。这经常设置为/usr/bin/less。                |
| PATH    | 由冒号分开的目录列表，当你输入可执行程序名后，会搜索这个目录列表。 |
| PS1     | Prompt String 1. 这个定义了你的 shell 提示符的内容。随后我们可以看到，这个变量 内容可以全面地定制。 |
| PWD     | 当前工作目录。                                               |
| TERM    | 终端类型名。类 Unix 的系统支持许多终端协议；这个变量设置你的终端仿真器所用的协议。 |
| TZ      | 指定你所在的时区。大多数类 Unix 的系统按照协调时间时 (UTC) 来维护计算机内部的时钟 ，然后应用一个由这个变量指定的偏差来显示本地时间。 |
| USER    | 你的用户名                                                   |



#### set    检查所有变量

 当使用没有带选项和参数的 set 命令时，shell 变量，环境变量，和定义的 shell 函数 都会被显示。不同于 printenv 命令，set 命令的输出很友好地按照首字母顺序排列： 

```shell
set | less  #浏览变量内容

```

#### alias 使用不带参数的alias来检查别名

![](https://img-blog.csdnimg.cn/img_convert/a99833d20dc0e8f2b518e82fc591d367.png)

#### 修改shell环境

我们先返回到home目录，然后ls -a查看目录信息

```shell
cd  /home #回到家目录
ls -a #预览隐藏内容
ls /bin  #预览bin文件下内容
```

![](https://img-blog.csdnimg.cn/img_convert/4f06f0f58f23459c4688fdd0022d37f1.png)

我们会发现 ls -a 并没发现bin文件，然而ls /bin 却可以看到内容。那么，bin目录下是什么文件呢？

**bin文件为命令搜索目录，其中装了我们系统自带的一些命令程序，例如ls。**

 既然我们知道了启动文件所在的位置和它们所包含的内容，我们就可以修改它们来定制自己的 shell 环境。 

通过修改shell环境，我们可以指定自己的环境，从而更加方便的使用自己的系统（具体作用在后面）

 按照通常的规则，添加目录到你的 PATH 变量或者是定义额外的环境变量，要把这些更改放置到 .bash_profile 文件中（或者其替代文件中，根据不同的发行版。例如，Ubuntu 使用 .profile 文件）。 对于其它的更改，要放到 .bashrc 文件中。除非你是系统管理员，需要为系统中的所有用户修改 默认设置，那么则限定你只能对自己家目录下的文件进行修改。 

**修改.bashrc**

我们为了优化自己的环境，要更改.bashrc，但是为了防止弄坏系统，我们可以选择先备份一下，然后对.bashrc进行编辑。

```shell
cd ~/  #跳到主目录
ls -a #浏览目录，包括隐藏目录，查看是否有.bashrc
cp .bashrc .bashrc.bak #备份，扩展名 “.bak”、”.sav”、 “.old”和 “.orig” 都是用来指示备份文件的流行方法。
ls -a #看一下是不是已经有了 .bashrc.bak
nano .bashrc #一类文本型编辑器
```

我们会看到以下界面

![](https://img-blog.csdnimg.cn/img_convert/da041b74e2cabed4ccfb873963ef6ced.png)

其中“^”代表ctrl 

（尝试以下ctrl+x是否可以离开编辑器）

 使用下箭头按键和 / 或下翻页按键，移动 鼠标到文件的最后一行，然后添加以下几行到文件 .bashrc 中： 

```shell
#为了防止以后忘记这些设置，可以添加注释，指出功能

#设置掩码解决共享目录问题
umask 0002
#使得 shell 的历史记录功能忽略一个命令，如果相同的命令已被记录。
export HISTCONTROL=ignoredups
#增加命令历史的大小，从默认的 500 行扩大到 1000 行。
export HISTSIZE=1000
#创建一个新命令，叫做'l.'，这个命令会显示所有以点开头的目录项。
alias l.='ls -d .* --color=auto'
#创建一个叫做'll'的命令，这个命令会显示长格式目录列表。
alias ll='ls -l --color=auto'
```

然后ctrl+o保存（写入）然后ctrl+x退出，大功告成。

我们对于文件 .bashrc 的修改不会生效，直到我们关闭终端会话，再重新启动一个新的会话， 因为 .bashrc 文件只是在刚开始启动终端会话时读取。然而，我们可以强迫 bash 重新读取修改过的 .bashrc 文件，使用下面的命令：

```
[me@linuxbox ~]$ source .bashrc
```

然后试着执行一下 ll 看看效果

![](https://img-blog.csdnimg.cn/img_convert/14bae7406de888b3dfd5e294aaaf172f.png)

从而，我们实现了修改环境变量的操作。

### 14. vi和vim

vi是一种行编辑器，用来编辑命令，一句话，你可以不用，但为了不被熟练使用vi的人嘲笑，你不可以不会。

#### vi

```shell
# 一些最基础的命令

vi  #启动vi（vim），在较新的ubuntu系统中，vi往往会自动地启动vim
:q  #退出vi，注意“:”冒号也是命令一部分
:q! #如果上一个命令退出不了，这个命令就相当于强制退出
#    如果你在 vi 中“迷失”了，试着按下 Esc 键两次来回到普通模式。
```

#### 使用vi编辑

- 用vi新建文件

```shell
vi viTest.txt #在合适的位置用vi新建了一个名为viTest.txt的文件（文件名可自拟）
```

新建成功后，可以见到下列界面：

![](https://img-blog.csdnimg.cn/img_convert/dd23cc26a04979453711b4c3b397e101.png)

**注意**：vi在启动后会先进入命令模式，在该模式下几乎灭个按键都有可能是一个命令，所以不要直接开始编辑！

- 进入插入模式

  ```shell
  i #摁i进入插入模式
  ```

  我们发现左下角出现了“--INSERT--”或者“--插入--”这样的提示了，这时候我们便可以进行插入了

  试着写一些东西吧

  ```shell
  例：
  你有没有听说过范露这个女生
  Have you ever heard of Fan Lu
  ```

- 保存我们的文件：

  ```shell
  #通过使用ESC我们可以返回命令格式，然后执行保存命令
  :w  #保存文件，注意“:”也是命令一部分
  ```

- 一些其他的命令（在命令模式下）：

  ```shell
  i #插入模式
  u #撤销
  A #光标将移动到行尾，同时 vi 进入输入模式。
  0 #数字0，移动到当前行行首
  ^ #移动到当前行的第一个非空字符。
  $ #移动到当前行的末尾。
  ↑↓←→ #上下左右，可以用k j h l代替
  Ctrl-f or Page Down  #下一页
  Ctrl-b or Page Up	#上一页	
  G #文件末尾
  [数字]G #来到第[数字]行 例如1G
  dd #删除文本当前行
  [数字]dd  #删除当前行和后n-1行
  dG #从当前行到文件的末尾
  d[数字]G #从当前行到文件的第20行
  yy  #复制当前行
  [数字]yy  #复制当前行和后n-1行
  yW    #从当前光标位置到下一个单词的开头
  y$    #从当前光标位置到当前行的末尾
  y0    #从当前光标位置到行首
  yG    #复制当前行到文件末尾
  y[数字]G #复制当前行到的第20行
  p     #粘贴到当前行下
  /[单词]  #查找单词位置，用n/N查找下一个/上一个
  :s/old/new/g # 用new替换当前行所有的old。
  :n1,n2s/old/new/g # 用new替换文件n1行到n2行所有的old。
  :%s/old/new/g # 用new替换文件中所有的old。
  ```

  这里只列出了一些经常用到的vi指令，更多更详细的内容，可以了解这篇博客：[vim 操作命令大全](https://blog.csdn.net/weixin_37657720/article/details/80645991)

#### 多文件编辑

```shell
vi file1 file2 file3... #多个文件编辑，开始进入第一个文件
:n/N  #切换到下/上个文件
:buffers #显示出文件 即其编号
:buffer 编号 #切换到相应的文件
:e file #加入文件
:w #保存当前文件
:w file #保存当前文件到一个file附件

#注意多个文件之间在vi里是可以复制粘贴的
```

buffers的使用：

![](https://img-blog.csdnimg.cn/img_convert/2735512498bde8607a8d38ca9907918b.png)



### 15. 自定制shell提示符

 和 Linux 内的许多程序一样，shell 提示符是可高度配置的，虽然我们把它相当多地看作是理所当然的， 但是我们一旦学会了怎样控制它，shell 提示符是一个相当有用的工具。 

#### 解析一个提示符

例：

[me@linuxbox ~]
me ：用户名
linuxbox：主机名
~ :当前工作目录

现在使用我门学过的echo解析命令，解析一个环境变量PS1，他是用来存储提示符定义的：

```shell
echo $PS1
```

我们得到了以下结果（不同版本可能会有一些不同）

![](https://img-blog.csdnimg.cn/img_convert/53aab1d688b99b065bc2afc7c43fac57.png)

那么这些特殊字符是什么呢，根据上面的提示，我们容易看出，其中\u \h \w 分别是 用户名，主机名，目录名；

那么其他的是什么呢，这时我们就需要一个shell提示符中的转义字符表了：

| 序列 | 显示值                                                       |
| :--- | :----------------------------------------------------------- |
| \a   | 以 ASCII 格式编码的铃声 . 当遇到这个转义序列时，计算机会发出嗡嗡的响声。 |
| \d   | 以日，月，天格式来表示当前日期。例如，“Mon May 26.”          |
| \h   | 本地机的主机名，但不带末尾的域名。                           |
| \H   | 完整的主机名。                                               |
| \j   | 运行在当前 shell 会话中的工作数。                            |
| \l   | 当前终端设备名。                                             |
| \n   | 一个换行符。                                                 |
| \r   | 一个回车符。                                                 |
| \s   | shell 程序名。                                               |
| \t   | 以24小时制，hours:minutes:seconds 的格式表示当前时间.        |
| \T   | 以12小时制表示当前时间。                                     |
| \@   | 以12小时制，AM/PM 格式来表示当前时间。                       |
| \A   | 以24小时制，hours:minutes 格式表示当前时间。                 |
| \u   | 当前用户名。                                                 |
| \v   | shell 程序的版本号。                                         |
| \V   | Version and release numbers of the shell.                    |
| \w   | 当前工作目录名。                                             |
| \W   | 当前工作目录名的最后部分。                                   |
| \!   | 当前命令的历史号。                                           |
| \#   | 当前 shell 会话中的命令数。                                  |
| \$   | 这会显示一个"$"字符，除非你拥有超级用户权限。在那种情况下， 它会显示一个"#"字符。 |
| \[   | 标志着一系列一个或多个非打印字符的开始。这被用来嵌入非打印 的控制字符，这些字符以某种方式来操作终端仿真器，比方说移动光标或者是更改文本颜色。 |
| \]   | 标志着非打印字符序列结束。                                   |



#### 更改shell提示符

我们已经知道了

PS1中存储着提示符的内容，那么如果改变PS1内容，会发生什么呢？

```shell
#首先，为了防止我们无法恢复PS1，先做一个备份
ps1_bak="$PS1"
#然后查看一下，是否已经备份成功
echo "$ps1_bak"
```

![](https://img-blog.csdnimg.cn/img_convert/754bd407fc6b9ef7c1796e9cb3a3e9c9.png)

```shell
#之后如果我们想要恢复，只需要PS1="$ps1_bak"
#然后我们更改一下PS1的内容,让它为不同的值，看看shell提示符的变化
PS1= 
PS1="\a\$ "
PS1="\A \h \$ "
#可以对照着上面的表格来看这些转义符的意思
#例如最后一个例子，我们将shell提示改成了只有时间和主机名
```

![](https://img-blog.csdnimg.cn/img_convert/2863cb867525e51585fa40542a8c84d1.png)

同时，我们也可以改变shell提示符的一些其他特性，这里，我将其的转义表列出：

- 文本颜色

| 序列       | 文本颜色 | 序列       | 文本颜色 |
| :--------- | :------- | :--------- | :------- |
| \033[0;30m | 黑色     | \033[1;30m | 深灰色   |
| \033[0;31m | 红色     | \033[1;31m | 浅红色   |
| \033[0;32m | 绿色     | \033[1;32m | 浅绿色   |
| \033[0;33m | 棕色     | \033[1;33m | 黄色     |
| \033[0;34m | 蓝色     | \033[1;34m | 浅蓝色   |
| \033[0;35m | 粉红     | \033[1;35m | 浅粉色   |
| \033[0;36m | 青色     | \033[1;36m | 浅青色   |
| \033[0;37m | 浅灰色   | \033[1;37m | 白色     |



- 背景

| \033[0;40m | 蓝色 | \033[1;44m | 黑色   |
| ---------- | ---- | ---------- | ------ |
| \033[0;41m | 红色 | \033[1;45m | 紫色   |
| \033[0;42m | 绿色 | \033[1;46m | 青色   |
| \033[0;43m | 棕色 | \033[1;47m | 浅灰色 |

- 移动光标

| 转义编码  | 行动                                           |
| :-------- | :--------------------------------------------- |
| \033[l;cH | 把光标移到第 l 行，第 c 列。                   |
| \033[nA   | 把光标向上移动 n 行。                          |
| \033[nB   | 把光标向下移动 n 行。                          |
| \033[nC   | 把光标向前移动 n 个字符。                      |
| \033[nD   | 把光标向后移动 n 个字符。                      |
| \033[2J   | 清空屏幕，把光标移到左上角（第零行，第零列）。 |
| \033[K    | 清空从光标位置到当前行末的内容。               |
| \033[s    | 存储当前光标位置。                             |
| \033[u    | 唤醒之前存储的光标位置。                       |



所以我们可以设置一个酷炫的shell提示符：

```shell
PS1='\[\033[s\033[0;0H\033[0;41m\033[K\033[1;33m\t\033[0m\033[u\]
<\u@\h \W>\$ '
```

#### 储存shell提示符设置

为了保存我们的设置，不必每次开机后都要重更新蛇者一遍，可以把下面这两行添加到.bashrc 文件中。 如何保存，可以看看13章

```shell
PS1='\[\033[s\033[0;0H\033[0;41m\033[K\033[1;33m\t\033[0m\033[u\]<\u@\h \W>\$ '
export PS1
```

如此一来，我们get了自定制shell提示符的技能。



### 16. 软件包管理

软件包管理，就是使用命令行通过软件包安装软件，原书中的介绍较为官方，没有实例展示，这里我通过升级软件和实际安装一个软件包进行实际的演示。

我将以Ubuntu为例，使用 .deb 的包管理系统（适用于 Debian, Ubuntu, Xandros, Linspire 等）来演示软件包的管理。

当然如果你的系统属于 .rpm 的包管理系统（适用于 Fedora, CentOS, Red Hat Enterprise Linux, OpenSUSE, Mandriva, PCLinuxOS 等）也可以参考安装过程，来学习.rmp包管理系统的相关指令。

**注：以下命令只适用于 .deb 的包管理系统**

#### 更新软件

首先，让给我们学习一下如何更新软件：

```shell
sudo apt update  #列出所有可更新的软件清单命令
apt list --upgradeable #列出可更新的软件包及版本信息
```

首先我们利用以上命令来确认可以更新的软件：

![](https://img-blog.csdnimg.cn/img_convert/b175bae5c91e855278e34400553716b1.png)

我们可以看到，有许多的软件需要我们更新，这时，我们可以使用以下命令：

```shell
sudo apt upgrade #升级所有可以升级的软件包
```

然后开始更新:)



#### 安装软件（Aterm）

先让我们了解以下今天要安装的软件包---Aterm，他是一个外观很漂亮的终端模拟器， 这个应用程序仍然可以在标准软件库中找到，所以我们可以利用命令行安装。

```
sudo apt install <package_name> #安装
```

![](https://img-blog.csdnimg.cn/img_convert/1b32b9480e6b3eab58dc3ef252c72899.png)

选择yes,进行安装...

我们在可视化Ubuntu的应用界面发现多出来了一个新应用，说明安装已经成功。打开它，试试全新的终端吧。

（一开始会很简陋...但是可以自定义终端，可以去CSDN看一下，也可以试试guake终端模拟器，容易配置）

最终效果：

![](https://img-blog.csdnimg.cn/img_convert/589ad9af0cf37431339deede00a6e69a.png)

我们可以利用这些命令来查看aterm是否已经安装及的版本属性：

```shell
sudo apt show <package_name> #列出软件的具体信息
apt list --installed  #查找已安装的安装包
apt list --all-versions #查找所有安装包的版本信息
```

#### 其他常用功能

```shell
sudo apt remove <package_name> #移除安装包
sudo apt autoremove #移除某个软件包的不需要的依赖(其他程序的组件,帮助软件运行)
sudo apt purge <package_name> #移除安装包和其配置文件
dpkg -l | grep [关键字] #列出所有含有该关键字的应用
```



### 17. 储存媒介

略。

### 18. 网络系统

 当谈及到网络系统层面，几乎任何东西都能由 Linux 来实现。Linux 被用来创建各式各样的网络系统和装置， 包括防火墙，路由器，名称服务器，网络连接式存储设备等等。 

而我们主要学习的，包括监测网络和传输文件的命令。和远端登录ssh程序。

#### ping 验证网络连接

 ping 命令发送一个特殊的网络数据包，叫做 ICMP ECHO_REQUEST，到 一台指定的主机。大多数接收这个包的网络设备将会回复它，来允许网络连接验证。 

 **注意：**大多数网络设备（包括 Linux 主机）都可以被配置为忽略这些数据包。通常，这样做是出于网络安全 原因，部分地遮蔽一台主机免受一个潜在攻击者地侵袭。配置防火墙来阻塞 IMCP 流量也很普遍。 

让我们试试连接一个网站

```shell
ping baidu.com  #连接百度
```

![](https://img-blog.csdnimg.cn/img_convert/11e7860e4c85326edebcadeffa0e4041.png)

 一旦启动，ping 命令会持续在特定的时间间隔内（默认是一秒）发送数据包，直到它被中断  (ctrl+c可以停止）

 一个正常工作的网络会报告 零个数据包丢失。一个成功执行的“ping”命令会意味着网络的各个部件（网卡，电缆，路由，网关） 都处于正常的工作状态。 

```
0% packet loss
```

#### traceroute   （需安装程序） 显示从本地到指定主机 要经过的所有“跳数”的网络流量列表。 

```shell
traceroute [网站] #可能需要安装带有traceroute命令的程序，通过对16章软件包的安装，这点并不难
```

![](https://img-blog.csdnimg.cn/img_convert/16b8fb6a2b28b0cc226ff1512fc79d47.png)

由于现在的网站基本都有防火墙，一般看不到它们的主机名，IP 地址和性能数据（变成了三个星号） 

#### netstat （需安装程序） 检查网络设置和统计数据。 

```shell
netstat --help  #查看netstat作用
netstat -i -e #查看系统中的网卡
netstat -r #显示网络路由信息
netstat -anp | grep [端口号] #过滤出某个端口的连接
```

![](https://img-blog.csdnimg.cn/img_convert/51622a9cee8f60be20c406cb5f6c3007.png)

相关更多信息，可以通过查看手册了解

#### ftp

  ftp 程序可用来与 FTP 服务器进行通信，  FTP 服务器就是存储文件的计算机，这些文件能够通过 网络下载和上传。

**使用ftp服务需要先搭建ftp服务器，文末有搭建教程**

- 连接网站

  ```shell
  ftp [域名][ip地址] #唤醒ftp程序，连接到ftp服务器
  >ls  #在服务器下使用以下命令可以实现查看服务器下的文件
  bye #退出远端服务器
  cd  [目录] #跳转目录（远端）, 注意在大多数匿名的 FTP 服务器中，支持公共下载的文件都能在目录 pub （public）下找到
  lcd [目录] #跳转目录（本地），设置为指定目录
  get [文件] #下载文件到本地指定目录
  ```

  尝试在一个远端服务器载（待更新）：

  ```shell
  ftp 194.71.11.165  # 乌普萨拉瑞典大学计算机网络，为数不多的工共ftp服务器
  #用户名为anonymous 密码为空
  #如果ls无法查看服务器目录可以尝试解决办法：https://blog.csdn.net/sfdst/article/details/79454950
  ```

![](https://img-blog.csdnimg.cn/img_convert/c38c37f46db1a5136a01640fbde8d14f.png)

- 扩展：

> 如何搭建ftp服务器：https://blog.csdn.net/zxw136511485/article/details/79460671
>
> ftp安全部署：https://blog.csdn.net/yangkaiorange/article/details/81431520

### 



#### 第三方ftp客户端

filezilla，可以尝试一下，让操作更加简单



#### SSH

ftp程序具有使用明码形式传输信息的特点，为了解决这个问题，SSH被开发出来用于解决 两个基本的和远端主机安全交流的问题 。

因为没有两台主机，所以没办法尝试

[相关知识](https://www.jianshu.com/p/b10c2b163100)

待更新...



### 19. 查找文件

查找文件相关操作：

#### locate  查找符合条件的文档 

```shell
locate [-d ][--help][--version][范本样式...]

#例：
locate /etc/zip  #查找etc文件下的zip开头的文件
```

相关语法：[locate用法](https://www.runoob.com/linux/linux-comm-locate.html)

#### find  依据更多的属性查找文件

```shell
find   path   -option   [   -print ]   [ -exec   -ok   command ]   {} \;
#例：
find . -name "*.c" #查找当前目录的所有.c文件
```

相关语法：[find用法](https://www.runoob.com/linux/linux-comm-find.html)

### 20. 归档与备份

压缩文件相关操作：

#### gzip  压缩命令

```shell
gzip [-acdfhlLnNqrtvV][-S &lt;压缩字尾字符串&gt;][-&lt;压缩效率&gt;][--best/fast][文件...] 或 gzip [-acdfhlLnNqrtvV][-S &lt;压缩字尾字符串&gt;][-&lt;压缩效率&gt;][--best/fast][目录]
#例：
gzip a.txt #压缩当前目录下a.txt 扩展名位默认为.gz
```

相关语法：[gzip用法](https://www.runoob.com/linux/linux-comm-gzip.html)



#### Linux tar.gz、tar、bz2、zip   解压缩、压缩命令

[命令详解](https://www.runoob.com/w3cnote/linux-tar-gz.html)



#### rsync Linux远程数据同步工具

因为没有两台电脑，所以暂时无法实践

[rsync详情](https://zhuanlan.zhihu.com/p/49577967)



### 21. 正则表达式

 正则表达式(regular expression)描述了一种字符串匹配的模式（pattern），可以用来检查一个串是否含有某种子串、将匹配的子串替换或者从某个串中取出符合某个条件的子串等。 

我们可以用grep命令来帮助学习正则表达式。

#### grep  查找过滤

```shell
grep [options] regex [file...]  #在指定的文件中匹配
#其中options的命令可以通过--help查找，下面也列出了options选项，regex表示正则表达式
```

| 选项 | 描述                                                         |
| :--- | :----------------------------------------------------------- |
| -i   | 忽略大小写。不会区分大小写字符。也可用--ignore-case 来指定。 |
| -v   | 不匹配。通常，grep 程序会打印包含匹配项的文本行。这个选项导致 grep 程序只会打印不包含匹配项的文本行。也可用--invert-match 来指定。 |
| -c   | 打印匹配的数量（或者是不匹配的数目，若指定了-v 选项），而不是文本行本身。 也可用--count 选项来指定。 |
| -l   | 打印包含匹配项的文件名，而不是文本行本身，也可用--files-with-matches 选项来指定。 |
| -L   | 相似于-l 选项，但是只是打印不包含匹配项的文件名。也可用--files-without-match 来指定。 |
| -n   | 在每个匹配行之前打印出其位于文件中的相应行号。也可用--line-number 选项来指定。 |
| -h   | 应用于多文件搜索，不输出文件名。也可用--no-filename 选项来指定。 |

例子：

```shell
grep bzip dirlist.txt #在dirlist.txt中找到含有bzip的串
```

正则表达式的方式有很多，这里不一一列出，我们只说明其中一些例子

[相关正则表达式的语法](https://www.runoob.com/regexp/regexp-syntax.html)

[Linux中的正则表达式语法](https://www.linuxprobe.com/linux-regular-expression.html)

```shell
#[A-Z]表示匹配所有大写字母
ls | grep [A-Z]
#'t+est.txt' 重复t开头加上est[一个字符]txt
```

样例图片：

![](https://img-blog.csdnimg.cn/img_convert/83c20a81e043d2a499c9061fcb510095.png)

![](https://img-blog.csdnimg.cn/img_convert/a47e515c125d351bccaa825899cd15f3.png)



### 22. 文本处理

22-24为一系列文本操作，现代的文本软件可以更加便捷的处理文本；但终端命令行操作也有许多优点，以后有时间会更新。

### 23. 格式化输出

（待更新...)

### 24. 打印

（待更新...)

### 25. 编译程序

这一章学习如何通过编译(C)源代码来创建程序进行运行。

主要过程：

- 创建目录（src）
- 使用ftp协议下载源码
- 得到源码并存放在目录中
- 检查源码树并了解源码
- 编译并安装程序
- 根据帮助文档使用程序

为了完成这个操作，需要用到make命令。

#### make  维护程序

```shell
less Makefile #查看make的配置文件
make #构建当前目录下的程序
```



#### 前序-安装GCC

```shell
which gcc #查看系统安装GCC的位置，如果没有需要安装

#安装 GCC,g++,make
sudo apt update #更新列表
sudo apt install build-essential#下载安装包，包括GCC,g++,make
gcc --version #检验gcc的安装
```

更新列表：

![](https://img-blog.csdnimg.cn/img_convert/5efee3641496302fb071bd5c1fa5f5d4.png)

下载安装包（输入Y）

![](https://img-blog.csdnimg.cn/img_convert/2a263500a4f8f5e142fa2cd28b29873a.png)

最后使用gcc --version 检测是否已经安装了GCC

![](https://img-blog.csdnimg.cn/img_convert/5bdd790b38f26e8090fd46618dbc90e0.png)

#### 创建目录存放源码

![](https://img-blog.csdnimg.cn/img_convert/1be1a43cb0eaa5f0ac674faa68fdf68f.png)

#### 使用ftp下载diction源码

我们将编译一个叫做 diction 的程序，来自 GNU 项目。这是一个小巧方便的程序， 检查文本文件的书写质量和样式。就程序而言，它相当小，且容易创建。

![](https://img-blog.csdnimg.cn/img_convert/960b709eec09929601244ca0d9453ece.png)

成功登录后按操作顺序依次在ftp>输入以下命令

![](https://img-blog.csdnimg.cn/img_convert/a136f20809b846a5a52a9f84800f8cb3.png)

解压diction包

```shell
tar xzf [压缩包]  #解压程序命令，此处diction-1.11.tar.gz
```

**tip:**

diction像所有的 GNU 项目软件，遵循着一定的源码打包标准。该标准的一个条目是，当源码 tar 文件打开的时候，会创建一个目录，该目录包含了源码树， 并且这个目录将会命名为 project-x.xx，其包含了项目名称和它的版本号两项内容。这种方案能在系统中方便安装同一程序的多个版本。 然而，通常在打开 tarball 之前检验源码树的布局是个不错的主意。一些项目不会创建该目录，反而，会把文件直接传递给当前目录。 这会把你的（除非组织良好的）src 目录弄得一片狼藉。为了避免这个，使用下面的命令，检查 tar 文件的内容：

```shell
tar tzvf {压缩包] | head ---
```

#### 检察源码树

![](https://img-blog.csdnimg.cn/img_convert/fa5673719cab00aac534334625d308d1.png)

#### 打开diction文件并预览diction.c了解代码

![](https://img-blog.csdnimg.cn/img_convert/5a21f18c1da984b5d5948e826e71f42c.png)

其中.c文件的头文件在源码树的外面，具体内容可以在/usr/include 目录看到他们。（安装编译器的时候，目录的头文件就被安装了）

#### 构建程序

```shell
./configure  #分析程序构建环境
#没有错误信息则可以进行构建
make  #使用Makefile文件指导其行为，最终会产生很多信息。
```

使用make程序结束后，使用less程序可以看到文件中多出的目标文件。完成了源码编译文件。

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-JFXjIGYr-1617349513932)(C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1615430074359.png)]

**注意：** make命令只会构建需要构建的部分，即丢失可以补充的文件和可以更新的文件。

#### 安装程序

打包良好的源码经常包括一个特别的 make 目标文件，叫做 install。这个目标文件将在系统目录中安装最终的产品，以供使用。

我们通常使用以下操作来安装：

```shell
sudo make install
```

查看是否安装

```shell
which diction  #查看安装位置
man diction  #查看diction手册
```

#### 程序的使用

以安装的diction为例，我们通过查看（man命令）文档得知其用法：

![](https://img-blog.csdnimg.cn/img_convert/89b63dd8777aef3d8cf3eac90c41a297.png)

由diction的使用文档可知，这个程序是用来处理文章句子的，其中的-s选项可以为我们提供词更好的使用建议，所以我们执行并尝试一下。

```shell
diction -s dtest.txt  #dtest.txt 是提前准备好的一篇英语小文可以供diction程序使用
```

![](https://img-blog.csdnimg.cn/img_convert/132f966cc560dfed28298ff4a94bf6ba.png)

我们可以看到很多对文本单词的使用建议，比如may不要和can混淆等。

其他功能也可以尝试一下。（diction支持德语和英语，中文暂不支持）

至此，我们最终实现了程序的diction源码的下载，编译和安装和使用。



### 26. Shell脚本

Shell脚本，就是包含一系列命令的文件。通过shell读取文件然后执行命令，实现各类功能。

#### 脚本语言编写流程：

- 编写脚本 （使用vim等）
- 设置脚本文件权限使其可执行
- 放置脚本到shell执行目录

#### 编写脚本

我们建立一个hello_world文档并作为我们的第一个脚本

使用vim进行编辑

```shell
touch hello_world
vi hello_world
```

在文件中，我们插入如下文本：

```shell
#!/bin/bash
# This is our first script.
echo 'Hello World!'
```

其中第一行尤为重要，它用来表明该文档要使用什么样的脚本语言来解释。

编辑好后，保存文件。

#### 设置可执行权限

为文件设置可执行权限可以使用 chmod命令。

![](https://img-blog.csdnimg.cn/img_convert/8025572e9dec13ceaf43eae9c3a73c49.png)

我们可以通过 ls -l命令看到，通过使用chmod 755 hello_world，hello_world文件已经变成了可执行的文件（‘x’代表执行）

其中的chmod命令具体用法，可以参考[chmod命令详解](https://www.runoob.com/linux/linux-comm-chmod.html)

#### 设置脚本位置

将hello_world文件设置为可执行后可以通过以下命令执行文件

```shell
./hello_world   #执行当前目录下的hello_world
```

但是像ls这样的命令，是没有表明目录的，而我们如果直接执行hello_world显然是不行的，所以我们需要将其移动到合适的目录，让shell执行命令的时候，找到这个默认目录，就可以直接执行了。

我们讨论了过PATH 环境变量及其在系统 查找可执行程序方面的作用。回顾一下，如果没有给出可执行程序的明确路径名，那么系统每次都会 搜索一系列的目录，来查找此可执行程序。这个/bin 目录就是其中一个系统会自动搜索的目录。 这个目录列表被存储在一个名为 PATH 的环境变量中。这个 PATH 变量包含一个由冒号分隔开的目录列表。 我们可以查看 PATH 的内容： 

```shell
echo $PATH
```

我们通古配置PATH 变量，让我们在主目录下建立的bin文件可以作为shell执行的一个默认目录

```shell
cd #返回主目录
mkdir bin #创建bin目录（在主目录下）
export PATH=./bin:$PATH  #配置PATH(临时生效，重新打开中断后失效)
mv hello_world的地址 bin #接下来使用mv命令将你创建的hello_world文件移动到这里，就可以直接使用hello_world了
hello_world  #直接执行
```

长期保留一个PATH可以vim ~/.bashrc 这里不再赘述，可以自行百度如何添加长期变量



### 27. 脚本设计

我们将要编写是一个报告生成器程序。它会显示系统的各种统计数据和它的状态，并将产生 HTML 格式的报告， 所以我们能通过网络浏览器，比如说 Firefox 或者 Konqueror，来查看这个报告。

####  简单的项目

首先我们建立一个print_file文件

并输入以下内容（通过vim完成）

```shell
#!/bin/bash
# Program to output a system information page
echo "<HTML>
    <HEAD>
          <TITLE>Page Title</TITLE>
    </HEAD>
    <BODY>
          Page body.
    </BODY>
</HTML>"
```

然后使得文件可执行并执行该程序

```shell
chmod 755 ~/bin/print_file
print_file
```

#### 变量

我们来稍微更改一下文本来体会变量的作用

```shell
#!/bin/bash
# Program to output a system information page
title="System Information Report"
echo "<HTML>
        <HEAD>
                <TITLE>$title</TITLE>
        </HEAD>
        <BODY>
                <H1>$title</H1>
        </BODY>
</HTML>"
```

保存好启动程序，我们可以看到，title变量的作用。

当我们需要代码中重复引用时，带入变量是个很好的结局方案。

**变量使用注意：**

1. 变量名可由字母数字字符（字母和数字）和下划线字符组成。
2. 变量名的第一个字符必须是一个字母或一个下划线。
3. 变量名中不允许出现空格和标点符号。
4. 当我们使用变量遇到更加复杂的情况时，可以利用${变量名} 来表示{}内是个变量，那么变量就可以和文本自由组合了

我们可以利用变量,即创建包括的日期和时间，以及创建者的用户名：

```shell
#!/bin/bash
# Program to output a system information page
TITLE="System Information Report For $HOSTNAME"
CURRENT_TIME=$(date +"%x %r %Z")
TIME_STAMP="Generated $CURRENT_TIME, by $USER"
echo "<HTML>
        <HEAD>
                <TITLE>$TITLE</TITLE>
        </HEAD>
        <BODY>
                <H1>$TITLE</H1>
                <P>$TIME_STAMP</P>
        </BODY>
</HTML>"
```

其中可将HOSTNAME定义为用户名

最终效果：

![](https://img-blog.csdnimg.cn/img_convert/46c1eabd1080dd1d1fe5e2eaa62a2b7f.png)



我们利用>操作符print_file内容输出，并用firefox打开：

```shell
print_file > print_file.html
firefox print_file.html
```

####  here document 输入方法

为了更加方便地编辑脚本，我们可以利用here document  文本输出方法 

```
command << token
```

 这里的 command 是一个可以接受标准输入的命令名，token 是一个用来指示嵌入文本结束的字符串。 

所以上面的文档我们也可以这样写：

```shell
#!/bin/bash
# Program to output a system information page
TITLE="System Information Report For $HOSTNAME"
CURRENT_TIME=$(date +"%x %r %Z")
TIME_STAMP="Generated $CURRENT_TIME, by $USER"
cat << _EOF_
<HTML>
         <HEAD>
                <TITLE>$TITLE</TITLE>
         </HEAD>
         <BODY>
                <H1>$TITLE</H1>
                <P>$TIME_STAMP</P>
         </BODY>
</HTML>
_EOF_
```

这样的写法取代 echo 命令，现在我们的脚本使用 cat 命令和一个 here document。这个字符串\_EOF\_（意思是“文件结尾”， 一个常见用法）被选作为 token，并标志着嵌入文本的结尾。注意这个 token 必须在一行中单独出现，并且文本行中 没有末尾的空格。 

这样写的好处是我们可以在文档中随意使用""符号，不必担心echo"" 这样的输出带来的不便。

其中cat << \_EOF\_也可以写成cat<<-\_EOF\_ 这样将缩进脚本地tab行，增加可读性。

例：

![](https://img-blog.csdnimg.cn/img_convert/af3b1f0e26656eadcf2c1d953b3626fa.png)

同样的，我们可以利用这样的脚本设计，进行各种命令行的操作。

例如我们可以编写一个使用firefpx打开刚才的文件的脚本

```shell
 #!/bin/bash
 firefox $(print_file)
```



#### 自顶向下设计

为了进一步开发我们的报告产生器脚本，使得脚本更加复杂，我们将采用自顶向下（先确定上层步骤，再逐步细化步骤）的设计方法。

我们首先看看对于我们已经设计的脚本，他现在可以做什么：

- 设置网页标题
- 关闭网页标头
- 打开网页主体部分
- 输出网页标头
- 输出时间戳

接下来要在时间戳下面加入：

- 系统正常运行时间和负载。这是自上次关机或重启之后系统的运行时间，以及在几个时间间隔内当前运行在处理 中的平均任务量。
- 磁盘空间。系统中存储设备的总使用量。
- 家目录空间。每个用户所使用的存储空间使用量。

```shell
#!/bin/bash
# Program to output a system information page
TITLE="System Information Report For $HOSTNAME"
CURRENT_TIME=$(date +"%x %r %Z")
TIME_STAMP="Generated $CURRENT_TIME, by $USER"
cat << _EOF_
<HTML>
    <HEAD>
        <TITLE>$TITLE</TITLE>
    </HEAD>
    <BODY>
        <H1>$TITLE</H1>
        <P>$TIME_STAMP</P>
        $(report_uptime)
        $(report_disk_space)
        $(report_home_space)
    </BODY>
</HTML>
_EOF_
```

要加入这些功能,我们可以先编写三个脚本，然后通过命令的方式引用他们，同时我们也可以把这些脚本作为shell函数嵌入我们的程序。

#### shell函数

- shell函数的建立

```shell
#第一种方法
function name {
    commands
    return
}
#第二种方法
name () {
    commands
    return
}
```

- 函数的使用：

函数在定义的时候是不会被使用的，但我们可以在定义后在脚本内以命令的形式直接引用他们。

```shell
funct_1   #函数的引用	
```

除了函数之外，我们还需要了解一下内容：

#### 局部变量

```shell
#定义
funct_1 ()
{
local foo=1
}
```

当我们在函数内定义一个局部变量时，它只能在函数内有定义。

接下来，让我们添加进去这三个函数到我们的脚本：

```shell
#输出启动时间
report_uptime () {
  cat <<- _EOF_
  <H2>System Uptime</H2>
  <PRE>$(uptime)</PRE>
  _EOF_
  return
}
#查看磁盘使用情况并输出
report_disk_space () {
  cat <<- _EOF_
  <H2>Disk Space Utilization</H2>
  <PRE>$(df -h)</PRE>
  _EOF_
  return
}
#这个函数查看文件大小
report_home_space () {
  cat <<- _EOF_
  <H2>Home Space Utilization</H2>
  <PRE>$(du -sh /home/*)</PRE>
  _EOF_
  return
}
```

![](https://img-blog.csdnimg.cn/img_convert/bc08f9517c832e8df9ca98dc6f0a08a1.png)

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-hioxCyjc-1617349513937)(C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1617281328652.png)]

最后执行以下命令可以在预览器里打开:

```shell
print_file>print_file.html
firefox print_file.html
```



### 29. 流程控制（读取/if  while/until  case  for）

#### 读取键盘输入(read)

我们需要利用下面的命令：

```shell
read [-option] [variable...]
read it #读入it并作为一个变量
read it1 it2 it3 it4 #读入多个变量
```

| 选项         | 说明                                                         |
| :----------- | :----------------------------------------------------------- |
| -a array     | 把输入赋值到数组 array 中，从索引号零开始。我们 将在第36章中讨论数组问题。 |
| -d delimiter | 用字符串 delimiter 中的第一个字符指示输入结束，而不是一个换行符。 |
| -e           | 使用 Readline 来处理输入。这使得与命令行相同的方式编辑输入。 |
| -n num       | 读取 num 个输入字符，而不是整行。                            |
| -p prompt    | 为输入显示提示信息，使用字符串 prompt。                      |
| -r           | Raw mode. 不把反斜杠字符解释为转义字符。                     |
| -s           | Silent mode. 不会在屏幕上显示输入的字符。当输入密码和其它确认信息的时候，这会很有帮助。 |
| -t seconds   | 超时. 几秒钟后终止输入。若输入超时，read 会返回一个非零退出状态。 |
| -u fd        | 使用文件描述符 fd 中的输入，而不是标准输入。                 |

命令详解可以查看[read详解](https://www.runoob.com/linux/linux-comm-read.html)

#### IFS 分隔符

read默认是空格为分割符，即输入1 2 3，就将1,2,3分别赋值给了三个变量，这是由IFS控制的，当我们需要用其他 符号作为分隔符的时候我们只需要在脚本的开头加入IFS的值就可以。

设置：

![](https://img-blog.csdnimg.cn/img_convert/852a6e1cd024195bbd3000b73aa46fdf.png)

效果：

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-q1qdcxkq-1617349513938)(C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1617285446087.png)]

#### if

```shell
#语法
if [condition];
then
commands
fi
```



#### while/until循环

基本语法：

```shell
while condition; do commands; done
```

例：

```
#!/bin/bash
count=1
while [ $count -le 5 ]; do
    echo $count
    count=$((count + 1))
done
echo "Finished."
```

其中的$count -le 5 意思时count小于等于5

“[ ]”里的内容只要是真的就可以一直运行。

更多while运用[while的应用详解](https://www.linuxprobe.com/shells-while-statement.html)

#### break和continue

```shell
break #跳出循环
continue #进行下一次循环	
```

#### until 

与while不同是，只有遇到条件是真的时候才会跳出

```
#!/bin/bash
# until-count: display a series of numbers
count=1
until [ $count -gt 5 ]; do
    echo $count
    count=$((count + 1))
done
echo "Finished."
```

#### case

```
case word in
    [模式 [| 模式]...) commands ;;]...
esac
```

| 模式         | 描述                                                         |
| :----------- | :----------------------------------------------------------- |
| a)           | 若单词为 “a”，则匹配                                         |
| [[:alpha:]]) | 若单词是一个字母字符，则匹配                                 |
| ???)         | 若单词只有3个字符，则匹配                                    |
| *.txt)       | 若单词以 “.txt” 字符结尾，则匹配                             |
| *)           | 匹配任意单词。把这个模式做为 case 命令的最后一个模式，是一个很好的做法， 可以捕捉到任意一个与先前模式不匹配的数值；也就是说，捕捉到任何可能的无效值。 |

例子：

```shell
case $REPLY in
    0)  echo "Program terminated."
        exit
        ;;
    1)  echo "Hostname: $HOSTNAME"
        uptime
        ;;
    2)  df -h
        ;;
    3)  if [[ $(id -u) -eq 0 ]]; then
            echo "Home Space Utilization (All Users)"
            du -sh /home/*
        else
            echo "Home Space Utilization ($USER)"
            du -sh $HOME
        fi
        ;;
    *)  echo "Invalid entry" >&2
        exit 1
        ;;
esac
```



#### for

语法结构：

```shell
for variable [in words]; do
    commands
done
```

variable是一个变量的名字。

words 是一个可选的条目列表， 其值会按顺序赋值给 variable，commands 是在每次循环迭代中要执行的命令。 

例子：

```shell
for i in A B C D; do echo $i; done
```

```
结果：
A
B
C
D
```

更多内容可以看以下[for详解](https://blog.csdn.net/magi1201/article/details/75195983)

### 30. 字符串，数字运算，数组

#### 字符串

最基本的，我们可以利用参数展开的形式，来实现展开一个字符串。

```shell
${a}  #参数展开
```

但我们对参数展开有更多的做法：

```shell
${parameter:-word} #若parameter存在则展开结果为parameter，反之则是word
${parameter:=word} #展开结果与上面相同，特殊的是若parameter不存在word会赋值给parameter
${parameter:?word} #若parameter不存在，则会发送错误，同时会发送word
${parameter:+word} #若parameter不存在，则展开结果为空，否则会返回word（不展开）
${#parameter}	#返回字长度
${parameter:offset:length} #从第offset数开始，展开length长度
${parameter#pattern}#清除开头一部分文本，这些字符要匹配定义的 pattern
${parameter##pattern}#清楚最长长度的匹配上pattern的结果
${parameter%pattern}# 类似于${parameter#pattern}的操作但是从尾开始
${parameter%%pattern}#类似
#可对照下面来理解
```

![](https://img-blog.csdnimg.cn/img_convert/c830a886064b04d7b7d2fdc909f148d0.png)

![](https://img-blog.csdnimg.cn/img_convert/bd389c59aa39a957c397962fd1874cc3.png)

以及替换再展开操作：

```shell
${parameter/pattern/string} #匹配parameter的pattern用string代替（只代替第一个）
${parameter//pattern/string} #匹配parameter的pattern用string代替（全部）
${parameter/#pattern/string} #匹配parameter的pattern用string代替（要求pattern出现在开头）
${parameter/%pattern/string} #匹配parameter的pattern用string代替（要求pattern出现在末尾）
```

![](https://img-blog.csdnimg.cn/img_convert/e0d924f9edab62b15b4d297ecd96768f.png)

以及其他一些操作：

| 格式           | 结果                                                        |
| :------------- | :---------------------------------------------------------- |
| ${parameter,,} | 把 parameter 的值全部展开成小写字母。                       |
| ${parameter,}  | 仅仅把 parameter 的第一个字符展开成小写字母。               |
| ${parameter^^} | 把 parameter 的值全部转换成大写字母。                       |
| ${parameter^}  | 仅仅把 parameter 的第一个字符转换成大写字母（首字母大写）。 |

这些操作都可以应用在脚本中，增加可用性和便利性。

#### 算术求值和展开

```shell
$((expression)) #算数展开的基本格式
```

关于shell中算数的一些基本规则，基本和其他语言相同：

| 表示法          | 描述                                                         |
| :-------------- | :----------------------------------------------------------- |
| number          | 默认情况下，没有任何表示法的数字被看做是十进制数（以10为底）。 |
| 0number         | 在算术表达式中，以零开头的数字被认为是八进制数。             |
| 0xnumber        | 十六进制表示法                                               |
| **base#number** | number 以 base 为底 例如 $((14#16)) 表示16的14进制           |

| 运算符 | 描述         |
| :----- | :----------- |
| +      | 加           |
| -      | 减           |
| *      | 乘           |
| /      | 整除         |
| ****** | 乘方         |
| %      | 取模（余数） |

| 表示法             | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| parameter = value  | 简单赋值。给 parameter 赋值。                                |
| parameter += value | 加。等价于 parameter = parameter + value。                   |
| parameter -= value | 减。等价于 parameter = parameter – value。                   |
| parameter *= value | 乘。等价于 parameter = parameter * value。                   |
| parameter /= value | 整除。等价于 parameter = parameter / value。                 |
| parameter %= value | 取模。等价于 parameter = parameter % value。                 |
| parameter++        | 后缀自增变量。等价于 parameter = parameter + 1 (但，要看下面的讨论)。 |
| parameter--        | 后缀自减变量。等价于 parameter = parameter - 1。             |
| ++parameter        | 前缀自增变量。等价于 parameter = parameter + 1。             |
| --parameter        | 前缀自减变量。等价于 parameter = parameter - 1。             |

| 运算符 | 描述                                         |
| :----- | :------------------------------------------- |
| ~      | 按位取反。对一个数字所有位取反。             |
| <<     | 位左移. 把一个数字的所有位向左移动。         |
| >>     | 位右移. 把一个数字的所有位向右移动。         |
| &      | 位与。对两个数字的所有位执行一个 AND 操作。  |
| \|     | 位或。对两个数字的所有位执行一个 OR 操作。   |
| ^      | 位异或。对两个数字的所有位执行一个异或操作。 |

| 运算符            | 描述                                                         |
| :---------------- | :----------------------------------------------------------- |
| <=                | 小于或相等                                                   |
| >=                | 大于或相等                                                   |
| <                 | 小于                                                         |
| >                 | 大于                                                         |
| ==                | 相等                                                         |
| !=                | 不相等                                                       |
| &&                | 逻辑与                                                       |
| \|\|              | 逻辑或                                                       |
| expr1?expr2:expr3 | 条件（三元）运算符。若表达式 expr1 的计算结果为非零值（算术真），则 执行表达式 expr2，否则执行表达式 expr3。 |

但是shell是不支持小数的，此时我们可以借助于Linux的一些命令

当我们进行更加复杂的运算时，我们可以利用Linux中自带的bc运算命令

```shell
bc #启动bc
quit #退出bc
```

![](https://img-blog.csdnimg.cn/img_convert/49aed0a01c5cbf270d49e2cd6cf17628.png)

通过引用命令的方式将其放在脚本中，可以实现更加多的算数操作：

```shell
bc <<- _EOF_
	2*1.5
_EOF_
```

#### 数组

```shell
#创建：
a[1]=2  #直接创建，此时除了a[1]外的元素为空且不占空间，a[1]是2
a=(1 2 3) #a[0]=1,a[1]=2,a[2]=3
a=("12" "12 3" "1")#a[0]=12,a[1]=12 3,a[2]=1
declare -A a #通过命令创建
#赋值
a[2]=sad #a[2]的值变为sad
```

访问数组：

![](https://img-blog.csdnimg.cn/img_convert/403c81ef7f802bd7926f7cb8b7ee1a7c.png)

通过这个脚本，我们可以实现一个简单的访问数组的功能。

![](https://img-blog.csdnimg.cn/img_convert/c037e3771c784f1dc821b40a8f37a52f.png)

*和@在数组访问的时候也有很多的用处，他们表示将整个数组的每个元素遍历,但用法不太相同

我们可以通过例子来验证：
![](https://img-blog.csdnimg.cn/img_convert/766afc205bac5f3c1e12de52a7d64117.png)

结果为：

![](https://img-blog.csdnimg.cn/img_convert/771102111462beb9f6327100f8e3af7b.png)

当不对数组加引号的时候，*和@都会遍历所有数组的所有元素，但当讲了引号，他们的表现则不太一样。

测量数组的大小长度：

```shell
${#a[@]} #返回数组的长度
${#a[100]}#返回a[100]的元素长度 
```

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-xdn1Ek2y-1617349513943)(C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1617347602115.png)]



我们发现，当我们测量数组的大小的时候，他只会计算有所有已经有值的下标，说明其他下标并不占空间。



找到使用的下标：

```shell
${!array[@]}  #返回所有有值的下标
${array[@]} #返回所有的值
```

![](https://img-blog.csdnimg.cn/img_convert/10b9afa741b9bb9eeabbb319b1a4e568.png)



数组后加元素

```shell
v+=(1 2 3) #在最后一个下标后加上1 2 3三个元素
```



数组排序

```shell
for i in "${v[@]}"; do echo $i; done | sort #将其输出的值用sort命令排序后再展开，从而实现排序
```

![](https://img-blog.csdnimg.cn/img_convert/7b445d37af62bbf18dd970361eeda8ca.png)



删除数组

```shell
unset v #删除数组v
unset v[100] #删除v[100]
```

#### 关联数组

bash提供的数组新的特性

```shell
declare -A colors
colors["red"]="#ff0000"
colors["green"]="#00ff00"
colors["blue"]="#0000ff"
```

那么当我们这么做时：

```shell
echo ${colors["blue"]}
#或者
echo ${colors[blue]}
#则会输出
#0000ff
```





### Tips

1. **快捷按键**

按键	行动
Ctrl-a	移动光标到行首。
Ctrl-e	移动光标到行尾。
Ctrl-f	 光标前移一个字符；和右箭头作用一样。
Ctrl-b	光标后移一个字符；和左箭头作用一样。
Alt-f	  光标前移一个字。
Alt-b	 光标后移一个字。
Ctrl-l	 清空屏幕，移动光标到左上角。clear 命令完成同样的工作。

Ctrl-d	删除光标位置的字符。
Ctrl-t	 光标位置的字符和光标前面的字符互换位置。
Alt-t	  光标位置的字和其前面的字互换位置。
Alt-l	  把从光标位置到字尾的字符转换成小写字母。
Alt-u	 把从光标位置到字尾的字符转换成大写字母。


Ctrl-k	剪切从光标位置到行尾的文本。
Ctrl-u	剪切从光标位置到行首的文本。
Alt-d	  剪切从光标位置到词尾的文本。
Alt-Backspace	剪切从光标位置到词头的文本。如果光标在一个单词的开头，剪切前一个单词。
Ctrl-y	 把剪切环中的文本粘贴到光标位置。

自动补全
tab键
路径名自动补全，这是最常用的形式。自动补全也能对变量（如果 字的开头是一个”$”）、用户名字（单词以”~”开始）、命令（如果单词是一行的第一个单词） 和主机名（如果单词的开头是”@”）起作用。主机名自动补全只对包含在文件/etc/hosts 中的主机名有效。
注意，补全只有当可以由前面的字母确定其后是什么才可以生效

按键  	行动
Alt-?	显示可能的自动补全列表。在大多数系统中，你也可以完成这个通过按 两次 tab 键，这会更容易些。
Alt-*	插入所有可能的自动补全。当你想要使用多个可能的匹配项时，这个很有帮助。

2. wc

```shell
 wc file #输出行数 字数 字节数
```

3.  算术操作符

| 操作符 | 说明                                                       |
| :----- | :--------------------------------------------------------- |
| +      | 加                                                         |
| -      | 减                                                         |
| *      | 乘                                                         |
| /      | 除（但是记住，因为展开只是支持整数除法，所以结果是整数。） |
| %      | 取余，只是简单的意味着，“余数”                             |
| **     | 取幂                                                       |

4. clear － 清空屏幕

5. history － 显示历史列表内容

[其他的知识](http://billie66.github.io/TLCL/book/chap37.html)

如有写的不对的地方，非常欢迎指出，感谢！