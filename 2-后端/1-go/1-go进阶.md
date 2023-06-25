# go学习进阶

## 线程和协程的区别

协程是用户态，属于轻量化线程，栈在kb级别，一个程序创建上万个协程是可以的。

线程属于内核态，线程跑可以跑多个协程，栈在mb级别。

## go 通道的机制

go通道通过在多个协程中建立通讯的方式来共享内存。（创建通讯来共享内存）

## GOPROXY的作用

例如：`GOPROXY="https://proxy1.cn,https://proxy2.cn,direct"`

这里代表，当我寻找依赖包的时候，`https://proxy1.cn,https://proxy2.cn`先去这两个站点去找包，如果找不到再去`direct`去找。direct代表源站，有可能是`github`，`SVN`，私有站点等。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230123161255.png)

## 使用map实现一个任意的键值对对象

通过`map[string]interface{}{...}`这样的写法，可以让map中定义的键值对，值为任意类型：

```go
map[string]interface{}{
	"xx": xx,
	"yy": yy,
}
```



## 高质量编码规范

编写质量高，易于阅读，易于维护的代码在工作中十分重要，这里列出了一些比较公认的编码规范。

### 注释

#### 什么代码需要注释？

- **公共符号注释**：公共符号一定要注释，包中声明的每个公共符号：变量，常量，函数以及结构体都需要添加注释。

- **长代码块注释**：任何既不明显也不简短的公共功能必须予以注释

- **库函数注释**：无论长度和复杂度如何，对库中的任何函数都必须进行注释
- **例外**：不需要注释实现接口的方法。例如 `func (r *FileReader) Read(Buf []byte) (int, error)` 因为该接口的使用注释应该在接口定义处已经写明了。

#### 注释应该说明什么？

- 注释应该**解释代码的作用**

- 解释代码什么情况下会出错，出什么错

  ```go
    // Mul 实现a/b的出发功能，当b为0时返回错误
    func Mul(a, b int) (err error) {
        ...
    }
  ```

- 合适注释复杂代码块的实现过程

  ```go
    // 加入凭证配置和指定加密算法，并根据自定义key生成token字符串
    c := &UserClaims{
    Name:   "aei",
    Expire: int(604800 + time.Now().Unix()), // 有效期7天
    }
    claim := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
    str, err := claim.SignedString([]byte(key))
  ```
  当然，如果一个函数名或者代码块已经很清晰的描述了其作用和使用方法，其实就没必要再加注释了：

  ```go
     func isNumber(num interface{}) bool 
  ```


- 公共符号需要注释说明：

  ```go
  // A JWT Token.  Different fields will be used depending on whether you're
  // creating or parsing/verifying a token.
  type Token struct {
  	Raw       string                 // The raw token.  Populated when you Parse a token
  	Method    SigningMethod          // The signing method used or to be used
  	Header    map[string]interface{} // The first segment of the token
  	Claims    Claims                 // The second segment of the token
  	Signature string                 // The third segment of the token.  Populated when you Parse a token
  	Valid     bool                   // Is the token valid?  Populated when you Parse/Verify a token
  }
  ```

- 代码时最好的注释，代码清晰，命名清晰最重要，其次才是通过注释提供代码未明确表达出来的信息

### 命名规范

- **变量**应该有意义，比如截止时间变量，我们使用 `deadline` 比使用 `t` 更加清晰有效；
- **函数**名应该具体简洁，不需要带上下文信息。比如 service 层的获取用户信息函数，使用 `UserInfo` 比使用 `ServiceUserInfo` 更加简洁；
- **包名**只由小写字母组成，不包含大写字母和下划线等字符，应该简短并包含一定的上下文信息，并且不使用常用变量和标准库的名字，例如使用 `userservice` 而不是 `user`

### 流程控制

流程控制中出现多个分支时，我们应该避免嵌套和冗余。例如：

```go
// 不优雅的写法
if foo {
	return x
} else {
	return err
}
// 优雅写法
if foo {
    return x
}
return nil
```

当分支比较多或者代码比较复杂时，我们应该尽早处理特殊情况或者错误情况，来尽早返回减少嵌套

```go
// 不优雅的写法
func Func() error {
    err := doSomething()
    if err == nil {
        err := doAnotherThing()
        if err == nil {
            return nil
        }
        return err
    }
    return err
}
// 优雅的写法
func Func() error {
    if err := doSomething(); err != nil {
        return err
    }
    if err := doAnotherThing(); err != nil {
        return err
    }
    return nil
}
```

