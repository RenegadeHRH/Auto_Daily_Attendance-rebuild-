# Auto_Daily_Attendance-rebuild-
>莞工每日疫情打卡  
>**自动虽省事，疫情勿轻视**  
>**程序为保险，打卡看着点**  
>特别鸣谢：hug，Doctor.Wu
>此readme面向小白，篇幅很长请见谅
##  部署指南  
###  一.fork本仓库(上游仓库)  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/173821_c9edd6b4_4796963.png "屏幕截图.png")  
选择你的账户：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/173925_81654206_4796963.png "屏幕截图.png")  
之后跳转到的这个界面就是你的fork界面，这个项目下你可以随意改变代码，不会影响到上游仓库  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/174515_5d7365fe_4796963.png "屏幕截图.png")
###  二.配置secret
接下来点击settings  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/174554_8f0a2f23_4796963.png "屏幕截图.png")  
可以看到secects，点击它：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/174633_0d7fc646_4796963.png "屏幕截图.png")  
新fork下来的项目是什么都没有的，需要我们自己创建，所以点击New repository secret   
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/174724_7e4ed2c0_4796963.png "屏幕截图.png")  
添加第一个secret，USER，这个对应的是你的学号  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/174927_dc4cf1b2_4796963.png "屏幕截图.png")  
这样就添加好了  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/175004_451da9f6_4796963.png "屏幕截图.png")  
现在还要再添加一个密码  
>**密码是不会传输出去的，只保存在GitHub，也不会被别人看见，代码里也没有把账号密码发送到除了中央认证以外的地方**  

![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/175204_7cd42a77_4796963.png "屏幕截图.png")  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/175240_452d3def_4796963.png "屏幕截图.png")  
现在基本配置就完成了，接下来配置Ation才能启动workflow
###  三.配置Action  
点击上方菜单栏Actions  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/180230_ba662412_4796963.png "屏幕截图.png")
不用理提示说的啥，直接点击  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/180306_7c9e802d_4796963.png "屏幕截图.png")
这时候我们的workflow还不能运行点击enable workflow  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/180457_119aa34a_4796963.png "屏幕截图.png")  
这时候workflow应该就是处于等待运行状态了，实际上并没有触发流程，因为没有到时间（半夜一点半和两点半触发一次）（通常  
也没人在这个点fork项目吧(lll￢ω￢) ）  
但是为了能够测试项目到底能不能正常运行，我们可以点击一下star，强制触发流程：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/180817_6730a894_4796963.png "屏幕截图.png")  
点击以后等待大约半分钟，然后刷新  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/181320_d0f79057_4796963.png "屏幕截图.png")  
可以看到一个绿的 签到 出来了，也就是执行成功了  
如果没有执行成功，我们可以点击进去看他的日志  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/181412_8ed61937_4796963.png "屏幕截图.png")  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/181427_b1d64fe1_4796963.png "屏幕截图.png")  
点击展开  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/181454_ac5c9454_4796963.png "屏幕截图.png")  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/181534_14e9aca2_4796963.png "屏幕截图.png")  
##  实现原理/自定义  
·本项目是通过发包实现的  ***登录->获取数据->提交数据***  来完成疫情填报的，疫情填报的位置判断可能是在前端，我在测试的时候没有  
·遇到因为定位而无法提交的  
·自动化使用了github提供的workflow，能够在GitHub上的服务器跑我的定时任务 
·本项目可以一次多账号打卡，只需要在添加账号和密码的时候把账号或密码用#隔开（一定要一一对应）  
·关于调整打卡时间：
如果使用默认的打卡时间，一旦使用本项目的人多起来，可能也无法正常打卡，所以建议自行修改打卡时间：  
进入code界面：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182505_87d3b7c4_4796963.png "屏幕截图.png")  
进入目录：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182522_ddea3018_4796963.png "屏幕截图.png")  
点击：
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182704_15d67d3c_4796963.png "屏幕截图.png")  
点击：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182741_afb82692_4796963.png "屏幕截图.png")  
在这里修改定时任务时间：  
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182814_20144c6c_4796963.png "屏幕截图.png")  
***注意：鼠标移到上面显示的是UTC时间，要换成北京时间***
![输入图片说明](https://images.gitee.com/uploads/images/2021/0118/182910_be970ec6_4796963.png "屏幕截图.png")  
要调整成什么时间大家可以手动修改试试  
其他代码尽量不要随意调整  
  
