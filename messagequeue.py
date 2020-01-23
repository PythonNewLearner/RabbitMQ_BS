#build producer and consumer
import pika
import time

class MessageQueue:
    def __init__(self,host,port,virtualhost,username,password,exchange_name,queue_name):
        url = 'amqp://{}:{}@{}:{}/{}'.format(username,password,host,port,virtualhost)
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange_name, 'direct')
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        self.channel.queue_declare(queue_name,exclusive=False)  # this is for consumer
        self.channel.queue_bind(queue_name,exchange_name)

class Producer(MessageQueue):
    def SendMsg(self,msg:str):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.queue_name, body=msg)  # No setting for routin_key:queue_name is same as routin_key

class Consumer(MessageQueue):
    def ReceiveMsg(self):
        _,_,body = self.channel.basic_get(self.queue_name,True)
        return body

#testing the class Producer and Consumer
if __name__ == '__main__':
    p1=Producer('192.168.126.129','5672','test1','baichen111','12345','news','htmls')
    c1 = Consumer('192.168.126.129', '5672', 'test1', 'baichen111', '12345', 'news', 'htmls')
    for i in range(40):
        p1.SendMsg('data-{}'.format(i))

    for i in range(100):
        msg = c1.ReceiveMsg()
        if msg:
            print(msg)
        else:
            time.sleep(1)




