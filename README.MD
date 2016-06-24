# 测试工具箱
后端使用Django+MongoDB，前端使用Django的模板渲染和jQuery+Bootstrap处理。

## 功能说明
* Web端测试（未完成）
* 移动端测试（未完成）
* 接口测试（未完成）
* 抓包测试（未完成）
* 缺陷记录（已完成）
* 身份证生成(已完成)

## 缺陷记录
### 操作数据库
操作MongoDB的方法都在mongodb包内。非完全，有待补充。

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

## 感谢
感谢 phinexdaz 提供的身份证生成接口