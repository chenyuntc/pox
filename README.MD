##POX是一个开源的OpenFlow 控制器，我们是来自北邮的创项目数据并行计算的软硬件项目成员，我们fork了POX之后
参考POX的相关代码，实线了主要以下三个功能
1. 简单的防火墙
2. 缓存服务器
3. 负载均衡集群
相关代码均存放forwaring 文件夹下
 
 
 ####欲实现相关功能打开相关文件 ，比如要验证负载均衡功能
 ```
 you—directory/pox.py forwarding.l3_learning misc.ip_loadbalancer --ip=10.0.0.15 --servers=10.0.0.1,10.0.0.2,10.0.0.3 
```
然后用mininet实验平台打开
sudo mn  --topo single,4 --mac  --controller remote

在然后
```
mininet> h1 python /home/floodlight/server1.py &
mininet> h2 python /home/floodlight/server2.py &
mininet> h3 python /home/floodlight/server3.py &
mininet> h4 firefox &
  ```
  其中serve的代码在web/文件夹下
  
  
  
  以上
