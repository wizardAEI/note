# go学习笔记



## 第一个go程序

1.   新建目录，终端输入`go mod init 模块名`的方式来新建`go.mod`文件作为依赖管理文件

2. 新建一个目录作为工作目录

3. 在新目录中新建`mian.go`作为主文件

   ```go
   package main // 包名 必须要有一个main包
   
   import "fmt" // 引入的包，这里用来做输入
   
   func main() {  // main函数只能声明在main包中，且只能声明一个函数
   	fmt.Println("HELLO GO")
   }
   ```

   在该目录下，终端执行`go build`(注意是在工作目录下)生成可执行文件

4. 新建其他go文件或者目录。注意同一目录下的go文件的package都必须是一致的



## 变量和常量

```go
func main() {
	var a int //声明一个int型的变量，默认值是0
	fmt.Println("a的默认值是：", a)
	fmt.Printf("a的类型是：%T \n", a)
	var b int = 1
	fmt.Println("a的默认值是：", b)
	fmt.Printf("a的类型是：%T \n", b)
	c := "字符串" //短声明方式
	fmt.Printf("c的类型是: %T,c的值是: %s \n", c, c)
}
/* a的默认值是： 0
a的类型是：int 
a的默认值是： 1
a的类型是：int 
c的类型是: string,c的值是: 字符串 */
```

