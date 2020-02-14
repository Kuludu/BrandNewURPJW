# BrandNewURPJW

URP教务管理系统是部分高校用于对学生进行管理的系统。

然而众所周知，它并不好使，本项目计划对其一部分功能进行了优化，包括但不限于：

- [x] GPA计算
- [x] 一键教评
- [x] 学期考试查询
- [x] 成绩查询

因考虑到大多数教务系统内网访问速度远大于外网，选课辅助功能已另成项目，敬请关注。

项目采用Flask框架，已在URP（版本1.5_0）下测试通过。

## 部署

1. 修改**config.py**，将URP教务系统的地址填入。
2. 使用Gunicorn拉起项目

```
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

## 支持

https://github.com/Kuludu/BrandNewURPJW/issues

## ChangeLog

* Beta 1.0
  * 添加GPA计算器功能。
* Beta 1.1
  * 添加成绩查询功能。
* Beta 1.2
  * 添加考试查询功能。
  * 修复GPA计算错误。
* Beta 1.3
  * 修复前端bug
  * 完成一键教评功能前端逻辑
* Beta 1.4
  * 完成一键教评功能