### 错误处理

#### 简单错误

对于简单的自定义错误，我们可以直接使用`errors.New`返回 

````go
return errors.New("to much fish")
````

#### 复杂错误（实现错误跟踪链）

#### error

复杂的错误我们可以使用错误包装和解包。错误的包装实际上提供了一个error嵌套另一个error的能力，从而在解包时形成一个跟踪链。

在 `fmt.Errorf` 中使用 %w 关键字来进行包装

```go
var ErrDemo = errors.New("123")

func main() {
	err1 := ErrDemo
	msg := "from main"
	err2 := fmt.Errorf("error: %v %w", msg, ErrDemo)
	err3 := fmt.Errorf("error: %w %v", err2, "又一个错误")
	// errors.Is 时会自动解包，当遇到 %w 包装的 错误时，会自动找出其中的错误并解包
	fmt.Println(err1, errors.Is(err1, ErrDemo),
		"\n", err2, errors.Is(err2, ErrDemo),
		"\n", err3, errors.Is(err3, ErrDemo))
}

// 123 true
// error: "from main" 123 true
// error: error: from main 123 又一个错误 true
```

上面的例子中，我们使用  `fmt.Errorf` 即可以添加额外信息，又可以使用 `errors.Is `来判断当前 error 的具体类型

同时，我们也可以通过 `errors.As`去指定去重其中某个类型的错误。

#### panic

我们不建议在业务代码中去使用 `panic` ，因为如果调用函数不包括 `recover` 会造成程序崩溃。如果问题可以被屏蔽或解决，我们可以使用 error 实现。

但是有些最基础的功能，例如连接数据库，实现消息队列等，我们需要尽早的暴露这里面出现的错误（因为如果基础功能出现了错误，上面的业务可能大部分都用不了），此时可以使用 `panic`

### deffer

defer 语句可以尽早的写在函数前。

```go
func Func() {
    defer fmt.Printf("1")
    ...
}
```

另外，如果一个函数中出现了多个 defer 函数，defer 语句会遵循后进先出：

```go
func Func() {
    defer fmt.Printf("1")
    defer fmt.Printf("2")
}
// 2 1
```

### 代码风格

代码格式方面，我们可以使用 `gofmt` 。它作为官方提供的工具，能自动格式化Go语言代码为官方的统一风格。并且常见的 IDE 都内置或具有相关的插件，可以很方便的配置。

另一方面我们也可以使用 Go 语言官方提供的工具 `goimports`，实际等于 `gofmt` 加上依赖包管理，可以自动增删依赖的包引用，将依赖包按字母排序并分类。

Goland 已经内置了改工具，我们可以在 Setting -> Tools -> Actions on Save  中找到 `Reformat code` 和 `Optimize imports` 并勾选上来开启相关功能。在 Setting -> Editor -> Code Style -> Go 找到 Imports 下的 排序风格来选择使用 `gofmt` 还是  `goimports`

当然 Goland 一般都已经把这些提前配置了，个人更推荐使用 `goimports` 管理包引用，而代码风格，引入风格等都使用 `gofmt`



## 性能优化

### 性能基准测试 

go本身提供了性能基准测试框架 `Benchmark`，它可以利用反复调用，来实现性能测试效果，具体使用在前面的测试笔记中有提到。

### slice优化

1. 提前设定容量

   我们应该尽可能的在使用 `make()` 初始化切片的时候提供容量信息：

   ```go
   arr := make([]int, 0, 20)
   ```

   因为当切片容量不够的时候，go内部会进行 `×2` 的扩容操作，这里会有划分地址和内存的操作，为了不影响性能，我们应该在使用之前就设定好容量值。

2. 及时释放大内存切片

   在已有切片的基础上创建切片，不会创建新的底层数组，此时如果原切片很大，其内存就得不到即时的释放。此时我们可以使用copy函数创建新的底层数组。

   ```go
   arr := originArr[98:100] // 不会去创建新底层数组，originArr底层的整个数组依然会保持引用状态
   
   // 优化写法
   arr := make([]int, 2)
   copy(arr, originArr[98:100])
   ```

### map优化

1. 提前设定容量（不断添加元素会触发map扩容）

   ```go
   data := make(map[int]string, 100)
   ```

### strings.Builder

对常见的字符串操作，我们可以使用 `strings.Builder` 来提升性能

```go
var builder strings.Builder
for i := 0; i < 2; i++ {
	builder.WriteString("123")
}
// builder.String() 为 123123
```