短声明的其他注意事项：[短变量声明](https://studygolang.com/articles/17913)

一次声明多个变量：

```go
var (
	n = 1,
    m = 2
)

var q, p = 1, 2
```

go中的常量可以使用`const`来声明，同时在go里也可以用来做枚举：

```go
const n = 1000

const (
	BEIJING = 1
	TIANJIN = 2
) 
```

同时go也提供了iota作为常量计数器,使用方法：

```go
func main() {
	const (
		a = 10 * iota
		b
		c
	)
	fmt.Printf("%d %d %d\n", a, b, c)
}
//0 10 20   不加10来设置步长 则默认为 0 1 2
```

### 大值常量

常量可以储存很大的值，此时其描述为无类型，并且在go底层使用big包进行处理：

```go
func main() {
	const a = 200000000000000000000 // untyped int 没办法直接输出，但是可以进行运算，此时go底层使用big包处理
	const b = 22343
	const c = a / b
	fmt.Println(c) // 8951349415924450
}
```



## 数据类型

### **整形 Integer**

int 包括 int8 int16 int32 int64 其中直接声明int型，变量根据系统是32位还是64位，决定其大小占几位和范围。例如64位系统下，int就和int64一样

无符号整形 unsignedInteger：

uint包括 uint8 uint16 uint32 uint64

### 浮点型 float

float包括 float32 和 float64

**小知识：**如果一个指数型的数字（ a := 2e5 ）没有被指定类型的时候，那么它默认为float64类型，因为float64的范围是很大的，这和其精度没有关系，其最大值为`1.8e308`。

### 字符串 string

string类型是字符串，go里面必须使用双引号包裹

#### 切分字符串

可以利用创建切片的语法来切分字符串：

```go
func main() {
	s := "hello world"
	s2 := s[:5]
	fmt.Println(s2) // hello
}
```

**注意**

```
s := "a"
s = s[1:]
```

上述写法并不会报错，而是返回一个空字符串。	

### 大数 big

虽然我们可以使用float64来很大的数，但这样不能保证对应的精度。此时我们可以使用big包来获取很大同时保证精度的值：

```go
// 使用newInt创建，函数接收值为一个int64类型的数
a := big.NewInt(12)

// 使用SetString创建超过int64上限的大数
a := new(big.Int)
a.SetString("240000000000000000000000000000000000000000", 10)
```



### 字符 Rune

用来表示字符，并且兼容中文，韩文等特殊符号等字符，其本质是一个int32。

```go
// rune is an alias for int32 and is equivalent to int32 in all ways. It is
// used, by convention, to distinguish character values from integer values.
type rune = int32
```



### **数组**

```go
var arr [5]int
arr[0] = 1

//短声明
arr := [5]int{15, 20} //后面不声明的默认是0

//通过制定索引，对某几个元素进行赋值
arr4 := [5]int{1: 100, 4:200}

//让编译器帮忙计算值
arr4 := [...]int{14, 20} 
```

注意数组的长度也是数类型的一部分，例如`[3]int`和`[5] int`不是一种类型。所以函数一般是使用切片而不是数组作为形参。

数组是一个值类型，并不是一个引用类型。如果我们传递数组需要使用同一个地址而不是复制，可以使用指针：

```go
func main() {
	a1 := [...]int{1, 2, 3}
	a2 := &a1
	(*a2)[1] = 3
	fmt.Println(a1, *a2) //[1 3 3] [1 3 3]
}
```



### 切片

切片是对数组的一个连续片段的引用，所以切片是一个**引用类型**，sllice会将数组作为其底层的数据结构，只是没有固定长度。

声明一个切片：

```go
var slice []int //声明整形切片
var numListEmpty []int{} //声明一个空切片

//make函数构造一个切片
numList := make([]int, 3, 5) //表明类型是int型数组，后两个参数切片的长度，切片的容量
// 此时底层会开辟一段数组内存，其长度为5，但是可以使用的只有前三个元素，要使用后面两个需要进行扩容操作，否则会panic

// 从数组中截取切片
arr := [5]int{1, 2, 3, 4, 5}
slcie := arr[2:4] //若是[:]则代表全部的元素
slice2 := arr[2:4:2] //表示切片取数组[2,4), 其容量为2，否则其容量会根据底层数组的截取大小设置为3
fmt.Println(slcie)
//[3 4] 
```

若没有对引用类型进行赋值，那么其值默认为`nil`

#### 切片的扩容：

```go
slice := []int{1, 2} // 此时切片的长度和容量相同，都是2
slice = append(slice, 1) // 我们使用追加函数，由于元素被追加进来时没有多余的空间了，所以进行扩容操作
fmt.Println(slice) // 扩容后的切片的容量为4，长度为3
//[1 2 1]
```

这里重点说一下扩容时的底层操作：

- 将原切片的值复制
- 生成一个原切片值两倍容量的底层数组，并将切片和追加的元素放进去
- 返回数组的引用

可以看到扩容时并不是在原有数组上进行操作，而是重新生成了一个长度为数组两倍的数组作为新的底层数组，其地址已经不同了。所以我们可以说扩容后的切片已经不等于原切片了。我们可以进行以下实验：

```
func main() {
	a1 := []string{"1", "2"}
	a2 := append(a1, "3") // 进行扩容，扩容后的底层数组长度为4，即切片容量为4
	a3 := append(a2, "4") // 不需要扩容
	a3[0] = "3"
	fmt.Println(a1, a2, a3) // [1 2] [3 2 3] [3 2 3 4]
}
```

可以看到，当改变a3时，a2变化了，a1没有变化，说明a1的底层数组和a2,a3已经不是同一个引用了。

#### 对切片的复制

```go
a := []int{1, 2}
b := []int{3}
copy(a, b)
fmt.Println(a)
// 3 2
copy(a[1:], b)  // 可以指定从确定下标开始向a复制b的值
fmt.Println(a)
// 3 3
```

#### 在函数中使用切片：

```go
func main() {
	s := []int{1, 2, 3} // 创建了底层数组并创建一个切片指向它
	func(myStr []int) {
		myStr[1] = 3 // myStr是对s的复制，但同时两者都指向一个底层数组
	}(s)
	fmt.Println(s) // [1 3 3] 说明改变myStr其实就是改变底层数组，相当于也影响了s
}
```

#### 利用方法和切片实现各种功能（例如排序）

我们可以在Go语言中声明底层为切片或者数组的类型，并为其绑定相应的方法。跟其他语言的类（class）相比，Go语言在类型之上声明方法的能力无疑更为通用。

例如标准库的sort包声明了StringSlice类型：`type StringSlice []String`并且该类型还关联了方法：`func (p StringSlice) sort()`

为了按照字母顺序对某一个切片排序，我们就可以利用上面的sort方法：

```go
func main() {
	s := []string{"a", "c", "b"} // 创建了底层数组并创建一个切片指向它
	sort.StringSlice(s).Sort()   // 将s变为StringSlice类型之后进行排序  这里sort包提供了辅助函数简化操作：sort.Stringss(s)
	fmt.Println(s)               // a b c
}
```

### **Map**

通过字面值创建Map:

```go
mapOne := map[string]string{
		"a": "A",
		"b": "B",
	}
fmt.Println(mapOne)
//map[a:A b:B]
```

通过make创建Map：

```go
mapTwo := make(map[string]string)
mapTwo["a"] = "cat"
fmt.Println(mapTwo)
// map[a:cat]
```

注意map是无序的，并且map是一个引用类型

添加和删除map，判断是否存在某个键值对：

```go
mapOne := map[string]string{
  "a": "A",
  "b": "B",
}
mapOne["c"] = "C" //插入
delete(mapOne, "a")
fmt.Println(mapOne)
value, ok := mapOne["c"]
fmt.Printf("%s %t\n", value, ok)
/*map[b:B c:C]
C true*/
```

虽然map是无序的，但是我们仍然可以进行遍历map，我们可以使用for range语法:

```go
for key, value := range mapOne {
		fmt.Println(key, value)
	}
/*
c C
b B
*/
```

更多range的参考可以查看：https://www.runoob.com/go/go-range.html

### **结构体**

声明一个结构体

```go
type Person struct {
	name   string //名称
	age    int    //年龄
	target string //目标
	behave string //行为
}
```

我们在使用的时候就可以采用

```go
xiaoming := Person{
		name:   "xiaoming",
		age:    10,
		target: "xx",
		behave: "yy",
	}
	println(xiaoming.name)
```

同时，我们也可以这样：

```go
xiaoming := Person{"xiaoming", 19, "xx", "yy"} //必须按照顺序
```

我们还可以先声明该结构体的变量后进行赋值：

```go
type Person struct {
	name   string //名称
	age    int    //年龄
	target string //目标
	behave string //行为
}
xiaoming := Person{}
xiaoming.name = "123"
```

#### 匿名结构体

```go
	xiaoming := struct {
		name   string //名称
		age    int    //年龄
		target string //目标
		behave string //行为
	}{
		name:   "xiaoming",
		age:    10,
		target: "xx",
		behave: "yy",
	}
	fmt.Println(xiaoming) //{xiaoming 10 xx yy}
```

#### 结构体指针

结构体声明的变量指针比较特殊，它可以直接代替变量去访问属性：

```go
type Person struct {
		name   string //名称
		age    int    //年龄
		target string //目标
		behave string //行为
	}

	ptr := &Person{
		name:   "xiaoming",
		age:    18,
		target: "xx",
		behave: "yy",
	}
	fmt.Println((*ptr).age, ptr.age) // 18 18
```

这里其实是统一了C语言中的指针使用`->`访问属性和变量使用`.`访问属性的形式，统一使用`.`

#### 结构体转发

结构体的嵌套和字段提升：

```go
	type Other struct {
		x int
		y int
	}
	type Person struct {
		name  string
		age   int
		other Other
	}
	s := Person{
		name: "xiaoming",
		age:  18,
		other: Other{
			x: 1,
			y: 2,
		},
	}
	fmt.Println(s.other.x) // 这里我们访问x需要先访问other
```

此时，我们若将`Other`定义为匿名字段的类型，则会出现**字段提升**，我们访问Other内部的字段可以直接使用Person，这种特性称为转发:

```go
	type Other struct {
		x int
		y int
	}
	type Person struct {
		name string
		age  int
		Other
	}
	s := Person{
		name: "xiaoming",
		age:  18,
		Other: Other{
			x: 1,
			y: 2,
		},
	}
	fmt.Println(s.x) //注意我们这里使用的是s.x，不必再去访问Other 
```

同时，这种匿名字段也可以实现对方法的转发，给结构体添加方法：

```go
type Person struct {
	name string
	age  int
}

func (p Person) ShowFullName(str string) (fullName string) {
	fullName = str + p.name
  return
}

func main() {
	s := new(Person)
	s.name = "ming"
	name := s.ShowFullName("xiao")
	fmt.Println(name) // xiao ming
}
```



### **指针**

创建一个指针：

```go
func main() {
	str := "hello"
	ptr := &str
	fmt.Println(ptr, *ptr)
}
//0xc000010250 hello
```

注意，go语言中的指针不支持例如`ptr++`这样的运算（只能使用`ptr + 1`来找到指针后的地址）

http://www.go-edu.cn/2022/05/08/go-07-%E6%8C%87%E9%92%88/

#### 解引用

指针为数组和结构体提供了可以自动解引用的操作，即`(&arr)[0]`可以直接使用`arr[0]`代替：

```go
arr := [...]int{1, 2}
arrPointer := &arr
fmt.Println(arr[0], arrPointer[0]) // 1 1
```

需要注意，虽然go给数组提供了自动解引用的操作，但是并没有为切片和映射提供自动解引用的特性。





### 格式化输出

go中可以利用`fmt`的方法判断变量的类型：

```go
package main

import "fmt"

func main() {
	a := 1
	fmt.Printf("%T", a)
}
```



## 引用类型

在 Go 语言中，引用类型有 切片(slice)、字典(又叫做映射 map)、接口（interface） 以及 通道(chan) 。 注意结构体是基本类型，如果函数中传递的不是结构体的指针，则函数中的修改不会影响到原结构体。

其中的每个引用类型性质又不太一样，例如切片是对一部分数组的窗口和引用，字典是隐式指针所以当复制时会共享同一块底层数据... 但他们都可以达到复制或者传参时还是同一个地址的效果。



## **函数**

```go
func main() {
	fmt.Println(fn(1, 2))

}

func fn(x int, y int) int {
	return (x + y)
}

// 3
```

上述代码中可以看出，go语言的函数声明顺序是随意的

同时函数的参数也可以是可变参数：

```go
func main() {
	fmt.Println(show("x", "y", "z"))

}
//当使用 ...string类型时，表明读入的参数是一个切片
func show(args ...string) int {
	sum := 0
	for _, v := range args {
		fmt.Println(v)
		sum++
	}
	return sum
}
// x y z 3  
```

函数可以返回多个参数：

```go
func main() {
	n, str := show("a", "b", "c")
	fmt.Println(n, str)

}

func show(args ...string) (int, string) {
	sum := 0
	str := ""
	for _, v := range args {
		sum++
		str += v
	}
	return sum, str
}
//3 abc
```

函数的返回值可以自带名称，这样函数就会自动去寻找对应的变量并返回，例如，上述函数可以改成：

```go
func show(args ...string) (sum int, str string) {
	for _, v := range args {
		sum++
		str += v
	}
	return
}
```

这样，执行代码也会返回`3 abc`

函数没有名字则变成了匿名函数,go语言不允许函数嵌套，但是我们可以利用匿名函数来实现相同效果：

```js
n,s := func (args ...string) (sum int, str string) {
			for _, v := range args {
				sum++
				str += v
			}
			return
		}("a", "b", "c")
```

**函数可见性**

- 首字母大写，对于所有包时public，其他包任意调用
- 首字母小写，这个函数是private，其他包无法访问



## 方法

`方法`和函数很类似，它可以通过附加行为来增强类型，方法在`func`这个关键字和方法名中间加入了一个特殊的接收器类型。接收器可以是结构体或者是非结构体类型。接收器是可以在方法内部访问的。

```go
func (t Type) methodName(parameter list) {

}
t.methodName(parameter)
```

go不允许相同名字的函数，但是允许相同名字的方法绑定在不同的结构体中。 

go的接收器可以使用指针或者值，如果我们想改变结构体的值，那么我们就需要使用到指针接收器：

```go
//两个方法都可以在内部修改lesson的值，但是当外面实例化出来的结构体变量，只能通过第二种方式进行修改
func (lesson Lesson) AddOne() {
	lesson.num++
}
func (lesson *Lesson) AddOne2() {
	lesson.num++
}
```

同时，不适用指针的方法，仍可以使用指针去调用，这样做go会自动进行解引用：

```go
func (lesson Lesson) AddOne() {
	...
}
var l Lesson
(&l).AddOne() // 这样是可以的
```



## 接口

### 简介

Go 语言提供了另外一种数据类型即接口，它把所有的具有共性的方法定义在一起，任何其他类型只要实现了这些方法就是实现了这个接口。

```go
type interface_name interface {
  method1()
  method2()
}
```

接口实例：

```go
package main

import (
    "fmt"
)

type Phone interface {
    call()
}

type NokiaPhone struct {
}

func (nokiaPhone NokiaPhone) call() {
    fmt.Println("I am Nokia, I can call you!")
}

type IPhone struct {
}

func (iPhone IPhone) call() {
    fmt.Println("I am iPhone, I can call you!")
}

func main() {
    var phone Phone

    phone = new(NokiaPhone)
    phone.call()

    phone = new(IPhone)
    phone.call()

}
```

可以利用接口来实现多态。

### 实现接口

以fmt包为例，其有一个`Stringer`接口（包含一个函数String）,我们只要实现了他的这个接口，那么我们就可以利用该String函数的返回值给Printf，Println等打印函数所用：

```go
/**
* fmt包的一个接口
* type Stringer interface {
*	String() string
* }
**/
type Location struct {
	x float64
	y float64
}

func (l Location) String() string {
	return "x: " + strconv.FormatFloat(l.x, 'f', 6, 64) + " y: " + strconv.FormatFloat(l.y, 'f', 6, 64)
}

func main() {
	location := Location{
		x: 1.0,
		y: 2.0,
	}
	fmt.Println(location) // x: 1.000000 y: 2.000000
}
```



### 泛型（利用空接口）

同时，利用空接口，我们可以实现可以承载任何类型的变量：

```go
func main() {
	a := make([]interface{}, 3)
	a[0] = "1"
	a[1] = 2
	a[2] = func() {
		fmt.Println("abc")
	}
	fmt.Println(a) //[1 2 0x1089780]
  a[2].(func())() //这里使用来接口的断言，让go知道当前的类型是方法，我们就可以直接调用匿名方法了
}
```

### 接口的嵌套（集成）

```go
type Device interface {
	on()
} 
type Phone interface {
  Device  
  call()
}
```

### 接口的nil

interface 是一个特殊结构，它由两部分组成，(type,  value)，当我们直接声明一个变量为某个interface类型时，他是nil，此时其内部(nil, nil) 

例如： `var s interface{}` 。

当我们给他制定一个值时，有三种情况：

第一种是只声明了接口：

```go
var s fmt.Stringer  //fmt.Stringer 是一个接口，里面存在String()方法
```

那么此时s打印出来的是nil

第二种确定了接口类型但值为空，例如:

```go
type Person struct {
 name string
}
func (p Person) String() string {
 return p.name
}
var p *Person // p是一个指针，没有初始化所以为nil
var s fmt.Stringer = p
```

那么此时s内部为 (*Person, nil)，打印出来还是nil

第三种情况 指定的变量初始化了 

```go
var p *Person = &Person{
  name: "xxx",
}
```

那么此时s内部为(*Person, value),打印出来的就不是nil了。

go认定，接口只有类型和值都为nil才等于nil，所以会出现下面这种情况：

```go
func main() {
	var v interface{}
	fmt.Printf("%T %v %v\n", v, v, v == nil) // <nil> <nil> true
	var p *int
	v = p
	fmt.Printf("%T %v %v\n", v, v, v == nil) // *int <nil> false  虽然值为nil，但是确定了类型，所以不等于nil
	fmt.Printf("%#v\n", v) // (*int)(nil)
}
```



## 包

```go
package 包名
import "包名"
```

在go中，任何在最外层被大写的变量或者函数都是被导出的，可以被其他包引用

假设有以下目录结构：

```
go_test
|-test1
  |-book
		|-book1.go
  |-mian.go
|-go.mod
```

我们在`book1.go`中写一个方法，并在main.go中使用：

```go
//book1.go
package book  //同一个目录下的包名必须一致，比如又在该目录下新建了book2.go,那么他的包名也必须是book

func GetBook() string {
	return "《abc》"
}

//main.go
package main

import (
	"fmt"
	"test/test1/book" //相对于根目录，也就是go.mod所在的目录
)

func main() {
	fmt.Println(book.GetBook()) //《abc》
}
```

### 包的别名

包名可以使用别名来代替：

```go
import (
	"fmt"
	b "test/test1/book"
)

func main() {
	fmt.Println(b.GetBook())
}

// 同时 如果我们将别名取为 . 那么就相当于默认把该包的变量直接导入，即可以直接使用GetBook()
```

包的初始化函数

`init()`函数作为包的初始化函数，会在包被调用时初始化执行

例如，我们在book包中加入：

```go
func init() {
	fmt.Println("import book")
}
```

那么它会在`main,go`引入该包时被调用。

包的匿名导入：

当我们只想执行包的`init()`函数又不想使用它，同时也不希望编译器会将包去掉，那么我们就可以使用`_`来代替包名，来达到匿名导入的效果：

```go
import _ "包名"
```

### 包的共有私有

包中的变量，只用大写字母开头才会被读取，作为共有变量。其余小写字母开头的变量都是私有变量。



## go的流程控制

### if else

```go
if a > 1 {
	// ...
}else if a < 0{
	// ...
} else {
	// ...
}

/*if 可执行语句; 判断 {
  ...
}*/
if a := getNum(); a > 1 {
 // ...
}
```

if 可以包含一个初始化语句（如：给一个变量赋值）。这种写法具有固定的格式（在初始化语句后方必须加上分号）：

```go
if initialization; condition {
    // do something
}
```

例如:

```go
val := 10
if val > max {
    // do something
}
```

你也可以这样写:

```go
if val := 10; val > max {
    // do something
}
```

但要注意的是，使用简短方式 := 声明的变量的作用域只存在于 if 结构中（在 if 结构的大括号之间，如果使用 if-else 结构则在 else 代码块中变量也会存在）。如果变量在 if 结构之前就已经存在，那么在 if 结构中，该变量原来的值会被隐藏。最简单的解决方案就是不要在初始化语句中声明变量。



### **switch**

```go
switch 表达式 {
	case 值:
		执行代码
  case 值1,值2, 值3:  //多条件判断
		执行代码
	default:
  	执行代码
}

/*switch statement; expression {}*/
switch a:= getNum(); a {
	case 1
		执行代码
  case 2, 3:  //多条件判断
		执行代码
	default:
  	执行代码
}
```

go的switch，默认自带break，若需要执行后面的case，可以使用 **fallthrough** 。

```go
switch 表达式 {
	case 值:
		执行代码
		fallthrough //若满足了上面的case，则也执行后面的执行代码
  case 值1,值2, 值3:  //多条件判断
		执行代码
		fallthrough
	default:
  	执行代码
}
```

switch还有另一种写法：

```go
var ans = getAns()
switch {
case ans == "a":
	fmt.Println("ans is a")
case ans == "b":
	fmt.Println("ans is a")
case ans == "c":
	fmt.Println("ans is a")
default:
	fmt.Println("there is no ans")
}
```



### for

```go
for i := 0; i < count; i++ {
		
}

//for range 形式
for index, value := range arr {
		
}
//类似于while
for num<4 {
  
}
```

go是没有while的，可以使用for来替代

### defer延迟调用

在函数名或者结构的方法前加上`defer`，可以让函数延迟执行。

defer栈：

多个defer存在时，会采用栈的方式存储和调用，即最后一个defer函数会被首先执行（但也是延迟到其他函数执行完之后）。

### goto

表示我们下一步要去执行哪里的代码:

```go
	fmt.Println("xxxx")
	goto label
	fmt.Println("yyyy")
label:
	fmt.Println("zzzz")
//  xxxx zzzz
```

注意，goto和label之间不能有变量声明，否则会报错



## 协程（Coroutine）

Go语言的协程是与其他函数或者方法一起并发运行的工作方式。协程可以看做是轻量级线程。与线程相比，创建一个协程的成本很小。

开启一个协程：

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	go PrintInfo()
	time.Sleep(1 * time.Second) //让主协程也就是main函数歇一会，不然主协程终止，整个程序也就终止了
	fmt.Println("hello ")
}
func PrintInfo() {
	fmt.Println("hello go")
}
```

### 协程转让

`runtime.Gosched()`这个函数的作用是让当前goroutine让出CPU，好让其它的goroutine获得执行的机会。同时，当前的goroutine也会在未来的某个时间点继续运行。

### 多协程检测访问冲突

如果又多个协程同时执行，可能会出现资源访问冲突，我们可以使用`go run -race xxx` 来检测

## 通道

go协程之间通讯的管道，它是一种队列的数据结构

通道的声明：

```go
/*
通道的声明 chan 就是channel的缩写
var channel_name chan channel_type
*/
var ch chan string
ch = make(chan string)

