# BrandNewURPJW

学校<del>终于</del>更新教务系统了，本项目停止开发。

***

URP教务管理系统是部分高校用于对学生进行管理的系统，然而部分学校<del>（比如我校）</del>久未对教务系统进行更新，<del>导致都0202年了在手机上看成绩字还小的跟蚂蚁似的</del>，本项目计划对其一部分功能进行了优化，其中包括：

- [x] GPA计算
- [x] 成绩查询
- [x] 成绩推送到IFTTT
- [ ] 导出课表

本项目采用Flask框架搭建，已在URP（版本1.5_0）下测试通过，暂不支持辅修、补考以及等级制成绩计算。

Update(2021.1.5) 采用`Vue.js`全新重构，支持前后端分离部署。

![image](https://github.com/Kuludu/BrandNewURPJW/blob/master/img/mainpage.png)

## 项目结构

```
BrandNewURPJW
├─ Dockerfile
├─ LICENSE
├─ README.md
├─ app.db # 数据库
├─ app.py # 后端主程序
├─ config.py # 配置文件
├─ fetch.py # 数据爬虫
├─ front_end # 前端
│    ├─ babel.config.js
│    ├─ package-lock.json
│    ├─ package.json
│    ├─ public
│    │    └─ index.html
│    └─ src 
│         ├─ App.vue # 主程序
│         ├─ components # 组件
│         ├─ config # 配置文件
│         └─ main.js
├─ push.py # 定时推送
├─ requirements.txt # 依赖
└─ student.py # 学生数据库逻辑
```

## 部署

### 0.1 配置文件参数说明

#### 前端配置文件

`./front_end/src/config/server.js`

* server : 后端服务器地址

#### 后端配置文件

`./config.py`

* HOST ： URP教务系统主机地址
* MAX_RETRY_TIME ： 推送最大尝试次数
* REFRESH_TIME ： 数据刷新时间（不建议设置过小<del>毕竟教务系统是块土豆</del>）

### 1.1 服务器部署

#### 前端部分

1. 项目环境依赖安装

```bash
npm install
```

2. 修改前端配置文件

详见前节。

3. 编译前端文件

```bash
npm run build
```

4. 部署前端

将上一步编译完成的前端文件部署到前端服务器中。

#### 后端部分

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 修改后端配置

详见前节。

3. 使用Gunicorn或其它前端程序拉起项目

可以使用screen等软件让其保持在后台运行（下同），服务将在服务器8080端口上运行。

```bash
gunicorn -w 1 -b 0.0.0.0:8080 app:app
```

4. 拉起推送服务

```bash
python push.py
```

### 2.1 IFTTT推送设置

**IFTTT在中国大陆地区访问速度可能欠佳。**

1. 首先新建一个Applets[https://ifttt.com/create](https://ifttt.com/create)，设置好触发事件的名称，具体的推送模板可以自定义，程序将在`value1`中推送课程名，在`value2`中推送成绩，以下是一个参考：

![image](https://github.com/Kuludu/BrandNewURPJW/blob/master/img/example.png)

2. 查看推送地址[https://ifttt.com/create](https://ifttt.com/maker_webhooks)点击右上角的`Documentation`进入到接口api界面获取秘钥。

3. 设置页面中（右上方个人信息下拉框中进入）填入上述两个参数并提交。

![image](https://github.com/Kuludu/BrandNewURPJW/blob/master/img/push.png)

具体效果可以参照下图：

![image](https://github.com/Kuludu/BrandNewURPJW/blob/master/img/result.jpg)

## 支持

如果您有什么好的想法与建议欢迎在issues中提出，同时如果您在使用过程中发现了Bug请以 **清晰的描述（包括程序环境信息等）** 在issues中提出，当然如果您有能力且愿意参与到本项目中来也欢迎您提交pull request。

同时，本人提供有偿技术支持，如有需要请与我联系。

## ChangeLog

* Beta 1.0
  * 添加GPA计算器功能
* Beta 1.1
  * 添加成绩查询功能
* Beta 1.2
  * 添加考试查询功能
  * 修复GPA计算错误
* Beta 1.3
  * 修复前端bug
  * 完成一键教评功能前端逻辑
* Beta 1.4
  * 完成一键教评功能
* Beta 1.4.1
  * 更换验证码识别方案为muggle-ocr
* Beta 1.5
  * 全新重构，支持成绩推送至IFTTT
* Beta 1.5.1
  * 修复前端逻辑
* Beta 1.5.2
  * 添加运行日志
  * 优化异常处理
  * 升级tensorflow依赖版本
* Beta 2.1.0
  * 全新重构
* Beta 2.1.1
  *  支持等级制成绩
