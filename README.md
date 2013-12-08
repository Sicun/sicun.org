#TODO
- - - 
<h3 align="center"><a href="http://pan.baidu.com/s/1BwjuY">原型图.psd</a></h3>  
![原型图.png](http://it-eproducts.com/images/sicuni-1386512974.png)  
 
##全局  
 * 可选的标记语言：markdown，reStructuredText和改进的markdown语法（默认，空白字符自动转义）
 * 游客权限：消息、分享、活动、作品、关于
  
- - - 
##主页  
[消息][message] | [项目][project] | [作品][works] | [关于][about]

- - -
###[消息][message]  
 * 前缀`!!!`转[通知][notice]发送
 * 前缀`~~~`转[分享][share]发送
 * 前缀`@@@`转[活动][activity]发送
 * 前缀`@`同twitter
 * 默认为字面含义，只有`title`和`content`  
 * 输入前缀后，输入框变化成对应条目

####[通知][notice]  
 * [](显示位置)按`时间` `内容摘要` `受众`格式和时间排序置于[消息][message]最上方
 * [](功能摘要)`内容` `时间` `受众`，渐进披露：`类别` `地点` `是否短信通知` `是否邮件通知`
 * `受众`自动补全，自动替换`时间`格式为`距今时间`或`yyyy-mm-dd hr:mi`
 * `受众`包括：成员、项目组、组、全体

####[分享][share]  
 * 显示在右边，显示格式：`条目名 说明`
 * 文章链接或上传文件
 * 上传文件时自动填充`条目名`

####[活动][activity]  
 * 显示在[分享][share]上面
 * `时间` `地点` `内容`，渐进披露：`费用` `集合点` `集合时间`
 * 只显示__未完成的活动__

####[思存动态][doing]  
 * 显示在[分享][share]上面，活动下面
 * `内容`
 * 自发布日起显示7天

- - - 
###[项目][project]  
 * [](显示格式)`项目名` `想法摘要` `需要人员` `发起人`
 * [](详细功能)`定义` `定位` `目标` `动态`

- - -  
###[作品][works]
 * 展示成员code toy
 * 提供工具，如：在线调色板等

- - - 
###[关于][about]
 * `留脚印` `团队介绍` `业务介绍` `加入我们`
 
##搜索
 * `用户` `通知` `消息` `图书`

[index]: http://www.sicun.org 
[login]: http://www.sicun.org/login 
[joinus]: http://www.sicun.org/joinus "邮箱、姓名、专业、年级、技能或经历"
[message]: http://www.sicun.org/message  
[notice]: http://www.sicun.org/notice "通知或公告"
[share]: http://www.sicun.org/share 
[activity]: http://www.sicun.org/activity 
[doing]: http://www.sicun.org/doing "思存动态" 
[project]: http://www.sicun.org/project "项目"
[works]: http://www.sicun.org/works "作品"
[about]: http://www.sicun.org/about