//或者
ch := make(chan string)
```

通道的使用：

通道可以在协程之间传递数据，并且起到阻塞的作用：

```go
func main() {
	var ch chan string = make(chan string)
	fmt.Println("1")
	go PrintChan(ch)
	res := <-ch // 发生了阻塞，等待ch返回结果后才会向下执行
	fmt.Println(res)
	println("3")
}

func PrintChan(c chan string) {
	c <- "2"
}

/* 1
   2
   3 */
```

可以看出，这次的main主协程，并没有运行到底，而是等待ch返回结果后才继续执行。

**注意** 这里的通道由于没设置长度，我们需要等到有两两个**不同**的协程(包括主进程)来同时有存和取时才可以执行。否则将一直阻塞或者产生死锁（当所有另开协程的协程都睡了，但是主进程还要操作通道时）

关闭通道：

```go
close(ch)
//检测通道情况
value, ok := <-ch // 如果通道已经关闭，则ok为false
```

通道的长度和容量：

通道可以利用make函数来设置长度：`make(chan typeName, length)`的方式设置

```go
c := make(chan int, 3) //make一个长度为3的通道，当长度设置为0时，则称为无缓冲通道，存取必须同步
```

当通道没有存储数据时，其`cap`容量为0，使用`c <- data `数据时，其容量加1；使用`<- c`取出数据时，其容量减1。当通道的容量等于长度时再次进行存储数据，就会发生阻塞的情况。

所以我们尽量上通道的存取是同步的。

对通道的遍历：

```go
func main() {
	var ch = make(chan int, 5)
	go loopFn(ch)
	for v := range ch {
		fmt.Println(v)
	}
}

