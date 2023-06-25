## git工作流

为了简化操作，我们将分支分为：

- main/master：历代迭代分支
- dev：集成最新开发特性的活跃分支和发布分支（和release合并起来使用该分支）
- feat：新功能开发分支
- bug: bug修复分支 

开发流程：

```sh
git clone url #克隆分支

# 开发前
git branch dev #切换到dev分支
git pull #获取最新dev分支
git checkout -b feat/xw_1.0 #切换远程分支并且设置上游分支，便于push
git push --set-upstream origin feat/xw_1.0

# 在origin feat/xw_1.0开发后
# 如果当前分支多人开发
git stash
git pull
git stash apply

# 如果单人开发，且当前为最新版本
git add .
git commit -m 'feat: xxx'
git push

# push成功后在git采用merge request的方式向dev提PR 我们定每日晚10点前push完今天内容

# 负责人review后进行merge到dev

# 第二次开发时流程循环，不同的是新建分支为feat/xw_2.0 如果不使用版本的话，也可以直接在feat分支git pull origin dev 不新建分支

# 删除之前无用分支可以切换到其他分支使用git branch -d branch_name删除本地分支 和  git push -d branch_name 删除远程分支

# tips: 如果当天由多次提交可以最后合在一起push，如果提出PR后还想push新内容，可以在10点之前直接push，无需重复提PR
```

## commit规范

1. feat：新功能（feature）。

2. fix/to：修复bug，可以是QA发现的BUG，也可以是研发自己发现的BUG。

   - fix：产生diff并自动修复此问题。适合于一次提交直接修复问题
   - to：只产生diff不自动修复此问题。适合于多次提交。最终修复问题提交时使用fix

3. docs：文档（documentation）。

4. style：格式（不影响代码运行的变动）。

5. test：增加测试。

6. merge：代码合并。

例如：

```sh
git commit -m 'feat: 用户登录接口实现'
```

   