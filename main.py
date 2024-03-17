import Module.Process.malody as malody,Module.Process.osu as osu,Module.Process.etterna as etterna
import threading,queue,time
from Module.Process.map import unzip_file,judge_maptype
from Module.Process.map import info_signal
from Module.Gui.MySignal import MySignal
getinfo_signal = MySignal()
# 创建一个全局变量来存储run线程和队列
game=None
user_has_chosen:bool = False
version:str=""
run_thread = None
run_queue = queue.Queue()
stop_thread = False

def run(map_path,rate):
    global version,user_has_chosen,game
    rate=list(map(float,rate.split()))
    maptype=getVersion(map_path)
    #等待用户选择
    while not user_has_chosen:
        if stop_thread:
            info_signal.signal1.emit("The thread has been stopped!") 
            return
        time.sleep(1)
    user_has_chosen = False
    game.run(maptype,rate,version) #type:ignore
def getVersion(map_path):
    global game,stop_thread
    map_path=map_path.strip('"')
    unzip_file(map_path,"./temp")
    maptype=judge_maptype()
    if maptype=="osu":
        game=osu.Osu(map_path)
    if maptype=="malody":
        game=malody.Malody(map_path)
    if maptype=="etterna":
        game=etterna.Etterna(map_path)
    getinfo_signal.signal2.emit(game.get_version(),game.get_title()) #type:ignore
    return maptype #type:ignore
def addQueue(map_path, rate):
    global run_thread
    # 将参数添加到队列中
    run_queue.put((map_path, rate))
def processQueue():
    while not run_queue.empty():
        # 从队列中获取参数
        map_path, rate = run_queue.get()
        # 运行run函数
        run(map_path, rate)
    run_queue.task_done()
    info_signal.signal1.emit("All done!") 
def startQueue() -> None:
    global run_thread,game
    if run_thread is not None and run_thread.is_alive():
        return
    run_thread = threading.Thread(target=processQueue)
    run_thread.start()

        