func loopFn(c chan int) {
	for i := 0; i < 10; i++ {
		c <- i
	}
	close(c)
}
// 0 1 2 ... 9
```

这里由于协程之间的通道写进去就被读出来，所以没有产生阻塞，也可以看出，即使通道被`close`关闭了，仍可以取出数据。

我们可以利用，容量为1的通道，通过堵塞的效果，达到锁的作用：

```go
var ch = make(chan bool, 1)

ch <- true //产生堵塞
a = a + 1  //同一时间我们只希望一个协程去操作这个a = a + 1
<- ch //消除堵塞
```



## Select

select语句用在多个发送/接收通道操作中进行选择。

- select语句会一直阻塞，直到发送/接收操作准备就绪
- 如果有多个通道操作准备完毕，会随机地选择其中之一执行

```go
select {
  case expression1:
  	code
  case expression2:
  	code
  default:
  	code
}
```

select的使用：

```go
func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)
	ch3 := make(chan string)
	go fna(ch1)
	go fnb(ch2)
	go fnc(ch3)
	select {
	case mes := <-ch1:
		fmt.Println(mes)
	case mes := <-ch2:
		fmt.Println(mes)
	case mes := <-ch3:
		fmt.Println(mes)
	}

}

func fna(ch chan string) {
	time.Sleep(2 * time.Second)
	ch <- "a"
}

func fnb(ch chan string) {
	time.Sleep(1 * time.Second)
	ch <- "b"
}

