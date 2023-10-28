## VS Code 

### 一些有用的插件

#### emotion / tailwind / css module

安装 `Tailwind CSS IntelliSense` 和 `vscode-styled-components`  和 `clinyong.vscode-css-modules` 插件后，可以分别在className和emotion的模板字符串中得到拼写提示和高亮提示。

#### 特殊标签高亮

安装 `TODO Highlight` 插件后，可以使用以下注释来标注代码块，会有高亮提示。

```jsx
// 带有特殊标记 FEAT: TODO: FIXME: 都会高亮

// FEAT: 此处代码创建数据集业务

{
    /* TODO: 这部分模板渲染还需要...*/
}

/**
 * FIXME: 待修复...
 */
```

通过 ⌘ + p 调出快速启动后，输入`>list` 找到该插件相关的选项，回车或点击后，会在 output 中输出 list，快速定位问题或功能。

#### 拼写提示

如果你怕拼错单词，安装 `Code Spell Checker` 插件。

#### svg 预览

安装 svg 插件后可以实时预览 svg 对应的图片。

### extensions 的妙用让团队项目更加规范

在 `.vscode` 目录新建 `extensions.json`，在其中写上希望团队一起使用的插件 id：

```json
{
    "recommendations": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "styled-components.vscode-styled-components",
        "wayou.vscode-todo-highlight",
        "bradlc.vscode-tailwindcss",
        "clinyong.vscode-css-modules",
        "streetsidesoftware.code-spell-checker",
        "jock.svg"
    ]
}
```

这样其他成员在下载新的仓库项目时，可以根据你的配置在扩展出按照提示下载对应的插件。（插件 id 可以在插件列表右键 `Copy Extention ID` ）



## GoLand

### Tag 模板

在 Go 项目中，我们经常需要写一些 tag 来满足框架需求，而基础的 tag 提示只有 `json`，`bson` 等。

我们可以使用在 `Settings` 中配置 tag 模板的方式来拓展更多的 tag 提示：

在 GoLand 中，你可以通过以下步骤来配置自定义的标签（tag）书写提示：

1. 打开 GoLand，点击顶部菜单栏的`GoLand` ->  `Settings`。

2. 在打开的设置窗口中，选择 `Editor` -> `Template Group` -> 新建 `My Templates`。

3. 点击新建的模板，点击右上角的 `+` 按钮，选择 `Live Template`。

4. 在弹出的窗口中，填写你的自定义标签。例如，你可以在 `Abbreviation` 中填写标签的简写，然后在 `Template text` 中填写标签的完整形式（例如 `example:"$END$"`）。你还可以在 `Description` 中填写这个标签的描述。

5. 在 `Define` 部分，选择 `Go` -> `tag` 和 `tag literal`。

6. 我们也可以使用匹配符让 tag 有更灵活的提示：例如 `validate:"$FIELD_NAME$"`，右侧点击 `Edit Variables` 来更改其展示效果。[Edit Template Variables dialog 说明文档](https://www.jetbrains.com/help/go/2023.2/edit-template-variables-dialog.html#controls)

7. 点击 `OK` 保存你的设置。

#### 将tag模板分享给他人

1. 打开 GoLand，点击顶部菜单栏的 `File` -> `Manage IDE Settings` -> `Export Settings...`。‎
2. 仅勾选 `Live templates` -> OK
3. 将 zip 文件分享给他人，在 `File` -> `Manage IDE Settings` -> `Import Settings...` 处引入配置。