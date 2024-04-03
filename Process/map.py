import os,zipfile,time,subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from Process.MySignal import signal1

def unzip_file(zip_filepath, dest_path) -> None:
    if os.path.exists("temp"):
        os.system("rd /s/q temp")
    with zipfile.ZipFile(zip_filepath, 'r',) as zip:
        zip.extractall(dest_path)

def zip_dir(dirname, zipfilename) -> None:
    with zipfile.ZipFile(zipfilename, 'w') as zip:
        for root, dirs, files in os.walk(dirname):
            for file in files:
                zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dirname))

def judge_maptype() -> str:
    maptype:str="None"
    for root, dirs, files in os.walk("./temp"):
            for file in files:
                if file.endswith(".osu"): 
                    maptype="osu"
                    break
                elif file.endswith("mc"):
                    maptype="malody"
                    break
                elif file.endswith(".sm"):
                    maptype="etterna"
                    break
    signal1.emit(f"the MAPTYPE is:{maptype}")
    #print("the MAPTYPE is:",maptype)
    return maptype

class Map:
    
    enum={"osu":0,"mc":1,"sm":2}
    def __init__(self,map_path) -> None:
        self.version:list=[] #record the name of the beatmap
        self.music:list=[]   #record music paths
        self.bpmlist:list=[] #record the bpm
        self.maplist:list=[] #record the beatmap path
        self.title:str=""    #record the beatmap title
        self.root:str=""     #record the beatmap root
        sox_path = 'Tool/sox'
        # 获取当前的path环境变量
        path = os.environ.get('PATH', '')
        # 将想要添加的路径追加到path变量中，用分号分隔
        path = sox_path+";" + path
        # 将修改后的path变量设置为新的环境变量
        os.environ['PATH'] = path
        self.title=os.path.basename(map_path).split(".")[0]

    def change_speed_and_pitch(self, input_file, output_file, speed):
        # 创建一个命令列表
        if speed < 1:
            cmd = ['sox', input_file, output_file, 'tempo', str(speed)]
        else:
            cmd = ['sox', input_file, output_file, 'speed', str(speed)]
        # 使用subprocess运行命令，并隐藏输出
        subprocess.run(cmd,creationflags=subprocess.CREATE_NO_WINDOW)
        signal1.emit(f"processing:{input_file}->{output_file} speed:{speed}... done!")
    def get_split(self,selected_map,pos):
        return os.path.splitext(self.music[selected_map])[pos]
    def change_info(self,select_map,speed_rate) -> None:
        pass

    def change_filename(self,path, rate):
        path = Path(path)
        new_name = path.stem + f"x{rate}" + path.suffix
        new_path = path.with_name(new_name)
        return str(new_path)
    def process(self,selected_map,rate):
        self.change_speed_and_pitch(self.music[selected_map],self.change_filename(self.music[selected_map],rate),rate)
        self.change_info(selected_map,rate)
    def pack(self,maptype):
        if not os.path.exists("out"):
            os.makedirs("out")
        zip_dir('temp', f'out/{self.title}'+f'{".osz"if maptype=="osu" else ".mcz" if maptype=="malody" else ".zip"}')
        os.system("rd /s/q temp")
    def get_version(self):
        return self.version
    def get_title(self):
        return self.title
    #maptype:osu ||malody ||etterna
    def run(self,maptype,speed_rate,version):
        selected_map=self.version.index(version)
        
        begin=time.time()
        signal1.emit(f"start processing!{self.title} {speed_rate}\n"
              "if the audio file is an MP3 file, the speed may be slower please wait patiently!")
        
        with ThreadPoolExecutor() as executor:
            executor.map(partial(self.process,selected_map),speed_rate)
        # for rate in speed_rate:
        #     self.process(selected_map,rate)
        signal1.emit(f"Total cost:{time.time()-begin:.2f}s")
        #packed 
        self.pack(maptype)