func fnc(ch chan string) {
	time.Sleep(3 * time.Second)
	ch <- "c"
}
// 1s后执行了 case mes := <-ch2:
```

可以看出，当select中有一个接受操作准备就绪的时候，就会执行相应的case。若同时有多个条件满足了，那么就会随机执行一个case。

同时若没有条件会被满足，则会堵塞或死锁。为了避免一直死锁，可以采用`default`来执行默认语句或者新建一个超时case来兜底。



## Sync

### waitGroup 多个线程等待

当我们的业务需要等到多个协程全员结束后再去执行某个业务逻辑，那么我们就会用到`waitGroup`:

```go
/*
waitGroup 等待一组任务结束，再去执行其他业务逻辑
Add() 初始值是0，累加子协程的数量
Done() 当某个子协程完成后，计数器减去1，通常是defer调用
Wait() 阻塞当前协程，直到实例中的计数器归零
*/
func main() {
	var wg sync.WaitGroup
	wg.Add(3)
	go printId(1, &wg)
	go printId(2, &wg)
	go printId(3, &wg)
	wg.Wait()
}

func printId(id int, wg *sync.WaitGroup) {
	defer wg.Done() //使用defer则Done会在协程结束之前调用
	for i := 0; i < 3; i++ {
		fmt.Printf("协程%d的第%d个\n", id, i)
	}
}
/*
协程1的第0个
协程1的第1个
协程1的第2个
协程3的第0个
协程3的第1个
协程3的第2个
协程2的第0个
协程2的第1个
协程2的第2个
*/
```



### 通过锁来解决竞争

在go语言中，经常会遇到并发的问题，当然我们会优先考虑使用通道，同时go语言也提供了传统解决方式Mutex(互斥锁)和RWMutex(读写锁)来处理竞争问题。

这里使用银行存取款来演示如何使用锁来解决问题：

首先我们使用waitGroup来操作一系列的并行程序：

```go
type Bank struct {
	balance int //余额
}

func (b *Bank) deposit(amount int, wg *sync.WaitGroup) {
	defer wg.Done()
	b.balance += amount
}

func (b *Bank) getBalance() int {
	return b.balance
}

func main() {
	b := new(Bank)
	var wg sync.WaitGroup
	wg.Add(1000)
	for i := 0; i < 1000; i++ {
		go b.deposit(1, &wg)
	}
	wg.Wait()
	fmt.Println(b.getBalance())
}
//生成不同的结果 如 987
```

发生这种情况的原因在于并行操作了共同的资源，发生了资源竞争。这些修改公共资源的代码被称为**临界区**

现在我们使用互斥锁来解决这个问题：

```go
type Bank struct {
	balance int //余额
	m       sync.Mutex
}

func (b *Bank) deposit(amount int, wg *sync.WaitGroup) {
	defer wg.Done()
	b.m.Lock()
	b.balance += amount
	b.m.Unlock()
}
```

与最初版本相比，我们改变了这两个部分，从而形成了互斥锁。

同时，我们也可以使用`defer`把解锁放在前面：

```go
func (b *Bank) deposit(amount int, wg *sync.WaitGroup) {
	defer wg.Done()
	defer b.m.Unlock()
	b.m.Lock()
	b.balance += amount
}
```

但是，互斥锁会导致同一时间只有一个程序可以执行加锁后的程序，对于读操作较多的业务不是很友好，此时可以使用读写锁：

```go
type Bank struct {
	balance int //余额
	m       sync.RWMutex
}

func (b *Bank) deposit(amount int, wg *sync.WaitGroup) {
	defer wg.Done()
	defer b.m.Unlock()
	b.m.Lock()
	b.balance += amount
}

func (b *Bank) getBalance() (balance int) {
	b.m.RLock()
	balance = b.balance
	b.m.RUnlock()
	return  //默认返回blance
}
```

我们将互斥锁改为读写锁，并改变读取函数，从而实现读写锁。

读写锁与互斥锁的区别：

Mutex 是最简单的一种锁类型，同时也比较暴力，当一个 goroutine 获得了 Mutex 后，其他 goroutine 就只能乖乖等到这个 goroutine 释放该 Mutex。

RWMutex 相对友好些，是经典的单写多读模型。主要遵循以下规则 ：

1. 读写锁的读锁可以重入，在已经有读锁的情况下，可以任意加读锁。
2. 在读锁没有全部解锁的情况下，写操作会阻塞直到所有读锁解锁。
3. 写锁定的情况下，其他协程的读写都会被阻塞，直到写锁解锁。

Go语言的读写锁方法主要有下面这种

1. Lock/Unlock：针对写操作。
2. RLock/RUnlock：针对读操作。

### sync.Cond

Golang的sync包中的Cond实现了一种**条件变量**，可以使用在多个Reader**等待**共享资源ready的场景（如果只有一读一写，一个锁或者channel就搞定了）。

我们通过声明一个条件变量，使用等待`wait`和广播`broadcast`进行同步管理：

```go
func listen(s string, c *sync.Cond, wg *sync.WaitGroup) {
	defer wg.Done()
	c.L.Lock() //这里必须先加锁，因为wait中会先去释放锁再进行阻塞
	// 干点啥
	c.Wait()               //开始等待广播，进行阻塞
	fmt.Println(s, "等待完毕") //这里应该是读操作
	c.L.Unlock()
}
func main() {
	var wg sync.WaitGroup
	wg.Add(3)
	var l sync.Mutex
	c := sync.NewCond(&l)
	go listen("1", c, &wg)
	go listen("2", c, &wg)
	go listen("3", c, &wg)
	time.Sleep(time.Second)
	c.Broadcast()
	wg.Wait()
}
//1s后打印出：
/* 1 等待完毕
3 等待完毕
2 等待完毕  顺序可能不同*/
```

这里，协程会从`wait()`处等待，直到，接收到广播。

同时，我们可以使用`c.Signal()`来唤醒单个协程。

### sync.Once

多个并发(或穿行)调用，只会执行一次：

```go
func main() {
	o := &sync.Once{}
	for i := 0; i < 10; i++ {
		o.Do(func() {
			fmt.Println(i)
		})
	}
}
```

只会打印 0 执行一次之后，`o.Do`中的函数不再执行

我们可以使用`sync.once`实现单例模式：

```go
var once sync.Once
var topicDao *TopicDao
// 初始化TopicDao实例
func NewTopicDaoInstance() *TopicDao {
  // 只执行一次，防止重复创建实例
  once.Do(
  	func() {
  		topicDao = &TopicDao{}
  	}
  )
  return topicDao
}
```



### sync.Map

Go语言中内置的map不是并发安全的。请看下面的示例：

```go
var m = make(map[string]int)

func get(key string) int {
    return m[key]
}

func set(key string, value int) {
    m[key] = value
}

func main() {
    wg := sync.WaitGroup{}
    for i := 0; i < 20; i++ {
        wg.Add(1)
        go func(n int) {
            key := strconv.Itoa(n)
            set(key, n)
            fmt.Printf("k=:%v,v:=%v\n", key, get(key))
            wg.Done()
        }(i)
    }
    wg.Wait()
}
```

上面的代码开启少量几个goroutine的时候可能没什么问题，当并发多了之后执行上面的代码就会报fatal error: concurrent map writes错误。

像这种场景下就需要为map加锁来保证并发的安全性了，Go语言的sync包中提供了一个开箱即用的并发安全版map–sync.Map。开箱即用表示不用像内置的map一样使用make函数初始化就能直接使用。同时sync.Map内置了诸如Store、Load、LoadOrStore、Delete、Range等操作方法。

```go
var m = &sync.Map{}

