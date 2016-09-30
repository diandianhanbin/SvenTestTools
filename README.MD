# 测试工具箱
后端使用Django+MongoDB，前端使用Django的模板渲染和jQuery+Bootstrap处理。

## 功能说明
* Web端测试（未完成）
* 移动端测试（未完成）
* 接口测试（未完成）
* 抓包测试（未完成）
* 缺陷记录（已完成）
* 身份证生成(已完成)

## 移动端测试
### Android——基本信息

* 手机基础信息

包含手机型号,处理器,内存,分辨率,系统版本和手机串号

* 内存信息

包含总内存,空余内存,缓冲区内存,活跃内存和不活跃内存

* 电池信息

包含是否电源供电,是否USB供电,当前电量, 电池温度和电池类型

* CPU信息

由于不同手机差异太大,因此没做过滤,直接全部放出来

* 查看当前运行包名和Activity名

* 查看所有第三方包名

### Android——常用功能

* APK安装

新增了APK安装的功能,需要填写APK在本机的绝对地址

## 缺陷记录
### 操作数据库
操作MongoDB的方法都在mongodb包内。非完全，有待补充。

### 每日bug归档
需要手工启动归档服务, `python bugArchive.py` 每天下午5点归档数据,具体的时间和睡眠间隔可自行调整

### 缺陷趋势图
针对每个项目做缺陷趋势图的展示,数据来源是每日的bug归档数据.

绘图来源:[百度Echarts](http://echarts.baidu.com/)

### 缺陷导出
工具可以根据项目和缺陷状态导出相应的缺陷内容,目前支持Excel和HTML两种导出方式,JSON,TXT,CSV方式待补充

* Excel导出

点击导出后会在根目录下生成一个 `缺陷导出表.xls` 

* HTML

HTML格式要求在根目录下自行新建一个`htmlBugDetails`目录,用来存放导出记录的详情,根目录下的`index.html`打开后会展示导出的所有记录,点击编号可查看bug的详情

## 身份证生成

* 输入限制只能输入int类型.
* 暂未做int大小控制.


### 缺陷记录的config
前端展示的大部分内容都在配置文件中。

* COLLECTION 表示MongoDB中的数据集合
* TESTER 表示测试人员
* DEVELOPER 表示开发人员
* TERMINAL 表示终端
* BUGSTATUS 表示缺陷状态

## 数据库表

* bugContent 存储缺陷的内容
* bugID 存储缺陷ID的自增字段
* bugStatus 存储缺陷的状态（映射表）
* category 存储前端nav的记录
* project 存储缺陷管理中的项目名称
* bugArchive 每日bug统计归档

## 感谢
感谢 phinexdaz 提供的身份证生成接口