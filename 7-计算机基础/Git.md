### git

```git
git config --global user.name aei   //配置username,因为设置了全局配置，所以只配置一次就行
git config --global user.email 3035816700@qq.com 
git config --list   //查看
git init   //初始化git仓库
git status //查看文件状态
git add 文件列表  //添加到暂存区
git add .  //添加全部文件
git commit -m 提交信息   //向仓库提交代码
git log    //查看提交历史记录
git checkout 文件名 //将暂存区中的文件覆盖先在的文件
git rm --cached 文件名 // 从索引中删除文件。但是本地文件还存在， 只是不希望这个文件被版本控制。
git rm 文件名 //删除文件，并且删除索引

git reset --hard  提交id //将一个项目回复到某次提交的时间线上

git branch   //查看分支
git branch  分支名称 //根据当前分支创建分支
git checkout 分支名称  //切换分支，在切换分支的时候必须要提交当前分支或者暂时保存更改才能切换，不然会出现问题
git merge  分支名称 //合并分支  将你输入的分支合并到当前分支
git branch -d 分支名称 //删除分支，注意1：不能在分支内删除该分支，只能在别的分支删除该分支 2：没有被合并的分支只能通过强制删除（-D）来删除
git branch -D 分支名称 //强制删除


git stash  //储存临时改动
git stash pop //回复改动，注意要在原来的分支恢复改动

git push 仓库地址 分支名称  //推送，推送时会储存帐号密码，之后win10系统会自动将凭据储存  
//tips:只有当前的仓库版本高于远程仓库版本才可以提交
//tips:不是项目合作作者可以直接推送，之后需要在pull request 这里发送请求
//tips:-f 强行上传

git remote add 仓库别名 仓库地址  //给仓库取别名

git clone 远程仓库地址   //克隆远程仓库

git pull 远程仓库地址 分支名称 //拉取远程仓库的新版本和当前版本合并

git pull future:dev //拉取future分支并和dev分支合并

git rebase //合并commit和分支合并
```

 git rebase的用法

[【Git】rebase 用法小结 - 简书 (jianshu.com)](https://www.jianshu.com/p/4a8f4af4e803) 

### .gitignore  这个文件用来设置不需要跟踪的文件 

### Commit规范

**综合阿里巴巴和高德地图相关部门已有的规范总结的git commit规范（转载）**

```git
Copy<type>(<scope>): <subject>
```

**type(必须)**

用于说明git commit的类别，只允许使用下面的标识。

1. feat：新功能（feature）。
2. fix/to：修复bug，可以是QA发现的BUG，也可以是研发自己发现的BUG。
   - fix：产生diff并自动修复此问题。适合于一次提交直接修复问题
   - to：只产生diff不自动修复此问题。适合于多次提交。最终修复问题提交时使用fix
3. docs：文档（documentation）。
4. style：格式（不影响代码运行的变动）。
5. refactor：重构（即不是新增功能，也不是修改bug的代码变动）。
6. perf：优化相关，比如提升性能、体验。
7. test：增加测试。
8. chore：构建过程或辅助工具的变动。
9. revert：回滚到上一个版本。
10. merge：代码合并。
11. sync：同步主线或分支的Bug。

**scope(可选)**

scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

例如在Angular，可以是location，browser，compile，compile，rootScope， ngHref，ngClick，ngView等。如果你的修改影响了不止一个scope，你可以使用*代替。

**subject(必须)**

subject是commit目的的简短描述，不超过50个字符。

- 建议使用中文（感觉中国人用中文描述问题能更清楚一些）。

- 结尾不加句号或其他标点符号。

根据以上规范git commit message将是如下的格式

```
Copyfix(DAO):用户查询缺少username属性 

feat(Controller):用户查询接口开发
```

这样规范git commit到底有哪些好处呢？

- 便于程序员对提交历史进行追溯，了解发生了什么情况。
- 一旦约束了commit message，意味着我们将慎重的进行每一次提交，不能再一股脑的把各种各样的改动都放在一个git commit里面，这样一来整个代码改动的历史也将更加清晰。
- 格式化的commit message才可以用于自动化输出Change log。



## Git

### 储藏分支

`git stash`

利用`git stash`储藏当前修改，之后就可以直接pull拉取远程分支，然后使用`git stash apply`把储藏的修改再放出来。之后再进行add，commit



### 软回退分支

git reset --soft HEAD^

HEAD是指的最新的分支，`HEAD~1`或者`HEAD^`指上一次分支。所以这个命令代表回退到上一次分支。加上`--soft`指回退一个版本的同时，将所有变更重新放回暂存区(就是add之后的区)。这样就可以对代码继续修改再进行提交分支。同时通过`git reset .`将暂存区的文件都撤销回到工作区

通常用于提交错误或者处于某种原因分支异常需要回退，同时不想丢失已修改的代码



### 新建一个分支并且切换

git checkout -b develop



### 切换远程分支并且将远程分支设为上游分支，便于push

```bash
git checkout -b branch_name origin/branch_name
git push --set-upstream origin branch_name 
```

​	之后就可以直接`git push` 来快速的push分支了





## 其他



### bind创建的函数的特殊性

[js的bind函数那些你可能没想过的点](https://cloud.tencent.com/developer/article/1399270)



### request请求中undefined的使用

在请求时在body的令某个属性为undefined，那么在发送请求的时候，body的属性就会自动去掉这个属性。



### CSS中括号的使用

标签属性选择器

      span[class='test']    =>匹配所有带有class类名test的span标签
    
      span[class *='test']  =>匹配所有包含了test字符串的class类名的span标签
    
      span[role]               =>匹配所有带有role属性的span标签
    
      [class='all']               =>匹配页面上所有带有class='all'的标签
    
      [class *='as']             =>匹配页面上所有class类且类名带有as字符串的类的标签



### 大小写规范

https://keqingrong.cn/blog/2021-05-29-case-sensitivity/



### CSS命名规范

https://juejin.cn/post/6844903672162304013



### 如何使用CSS保持盒子的横纵比

1. 使用`height: 0; padding:75%`来绘出一个4 : 3的盒子。如果需要在盒子里加内容，则盒子使用相对定位，内容盒子使用绝对定位。
2. 使用新属性`aspect-ratio`

https://juejin.cn/post/6844904070679887886



### 