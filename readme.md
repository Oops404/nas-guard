# 使用说明

> 欢迎关注 bilibili id: 1489684 翻滚吧年糕君，联系邮箱：cheneyjin@outlook.com
>
> **！若感觉自己动手能力欠佳，可以购买能发送关机命令的UPS。本脚本，意在折腾着玩。！**

**nas_guard_py*.py**脚本运行一共需要三个参数，说明如下：

```
# -r 为路由网关，若路由找不到了说明家里断电了或断网了，nas自动关机。
# -p 为目标IP开放的端口号，本使用场景下就是路由的WEB后台端口，一般80，也可以自己按情况设置。
# -t 为容许多少次检测不到路由，举例：“-t 3”，含义为3次无法和路由通讯，则触发关机。
```

**举例py脚本单独运行：**

```basic
python nas_guard_py3.py -r 192.168.1.1 -p 80 -t 3
```

**注意：**脚本启动后，会睡眠20分钟。意在等待系统启动，避免系统没启动完成，无法通讯，陷入不停关机的境地，因此不要随便删除。

### WINDOWS添加自启动

* 安装好python2或者python3。

* 编写批处理BAT，若安装了python3则使用-py3的python脚本，否则使用-py2的脚本，内容如下：

  > ```shell
  > python /路径/nas_guard_py3.py -r {ip} -p {port} -t {count}
  > ```

3. 然后将批处理存放于“C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp”即可。


### QNAP NAS添加自启动
> **！autorun.sh 用于QNAP（威联通）自定义开机启动项，其他类unix系统可依据系统情况自行编写bash运行nas_guard_*.py ！**

* 使用PUTTY.EXE或者WinScp，ssh到NAS上。

* 挂载特殊分区。

  > ```bash
  > cd /tmp/config
  > mount $(/sbin/hal\_app --get\_boot\_pd port\_id=0)6 /tmp/config
  > ```


* 用编辑器打开"autorun.sh"，根据情况改写参数。然后将"autorun.sh"移动到/tmp/config下。

* 增加可执行权限。
	
	> ```bash
	> chmod +x /tmp/config/autorun.sh
	> ```
	
* 取消挂载。
	
	> ```bash
	> umount /tmp/config
	> ```
	
* 自启动开关位于：控制面板 -> 系统 -> 硬件 -> 一般设置 -> 启动时运行用户定义的进程（查看autorun.sh）。

* nas_guard_py2.py 存放至"/share/CACHEDEV2_DATA/Public/"内。

----------

### 欢迎支持

![](欢迎支持.jpg)