func main() {
    wg := sync.WaitGroup{}
    for i := 0; i < 20; i++ {
        wg.Add(1)
        go func(n int) {
            key := strconv.Itoa(n)
            m.Store(key, n)
            value, _ := m.Load(key)
            fmt.Printf("k=:%v,v:=%v\n", key, value)
            wg.Done()
        }(i)
    }
    wg.Wait()
}
```

### sync.Pool

[sync package - sync - Go Packages](https://pkg.go.dev/sync#Pool)

## 错误与异常

### 错误

go中内建了一个错误接口，任何实现该接口的方法都可以使用错误：

```go
type error interface {
  Error() string
}
```

例如，`fmt.Println`就会在内部调用`Error()`方法来返回错误字符串：

```go
func FindFile() {
	file, err := os.Open("/a.txt") //找一个不存在的文件
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(file)
	}
}
//open /a.txt: no such file or directory
```

自定义错误：

```go
//定义一个结构体
type errorString struct {
	s string
}

//自定义error
func MyError(text string) error {
	return &errorString{s: text}
}

//实现Error方法,来实现error接口
func (e *errorString) Error() string {
	return e.s
}

func divide(a, b int) (int, error) {
	if b == 0 {
		return 0, MyError("被除数不能为零")
	}
	return a / b, nil
}
func main() {
	fmt.Println(divide(1, 0)) //0 被除数不能为零
}
```

更简单的，我么可以使用`return errors.New(“错误信息”)`或者`fmt.Errorf("错误信息")`快速返回自定义信息的错误

### 异常

异常指的是不应该出现问题的地方真的出现了问题。

我们可以使用`panic`来触发异常：

```go
panic("asd")  //panic: asd
fmt.Println("123") //并不会执行
```

程序发生异常的时候，会在`panic`处停止，执行完所有**延迟函数**后，执行并打印`panic`中的值，就此返回，并返回堆栈信息。在没有`panic`的时候，发生异常则也会立即停止，执行延迟函数，打印错误信息，返回堆栈信息。可以看做在异常的下一句直接执行了`panic`。

同时，我们可以通过`recover` 捕获异常:

```GO
func main() {
	read(2)
	fmt.Println("123") //会打印出来
}

func read(i int) {
	defer func() {
        err := recover() // 只用被延迟的方法可以使用recover()
		fmt.Println(err)
	}()
	arr := [1]int{1}
	fmt.Println(arr[i])
}
//runtime error: index out of range [2] with length 1
//123
```

会继续执行的原因是函数内发生了异常，本应立即返回，但是被defer中的`recover`函数捕获了，所以没有在外层产生异常。

异常会不断向上传递，所以我们可以在顶层函数上的延迟函数中捕获异常保证程序不崩溃

## new和make

`new`首先会分配内存，然后设置该结构的零值，最后返回一个指向新分配的类型的指针。

```go
o := new(sync.Once)  //也可以写成下面的
o := &sync.Once{}
```

`make`只能分配和初始化切片，`map`和`chan`:

```go
a := make([]int, 2, 10) //长度为2 容量为10
b := make(map[string]int) //map
c := make(chan int, 10)
```



## 静态类型和动态类型

静态类型：

```go
var number int
str := "abc"
```

动态类型

```go
var a interface {}
a = 100 //此时type为int
a = "123" //此时type为string
```



## 断言

### 基础

断言就是将接口类型的**值**`x`转换成类型`T`。格式为：x.(T)

- 类型断言的必要条件就x是接口类型，非接口类型的x不能做类型断言；
- T可以是非接口类型（基础类型，结构体或者指针等），如果想断言合法，则T必须实现x的接口；
- T也可以是接口，则x的动态类型也应该是接口T；
- 类型断言如果非法，运行时会导致错误，为了避免这种错误，应该总是使用下面的方式来进行类型断言:

```go
package main

import (
	"fmt"
)
func main() {
  var x interface{}
  x = 100
  value1,ok :=x.(int)
  if ok {
	fmt.Println(value1)
  }
  value2,ok :=x.(string)
  if ok {
	fmt.Println(value2)
  }
}
```

需要注意的如果不接收第二个参数也就是ok，这里失败的话则会直接panic。这里还存在一种情况就是x为nil同样会panic

若类型检查成功提取到的值也将拥有对应type的方法：

```go
package main

import "fmt"

func main() {
  var a interface{}
  a = A{}
  value :=a.(A)
  value.Hi()
  fmt.Println("看是否输出",value.Name)
}
type A struct {
	Name string
}
func (a *A) Hi()  {
	a.Name="fushaohua"
	fmt.Println(a)
}
```



这里我们定义一个结构体，又定义了一个方法，其中方法的参数类型为一个泛型，那么此时我们想调用参数的属性或方法就会有问题：

```go
type User struct {
	Name string
	Age  int
	Sex  bool
}

func (u User) SayName() (name string) {
	fmt.Println(u.Name)
	return
}

func main() {
	u := User{
		Name: "aei",
		Age:  10,
		Sex:  true,
	}
	check(u)
}

func check(v interface{}) {
	v.SayName() // 报错 type interface{} has no field or method SayName
}
```

这个时候我们使用断言就可以结局这个问题：

直接使用断言：

`v.(结构体类型).属性或方法`

```go
func check(v interface{}) {
    v.(User).SayName() // 不再报错
}
```

同时我们可以通过`v.(type)`和switch结合使用获得动态的类型值：

```go
func check(v interface{}) {
	switch v.(type) {
	case User:
		v.(User).SayName()
	}
}
```

### 断言和指针

```go
type A struct {
	name string
}

type Boy interface {
	getName() string
}

func (receiver A) getName() string {
	return receiver.name
}

func main() {
	a := A{
		name: "xiaoming",
	}
	formatName(&a)
	fmt.Println(a.name) // Mr.xiaoming} 如果我们在下面使用 ns.(A) ，则值不会被修改
}
// 这里的形参类型为接口，我们传递结构体或者指针都可以
func formatName(boy Boy) {
	//n, _ := ns.(A) // 这里我们断言为结构体是不会报错的，go会帮我们自动解引用，但是这样我们后续的修改就不会影响传过来的参数了
	n, _ := boy.(*A)
	n.name = "Mr." + n.name
}
```



## 反射

go提供了一种机制，能够在运行时更新变量和检查它们的值，调用他们的方法和它们支持的内在操作，而不需要在编译时就知道这些变量的具体类型。

go中`reflect`包实现了运行时反射。`reflect`包会帮助识别`interface{}`变量的底层具体类型和具体值

```go
func main() {
	reflectType(123) //int
	reflectType("abc") //string
}

func reflectType(x interface{}) {
	obj := reflect.TypeOf(x)
	fmt.Println(obj)
}
```

与`reflect.Typeof()`类型不同，`Kind()`代表一个大的种类：

```go
type Book struct {
	value string
}

func main() {
	book := Book{
		value: "《自行车》",
	}
	reflectType(book)
}

func reflectType(x interface{}) {
	typeb := reflect.TypeOf(x)
	kind := typeb.Kind() //注意这里是对reflect.TypeOf(x)返回的值进行.kind
	fmt.Println(typeb)
	fmt.Println(kind)
}
//main.Book 类型
//struct 种类
```

我们也可以通过`NumField`来返回字段的数量：

```go
type Book struct {
	label string
	value int
}

