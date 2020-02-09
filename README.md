# SiteScan
SiteScan是一款探测网站存活概率的工具,在对批量目标网站( 域名 或 ip:port)进行渗透测试的时候，第一步需要筛选出可能存活站点，排除异常站点。


#### 主要功能
* * *
- 使用异步协程批量快速扫描
- 要结合响应码和其他因素判断网站存活概率
- 结果保存CSV格式，分为html返回（url  |  status code | title） 和 json返回 （url  |  status code | JSON信息），二者皆无返回None



#### 多因素分析常见响应码
* * *
网站是否有潜在利用价值
- 200相关
> 需要结合页面关键字、响应headers content-length、页面相似度等判断网站状态

- 30x
> 允许requests 跳转，获取title

- 403相关
如果网站根目录扫描返回403？此时访问根目录url+随机字符：
> 1. 如果返回403，则有一定概率是除了根目录下的某些资源可能访问外，访问其他资源都返回403
> 2. 如果返回404，则有一定概率是，网站默认首页文件配置错误

- 404相关
> 如果网站根目录扫描返回404？此时访问根目录url+随机字符：
> 如果返回404，可能根目录下除了某些资源可访问外，其他都返回404

- 50x
> 重试处理，可能网站某段时间服务端异常，需要多次请求才能判断



#### 扫描结果分类保存CSV文件：
* * *
- 正常网站： 响应码 20x  、30x为主，个别 40x
- 大概率正常网站：404为主，少量其他常见响应码
- 小概率正常网站：403为主，少量其他常见响应码
- 异常网站，服务端异常：50x为主 
- 不太常见的响应码：个别常见响应码会出现在这个分类，如：401、200等

#### 后续计划
* * *
- 各个功能持续优化和完善
- 响应码400情况，逻辑需要完善
