from multiprocessing import Process, Queue
import time


class base():
	q = Queue()
	def __init__(self):
		pass
	def start(self):

		p = Process(target=self.run1,args=(4,self.q))
		p.deamon = True
		p.start()
		p.join()
		#print(self.q.get())
	def run1(self,n,q):
		t0 = time.time()
		for i in range(n):
			time.sleep(0.1)
		dt = time.time() - t0
		#print(dt)
		#if not q in None:
		q.put(dt)
		return dt


k = base()
k.start()
print(k.q.get())