为什么 `strings.Builder` 会性能更好呢？因为其内部是使用 `[]Byte` 数组实现的，而普通的字符串在 Go 语言中属于不可变类型（内存大小都固定），其每次进行 + 操作来拼接字符串都会重新分配内存。相比之下， `strings.Builder` 则会利用扩容策略来避免每次都需要重新分配内存。

### atomic

`"sync/atomic"`可以实现原子操作，适合在并发时使用，并且比常用的加锁操作更加节省开销和更好性能：

```go
type Num struct {
	i int32
}

func Add() {
	num := new(Num)
	atomic.AddInt32(&num.i, 1)
}
```

atomic包的原子操作只能保护一个变量，但同时他是利用硬件实现的，所以他的性能很高。

## fastrand函数 快速随机

由于rand函数为了保证随机序列的一致性，使用了全局锁。这样带来的牺牲是当我们使用rand函数又进行并行时，其效率会大大降低。

我们可以使用`fastrand`函数代替`rand`函数，`fastrand`函数不会设置全局锁，更能发挥并行的优点，而且`fastrand`函数其实是适用大部分情景的。





## 规则引擎的设计与实现

### 基础概念

规则引擎是一种嵌入在应用程序中的组件，实现了将业务决策从应用程序代码中分离出来，并使用预定义的语义模块编写业务决策。接收数据输入，解释业务规则，并且根据业务规则做出业务决策。

在真正的业务场景中，通常是代替了`规则修改 -> 业务人员整合 -> 开发人员修改(代码层面) -> 实现新的业务逻辑`成为`规则修改 -> 业务人员整合并在平台层面修改 -> 实现新的业务逻辑`；作为一名前端开发人员，我觉得这更像一种`后端的低代码`模型，将规则修改提升到了业务人员层面，通过“鼠标点点点”，来完成原本需要开发人员参与的规则修改工作。

组成部分：

- 数据输入：接收预定义的语义编写的规则作为策略集。比如“price > 500”和执行过程中的参数，比如价格，标签；
- 规则理解：按照预定义的词法，语法，优先级，运算符等正确理解业务规则所表达的语义；
- 规则执行：根据策略集进行正确解释和执行。

应用场景：

- 风控对抗：优化对抗策略以实现最好的风控识别效果；
- 活动运营策略：根据用户效果和反馈实施优化策略；
- 数据分析和清洗：使用规则引擎更加方便快捷的处理数据。

### 核心原理

#### 编译原理

规则引擎本身就是在做编译：

1. 对业务人员的输入进行此法分析和语法分析，最终理解。

- 词法分析：把源代码字符串转换为此法单元（Token）的过程。例如 price > 500 分割成price，>，500 
- 语法分析：在词法分析的基础上识别表达式的语法结构

2. 对分析出的语法结构构建抽象语法树。
3. 对类型进行校验，判断规则合法性，并且进行执行。

**词法分析：**

如何识别一个token(语法单元)？

使用一个有限自动机：有限自动机是一个状态机，它的状态数量是有限的。该状态及在任何一个状态，基于输入的字符，都能做一个确定的状态转换。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230131232733.png)

例如上面的图，当遇到一个英文字母时，循环去读，知道遇到空格或其他特殊标识，得到一个参数。

同时，词法分析也要分析出当前词的类型和**优先级**。常见的词可以分为：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2023-02-01_00-28-59.png)

**语法分析：**

语法分析就是在词法分析的基础上，识别表达式的语法构建的过程。例如，price > 500 被构建成了抽象语法树：

```
		> 操作数
	  /          \     
price 左操作数   500 又操作数
```

这里的抽象语法树有这么几个概念：

- 上下文无关语法：语言句子我们无需要考虑上下文就可以判断出其正确性。
- 递归下降算法：递归下降算法就是不断的对Token进行语法展开（下降）直到遇到分号等结束符。这中间可能会遇到一些递归的情况。
- 类型检查：根据子表达式的类型构造出父表达式的类型，例如`a=b+c`,b和c是int类型，所以a应该是一个int类型而不是其他类型

**语法树执行和类型检查：**

- 语法树执行就是对树进行后续遍历，即：先执行左子树得到左子树的值，在执行右子树得到右子树的值，最后根据根节点的操作符得到根节点的值。
- 类型检查就是根据上述的类型检查手法再运行时或者编译时进行类型检查。

### 设计实现规则引擎

规则引擎demo：

> [qimengxingyuan/young_engine: 简单的规则引擎 (github.com)](https://github.com/qimengxingyuan/young_engine)



