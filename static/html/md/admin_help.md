#欢迎试用游易点餐管理系统
管理系统分为管理前台和管理后台两部分

##管理前台界面
![管理前台界面](/static/img/help/admin_frontend_interface.jpg)

1. 订单获取栏
2. 额外点餐栏
3. 未点餐栏
4. 协助点餐跳转栏
5. 订单预订栏
6. 订单确认栏
7. 订单完成栏

##管理前台订单处理流程
1. 用户预订食物
2. 后台显示预订食物列表、未点餐列表、额外点餐列表。
    * 出现未点餐列表：各种方式通知用户点餐，必要时可以协助用户点餐
    * 出现额外点餐列表: 说明该用户在计划外，看是否应该调整订餐方案
3. 电话联系食物提供商，如果得到确认则点击订单预订栏的确认按钮。
    * 如果食物提供商不能提供该食物，可以在该阶段取消食物预订，通知用户有变更。
4. 当食物送过来后，点击订单确认栏的完成按钮，完成该订单。

### 注意事项
* 管理前台页面不能即时反应最新的信息，需要看到最新的用户预订信息可以刷新网页，网页会每5分钟自动刷新一次


##管理后台界面
![管理后台界面](/static/img/help/admin_backend_interface.jpg)
##管理后台
管理后台提供各个数据的设置查看，更改功能。
* 外卖服务提供商
  查看、添加、修改各个食品提供商的信息
  查看、添加、修改相关食物提供商的具体食物

* 扣费记录
  * 查看、修改扣费记录

* 用户账号
  * 设置用户点餐权限
  * 修改用户密码(稍微有点复杂)

* 订单
    
* 食物
  * 编辑食物相关信息
  * 设置食物是否提供
  * 验证用户提交的食物菜单(未验证的菜单会显示  用户id:食物名)

### 注意事项
* 管理后台的数据管理功能过于强大。请小心修改，尤其不要删除信息。