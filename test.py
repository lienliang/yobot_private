import time

localtime = time.localtime(1590379200)
ticks=time.strftime("%Y-%m-%d %H:%M:%S",localtime )

ticks2=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()) )
print(ticks)
print(ticks2)

