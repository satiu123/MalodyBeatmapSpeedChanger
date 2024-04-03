import Process.malody as malody,Process.osu as osu,Process.etterna as etterna
import threading,queue,time
from Process.map import unzip_file,judge_maptype
from Process.MySignal import signal1,signal2
# 创建一个全局变量来存储run线程和队列
game=None
user_has_chosen:bool = False
version:str=""
run_thread = None
run_queue = queue.Queue()
stop_thread = False

def run(map_path,rate):
    global version,user_has_chosen,game
    maptype=getVersion(map_path)
    #等待用户选择
    while not user_has_chosen:
        if stop_thread:
            signal1.emit("The thread has been stopped!") 
            signal1.emit("")
            return
        time.sleep(1)
    user_has_chosen = False
    game.run(maptype,rate,version) #type:ignore
def getVersion(map_path):
    global game,stop_thread,version,user_has_chosen
    map_path=map_path.strip('"')
    unzip_file(map_path,"./temp")
    maptype=judge_maptype()
    if maptype=="osu":
        game=osu.Osu(map_path)
    if maptype=="malody":
        game=malody.Malody(map_path)
    if maptype=="etterna":
        game=etterna.Etterna(map_path)
    map_version=game.get_version() #type:ignore
    if map_version.__len__()==1:
        version=map_version[0]
        user_has_chosen =True
        stop_thread=False
    else:
        signal2.emit(game.get_version(),game.get_title()) #type:ignore
    return maptype #type:ignore
def addQueue(rate_dict):
    # 将参数添加到队列中
    for map_path in rate_dict.keys():
        run_queue.put((map_path, rate_dict[map_path]))

def processQueue():
    while not run_queue.empty() and stop_thread==False:
        # 从队列中获取参数
        map_path, rate = run_queue.get()
        # 运行run函数
        run(map_path, rate)
    # 通知队列任务已完成
    if run_queue.empty():
        run_queue.task_done()
        signal1.emit("All done!") 
def startQueue() -> None:
    global run_thread,stop_thread,user_has_chosen
    if run_thread is not None and run_thread.is_alive():
        return
    if run_queue.empty():
        signal1.emit("The queue is empty!")
        return
    user_has_chosen = False
    stop_thread=False
    run_thread = threading.Thread(target=processQueue)
    run_thread.start()

        




