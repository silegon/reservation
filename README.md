Django 订餐程序
===========

项目地址：
https://github.com/silegon/reservation


典型环境：
    小型公司里有几十号人，每天告诉前台MM想吃什么外卖，然后前台MM统一打电话到各个外卖。

解决的问题：
* 减少每天与前台的沟通成本
* 减少以前人工操作下有人外卖被漏需要饿肚子的情况
* 可以提前预订实物 
* 可以看到全部的外卖菜单
* 自动算账记账

chrome下基本能用，未完成css兼容和js兼容。
测试运行步骤：
* 修改参数 
    修改settings.py中的数据库参数。
    修改"STATIC_URL"为正确的完整地址。
    PS:Django 自带测试服务器模式下相对路径虽然在html页面显示是一样的，但是Django自带静态文件会服务会不正常。

* mysql数据库中添加相关数据库
    create database reservation

* 同步数据库:
    ./manage.py syncdb 

* 导入初始测试数据:
    python manage.py loaddata test_data.json
    PS:有兴趣可以参考：http://stackoverflow.com/questions/853796/problems-with-contenttypes-when-loading-a-fixture-in-django

* 启动测试服务器:
    python manage.py runserver <your ip address:port>

* 相关测试账号密码:
    用户测试账号:xxx
    用户测试密码:xxx

    管理账号:demo
    管理密码:demo

Todo:
* 文档
* 前端修改兼容

修改记录：
* 2012/6/7 完善文档，修改models.py中的括号的歧义，添加初始测试文件。
* 2012/6/5 github上发布Django 订餐程序
