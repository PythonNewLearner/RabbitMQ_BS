# RabbitMQ_BS
Crawling Chinese news from website: https://news.cnblogs.com/
Pushing the data to RabbitMQ, then take the data from RabbitMQ and save it.



Make sure RabbitMQ is running:
![Image description](https://github.com/PythonNewLearner/RabbitMQ_BS/blob/master/rabbitmq_status.png)

Port Check: <br>
5672 is listening<br>
15672 is for web app<br>
25672 is for clustering<br>
![Image description](https://github.com/PythonNewLearner/RabbitMQ_BS/blob/master/portal_check.png)

Input:<br>
IP: 192.168.126.129<br>
Port: 5672<br>
Virtual host: test1<br>
User name: baichen111<br>
Password: 12345<br>
Exchange name: news<br>
Queue names: urls,htmls, outputs<br>


Running pragramme: RabbitMQ received data
![Image description](https://github.com/PythonNewLearner/RabbitMQ_BS/blob/master/rabbitmq_running.png)


Consumer received the data and saved it in html file:
![Image description](https://github.com/PythonNewLearner/RabbitMQ_BS/blob/master/pycharm_datashow.png)
