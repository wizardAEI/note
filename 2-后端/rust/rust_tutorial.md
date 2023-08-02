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

   