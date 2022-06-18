# BilibiliSuitBuy

⭐︎⭐︎⭐︎不要看没有支付操作了，如果b币充足可以直接完成购买⭐︎⭐︎⭐︎

B站抢装扮脚本(一起烂吧)

抓包教程也在里面

设置BuyConfig

看config命名应该都看的懂吧，抓包软件一个一个复制就行

Fiddler抓包教程 (http/https)

安卓7抓包(http/https)

前置:[Fiddler Classic](https://www.telerik.com/download/fiddler) 和 一部root的安卓手机或安卓模拟器(安卓7以下可以不看)

1.设置Connections( Tools - Options - Connections )

![fiddler-connections](/img/fiddler-connections.png)

2.安装CA证书( Tools - Options - HTTPS )

![fiddler-https](/img/fiddler-HTTPS.png)

导出证书到桌面 Tools - Options - HTTPS - Actions - Export Root Certificate to Desktop

![fiddler-cer](/img/cer.png) 随便找个方法把证书发送到手机 - 这里我用夜神模拟器来模拟

![phone-root](/img/phone-root.png)

我的模拟器系统是安卓9-64bit(必须开启root)

![cer-path](/img/cer-path.png)

从 设置 - 安全性和位置信息 - 加密与凭据 - 从SD卡安装

找到发送到手机上的证书直接安装

打开文件管理器找到/data/misc/user/0/cacerts-added/xxxxx.0

这个就是刚刚安装在用户证书里的fiddler证书

把.0文件复制到/etc/security/cacerts 下(用户证书移系统证书)

3.抓包

打开Win+R输入cmd

cmd输入ipconfig

找到你的内网ip

打开手机wifi设置

![cer-path](/img/wifi-http.png)

保存后打开fiddler就可以抓手机端的https包了