func main() {
	book := Book{
		label: "《自行车》",
		value: 12,
	}
	reflectType(book)
}

func reflectType(x interface{}) {
	typeb := reflect.TypeOf(x)
	kind := typeb.Kind()
	if kind == reflect.Struct {
		fmt.Println(reflect.ValueOf(x).NumField())
	}
}
// 2 
```

同时我们可以和`reflect.ValueOf(obj).Field(index)`搭配起来，对结构体进行遍历：

```go
type person struct {
	name string
	age  int
}
func main() {
	v := reflect.ValueOf(person{"steve", 30})
	count := v.NumField()
	for i := 0; i < count; i++ {
		f := v.Field(i)
		fmt.Println(f)
	}
}
// steve
// 30
```

也可以通过

```go
func (v Value) FieldByIndex(index []int) Value
```

```go
func (v Value) FieldByName(name string) Value
```

来拿到对应下标和对应属性名的值

## 结构体标签

在结构体上使用反引号加上字符串称为`Tag`，通常写作键值对的形式：

```go
type person struct {
	Name string `json:"name"`          //json 包只识别以大写字母开头的属性
	Age  int    `json:"age,omitempty"` //加上omitempty当字段为空的时候，不填充该字段
}

func main() {
	p := reflect.TypeOf(person{})
	name, _ := p.FieldByName("Name")
	tag := name.Tag
	keyValue, _ := tag.Lookup("json")
	fmt.Printf("tag和key值：%s %s\n", tag, keyValue)
}
//tag和key值：json:"name" name
```

tag可用作json的encode：

```go
type person struct {
	Name string `json:"name"`          //json 包只导出以大写字母开头的属性，我们通过标签改变其导出时的格式
	Age  int    `json:"age,omitempty"` //加上omitempty当字段为空的时候，不填充改字段
}

func main() {
	var v person
	v = person{
		Name: "steve",
	}
	data, err := json.Marshal(v)
	if err == nil {
		fmt.Printf("%s", data)
	}
}
//{"name":"steve"} 在JSON序列化的时候会根据结构体标签导出对应格式
```



## Go 真泛型

[全面解读！Golang中泛型的使用 - 腾讯云开发者社区-腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/2029500)

## go install；go get；go mod

### go mod和go install的区别

[Go 1.16 中关于 go get 和 go install 你需要注意的地方 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/338011682)

这里需要注意，现在全局安装模块，需要使用`go install`，安装在`$GOPATH`中，可执行文件在该路径下的bin目录中（我们可以将`$GOPATH`添加到环境变量中来实现全局使用包命令）

在项目中进行包安装使用`go get`,使用`go.mod`管理依赖

### go mod的常见命令

`go mod init` 初始化，创建go.mod文件

`go mod download`下载模块到本地缓存

`go mod tidy` 增加需要的依赖，删除不需要的依赖

### go get下载包命令

`go get example.com/pkg`,指定某个网站保存的某个包后面通过`@`跟指定版本：

`@update` 下载默认版本

`@none` 删除依赖

`@v1.1.2` tag版本，语义版本

`@23dfdd5` 特定的commit

`@master` 分支的最新commit

## 构建Go应用docker镜像

基础教学：如何让go的镜像更小（多阶段构建dockerfile）

https://www.cnblogs.com/kevinwan/p/16033634.html

例子：

```
FROM golang:alpine AS builder

LABEL stage=gobuilder
#cgo 是用来为 C 函数创建 Go 绑定的工具,不需要刻意禁用
ENV CGO_ENABLED 0  
#启用了 GOPROXY 加速 go mod download
ENV GOPROXY https://goproxy.cn,direct
#tzdata 在 builder 镜像安装，并在最终镜像只拷贝了需要的时区
RUN apk update --no-cache && apk add --no-cache tzdata

WORKDIR /build

ADD go.mod .
ADD go.sum .
RUN go mod download
COPY ./main ./main
#去掉了调试信息 -ldflags="-s -w" 以减小镜像尺寸
RUN go build -ldflags="-s -w" -o /app/main ./main/main.go


FROM alpine
#安装了 ca-certificates，这样使用 TLS证书就没问题了
RUN apk update --no-cache && apk add --no-cache ca-certificates
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /usr/share/zoneinfo/Asia/Shanghai
ENV TZ Asia/Shanghai

WORKDIR /app
COPY --from=builder /app/main /app/main

EXPOSE 9000

CMD ["./main"]
```



## 其他

### 参数传递结构体和结构体指针

```go
func (p *Person) initAge() { p.age = 1 }
func (p Person) initAge2() { (&p).age = 2 }

func main() {
	s := Person{
		age: 18,
	}
	s.initAge()
	s.initAge2()
    fmt.Println(s) // {1}
}
```

上面两种写法只有`initAge`可以达到修改变量值的效果，`initAge`由于是传进来结构体后才获取的地址，而此时结构体已经是复制而来的了，所以不生效。

### 大括号风格

go中的大括号摆放位置很挑剔，左大括号 { 与函数关键字在一行，右大括号 } 独占一行。否则会报错。

这是由于go中的分号；被去除了，代价就是苛刻的大括号格式。

### float精确度

float32，我们常说的单精度，存储只占32位，其中以为用来代表符号，8位用来代表指数，剩下23位表示尾数。

尾数位占23个bit，它的表达上有一个特殊点，它被认为是24个bit，第一个bit取值1，且被隐藏掉：
这24个bit，依次表达2^0， 2^-1, 2^-2, 2^-23，隐藏的第一位表达的指就是1，所以抛开指数位和符号位来看， 尾数位表达的范围是： [1， 2 - 2^-23]，所以真正的float精度为差不多`2 * 10-7`,但一定小于`2 * 10-7`。所以有下面的结果：

```go
var myfloat01 float32 = 1e-7 // 0.0000001

