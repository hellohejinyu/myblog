# MyBlog

1、系统运行前准备
打开安装MySQL-python-1.2.5.win-amd64-py2.7.exe，用于Python连接MySQL；
给计算机安装Python 2.x环境，安装采用默认选项即可；
打开cmd，输入pip install Django==1.8.2 安装1.8.2版本的Django；
安装MySQL环境，端口为默认的3306，用户名root，密码root，用于后续数据库创建。

2、解压myblog文件夹到任意目录，cmd进入manage.py同级目录下，输入python manage.py makemigrations 和 python manage.py migrate 来创建数据库；

3、输入 python manage.py createsuperuser，然后根据提示创建超级管理员账号；
超级管理员账号用于创建博客大类名称，否则用户无法新建博客

4、在cmd输入python manage.py runserver 8080，表示启动在8080端口启动服务，此时打开浏览器输入http://localhost:8080即可进入系统。输入http://localhost:8080/admin用刚才创建的超级管理员账号登录，新增文章大类，然后就可以使用整个系统了。
