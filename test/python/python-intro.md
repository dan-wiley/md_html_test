## Docker Lesson 1

> In this module ....


- Docker is fun
- Docker works
  - Same on every machine
  - Has packages installed on images already!

1. Use this image to run the code below
  ```
  FROM python:3.10.0
  # this is all you need for basic python
  ```

```python
print("hello")
text="new text"
text += " again"
if text:
    print(text)
    # prints new text again
```


| Python | C |
| ----------- | ----------- |
| VM | Native |
| Interpreted programming language thats loads of fun | Have to allocate memory and not leak over... not fun |