func main() {
	fmt.Println("myfloat: ", myfloat01+1.5) // 输出1.5000001 没有丢失精度
	fmt.Println("myfloat: ", myfloat01+2.5) // 输出2.5 已经丢失精度了
}
```

保险起见我们可以说，float32的精度是小数点后6位（当整数数为各位数的时候）。整数不为个位数时，将其改为科学计数法在进行比较。

同理，float64的精度为小数点后15位。

### 变量作用域

go的`var`和`const`的作用域总是在`{ }`中存在。只要变量存在作用域中，程序就可以访问它，一旦变量脱离作用域，那么尝试继续访问它将引发错误。

作用域可以让我们在多个位置使用相同的变量名而不会引发任何冲突，在编程的时候只需要考虑当前作用域内的变量。



## fmt.Print 格式化

### 普通占位符

| 占位符 |                     说明                     |             举例              |            输出             |
| :----- | :------------------------------------------: | :---------------------------: | :-------------------------: |
| %v     |              相应值的默认格式。              |   fmt.Printf("%v", people)    |         {zhangsan}          |
| %+v    |          打印结构体时，会添加字段名          |   fmt.Printf("%+v", people)   |       {Name:zhangsan}       |
| %#v    |              相应值的Go语法表示              |   fmt.Printf("#v", people)    | main.Human{Name:"zhangsan"} |
| %T     |           相应值的类型的Go语法表示           |   fmt.Printf("%T", people)    |         main.Human          |
| %%     |        字面上的百分号，并非值的占位符        |       fmt.Printf("%%")        |              %              |
| %nv    | 指定格式化宽度n,正数空格填充在右边，负数右边 | fmt.Printf("%-3v %v", "a", 1) |            a  1             |
| %[1]v  |                复用第一个变量                |   fmt.Printf("%T %[1]v", a)   |     int 1 (假设a := 1)      |
| %x     |                 输出16进制数                 |   fmt.Printf("%[1]x", 0x2F)   |             2f              |

## rand

rand需要一个随机数种子才可以实现随机，否则每次都会出现相同的随机数

```go
func main() {
	rand.Seed(time.Now().UnixNano())
	fmt.Println(rand.Intn(100)) // 92 
	fmt.Println(rand.Intn(100)) // 63
}
```



## GO 测试

### 单元测试

#### 单元测试概念

基本概念：

单元测试是面对**开发过程**进行的测试，测试对象是对开发过程中的相应**函数**，**模块**进行测试。

单元测试通过输入相应参数进入测试单元，对输出值和期望值进行校对，来完成对函数和模块的测试。

单元测试是测试成本最低但同时需要更高覆盖率的测试。

测试规则：

- 所有测试文件以`_test.go`结尾

- 函数命名和参数模板为：`func TestXxx(*testing.T)`。这里的`testing`是go语言的内置包。每一个测试函数都可以独立运行。

- 初始化逻辑放到`TestMain`函数中：

  ```go
  import "testing"
  func TestMain(m *testing.M) {
  	// 测试前：数据装载，配置初始化等前置工作
      code := m.Run()
      ...
      // 测试后：释放资源等收尾工作
      os.Exit(code)
  }
  ```

测试运行：

运行单元测试，我们可以使用`go test [flags] [packages]`，当然，更常用的是使用IDE自带的运行测试，逐个测试函数运行等按钮。

测试辅助：

我们可以使用assert包来辅助验证，

例子：

```go
import (
    "github.com/stretchr/testify/assert"
    "testing"
)
func TestEqual(t *testing.T) {
	output := 1
	expectOutput := 1
	assert.Equal(t, expectOutput, output)
}
```

其他参考资料：

> [Go Test 单元测试简明教程 | 快速入门 | 极客兔兔 (geektutu.com)](https://geektutu.com/post/quick-go-test.html)

测试覆盖率：

代码覆盖率是对整体程序可靠程度的重要评估标准。

计算代码测试的覆盖率可以使用`go test xx_test.go xx.go --cover`命令，在进行测试的同时就可以得到测试程序对`xx.go`的测试覆盖率是多少：

```go
// xx.go
func JudgePassLine(score int16) bool {
	if score >= 60 {
		return true
	}
    return false
}
// xx_test.go
func TestJudgePassLine(t *testing.T) {
    isPass := JudgePassLine(70) // 引入待测试函数
    assert.Equal(t, true, isPass)
}
```

得到以下覆盖率数据：

```
ok      command-line-arguments  0.665s  coverage: 66.7% of statements
```

说明其代码覆盖率达到了66.7%。

虽然我们在测试函数中执行了`JudgePassLine`函数，但是由于我们只验证了70得到true的情况，所以并没有对函数测试完全。我们修改测试函数（或新增测试函数）：

```go
func TestJudgePassLine(t *testing.T) {
	isPass := JudgePassLine(70) // 引入待测试函数
	assert.Equal(t, true, isPass)
	notPass := JudgePassLine(30)
	assert.Equal(t, false, notPass)
}
```

重新执行命令，得到以下数据：

```
ok      command-line-arguments  0.687s  coverage: 100.0% of statements
```

表明我们已经对`xx.go`中的函数做到了完全覆盖。

在实际项目中，我们对需要测试的单元，通常达到50%-60%即可；需要高度测试的单元，我们可以尽量做到80%以上。

### mock测试

在日常的项目开发中，一般都会存在很多依赖，例如`gorm`,`gin`,`os`等，我们在使用这些依赖进行项目开发时，对每个模块都进行单元测试会很麻烦，此时我们可以采取**mock测试**。

我们使用`gomonkey`测试包进行mock测试，这是一个常用的mock测试包。示例如下：

```go
import (
	"bou.ke/monkey"
	"github.com/stretchr/testify/assert"
	"testing"
)
func TestFnxxx(t *testing.T) {
    // 对Fnxxx进行打桩
	monkey.Patch(Fnxxx, func() bool {
		return true
	})
	defer monkey.Unpatch(Fnxxx)
    ...
}
```

上面示例中提到的打桩，就是将某个函数A替换成打桩函数P.

打桩函数的意义在于：若A函数的使用复杂，返回不规律且可能受各种环境影响不稳定，但是B函数(待测试函数)需要使用到函数A,那么我们就可以使用一个打桩函数P来替换函数A。打桩函数通过可控的返回来测试B。

实例：

```go
// xx.go
// 复杂函数
func FetchSomeApi() string {
	// ...一系列fetch操作
}
// 待测试函数
func ProcessFetchSomeApi() string {
	str := FetchSomeApi()
	return strings.ReplaceAll(str, "a", "b")
}

// xx_test.go
func TestProcessFetchSomeApi(t *testing.T) {
	monkey.Patch(FetchSomeApi, func() string {
		return "abc"
	})
	defer monkey.Unpatch(FetchSomeApi)
	strProcessed := ProcessFetchSomeApi()
	assert.Equal(t, "bbc", strProcessed)
}
```

注意这里进行测试运行的时候，由于`golong`使用了内部优化，导致打桩会失效。我们可以使用命令行进行测试:

`go test xx_test.go xx.go -gcflags=all=-l`

### 基准测试

基准测试是测试一段程序来查看cpu的损耗，我们通常对程序进行基准测试来分析程序性能，来找到瓶颈和优化点。

基准测试和单元测试规则相似，其命名规则为`BenchmarkXxx`。

例如，我们对上面单元测试的`JudgePassLine`函数进行基准测试：

```go
func BenchmarkJudgePassLine(b *testing.B) {
	// 重置操作，在重置操作之前，我们可以执行一些其他准备函数，不会记录在性能中
	b.ResetTimer()
    // 注意for循环使用b.N来模拟大量的循环触发
	for i := 0; i < b.N; i++ {
		JudgePassLine(70)
	}
}
```

得到测试结果：

```
BenchmarkJudgePassLine-16       1000000000               0.2906 ns/op
```

表明执行了1000000000次花费了0.2906ns。

上述的循环操作是串行的，我们可以使用并行来重新测试：

```go
func BenchmarkJudgePassLine(b *testing.B) {
	// 重置操作，在重置操作之前，我们可以执行一些其他准备函数，不会记录在性能中
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			JudgePassLine(70)
		}
	})
}
```

得到测试结果：

```
BenchmarkJudgePassLine-16       100000000               18.00 ns/op
```

可以看出，当程序比较简单的时候，其实使用串行比并行更加有效率。

