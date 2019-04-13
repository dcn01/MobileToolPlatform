**注意：修改模块名后，记得将类中的import修改，还要清除一下原先编译好的pyc文件**

### 技术实现所使用到的python模块及方法：
1. flask：jsonify、request、abort、make_response、url_for
2. flask-httpauth：HTTPBasicAuth
3. flask-restful：reqparse.RequestParser、Api、Resourceen、endpoint、fields、marshal
4. fields.Uri、request.json、request.values

add_resource 函数使用指定的 endpoint 注册路由到框架上。如果没有指定 endpoint，Flask-RESTful 会根据类名生成一个，但是有时候有些函数比如 url_for 需要 endpoint，因此我会明确给 endpoint 赋值。
fields.Uri 是一个用于生成一个 URL 的特定的参数。 它需要的参数是 endpoint。


**这块改造为接口的工程思想来自ApkInstallTool(改名：PyGuiForAndroidTest)功能，所以版本线需求接着上次的**

controller：该层处理接口中的业务逻辑
domian：该层主要是数据模型及蒙版的设计
service：该层对外提供接口，可以通过网络url访问
utils:实现一些常用的工具类
managers:这里有个modules模块主要是管理接口使用了那些库、模块、方法，学习阶段为了方便统计管理和移植，正式生产没必要这么做

*******************************************************************

### 第十四版修改需求：20171021

```text
    1.构建设备信息获取接口  get请求（先不添加header和token）获取：手机的各种信息
    2.为改接口设置404和500的错误提示
    3.为后台接口添加日志配置
        import logging
        file_handler = logging.FileHandler('app.log')
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
    4.为接口的请求加上参数验证
    5.全局对象
        config 当前配置对象 (flask.config)
        request 当前请求对象 (flask.request)
        session 当前会话对象 (flask.session)
        g 实现全局变量的请求范围的对象 (flask.g)
        url_for()  flask.url_for() 函数。
        get_flashed_messages() flask.get_flashed_messages() 函数。

    6.使用工厂方法来设计app的实例化,在v1.0中我们使用了混合的方式，来处理api和app的错误
      v1.1的版本主要以app的错误来处理错误，那这样我们在v1.2中全面使用api的方式来处理系统的所有错误

    7.接口都需要什么操作？链接的参数校验、错误处理、数据库操作、网络状态处理、加密解密处理、cookie和session处理等

    8.对于这个项目的基建部分，重新构建了一下，主要还是以adb为核心，分别对device和app进行场景需求，如device手机设备的一些硬件信息
      、运行时信息，app应用的属性和运行时数据，其中对应的场景有：电量、cpu、内存、网络（流量）、启动时间等，那么在接口api中会起到
      什么作用？其实就只是填充和优化测试过程中的数据获取，该工程主要是为了flask-restful api而生，所以后期还是主攻API，然后后续的
      appium自动化测试看看是否可以贯穿一起
      也就是基建部分到此结束，后面api实践过程再进行优化和实例
```

### 第十五版修改需求：20171122

```text
    1.修改数据获取的中间方式，及返回数据后的检验方式（设备连接校验、对象属性校验）
    2.整个数据流程更流程和低耦合化
    3.已经实现了两个查询的接口，一个是获取手机信息、一个是获取运行时信息，那么后面我么需要添加
      a.通过接口进行手机的apk安装和卸载
      b.手机的重启
      c.清理数据
      ...
    4.token使用方式，user和passw加时间来控制可用性，提供token解密和验证的方法，接口请求的token不可用就返回失败。
```

### 最后的描述 20190413

```
作为一个测试开发，在质量体系中，去构建辅助和补充测试场景的工具，技术选型是多样性的，编程语言也是数不胜数,
其实这个也不用很纠结，这个选择取决你的兴趣、已有的基础、所在环境的现状。目前的我，是一个综合性的存在，
会使用java、python、jquery编程技术去完成测试工具的实现，挑战性，其实蛮多，也在于实际的应用
和困难取舍，这里需要学会的就是‘拥抱变化’。本工程其实有很多文件夹内容被ignore，但开放出来的很有用，目前也还在用
做简单的服务平台（flask+pymsyql+pandas+flask-restful）
```