### Base type

String

```rust
let mut name = String::new()	// define a empty string
```



### disable the warning of unused code

1. use `allow` attribute

   ```rust
   #[allow(unused)]
   let unused_variable: i32 = 5
   ```

   `#[allow(unused)]` can disable the lint for the group of unused-imports, unused-variables, unused-assignments, dead-code, etc.

2. prefix the identifier by `_`

   ```rust
   let _unused_variable: i32 = 5
   ```

### 汉字

If we use Chinese characters in string, notice that the  occupancy length is not same as English character. In English, each latter takes up only 1 byte in UTF-8 encoding, but in Chinese, each latter always take up 3 bytes.

So if we operate the string when it includes the Chinese characters, it will be easy  to make mistakes. .e.g:

```rust
let mut str = String::from("我谁")；
str.inster(1, '是'); // error
```

the reason for the error above is that one Chinese character take up 3 bytes in UTF-8 encoding and not divisible in the middle. So we need code in this way:

```rust
str.inster(3, '是');
print!("{}", str) // 我是谁
```
