import os,zipfile,time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
def unzip_file(zip_filepath, dest_path) -> None:
    if os.path.exists("temp"):
        os.system("rd /s/q temp")
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
def zip_dir(dirname, zipfilename) -> None:
    with zipfile.ZipFile(zipfilename, 'w') as zipf:
        for root, dirs, files in os.walk(dirname):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dirname))
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
    print("the MAPTYPE is:",maptype)
    return maptype
class Map:
    version:list=[] #record the name of the beatmap
    music:list=[]   #record music paths
    bpmlist:list=[] #record the bpm
    maplist:list=[] #record the beatmap path
    title:str=""    #record the beatmap title
    root:str=""     #record the beatmap root
    enum={"osu":0,"mc":1,"sm":2}
    def __init__(self,map_path) -> None:
        sox_path = 'Tool/sox'
        # 获取当前的path环境变量
        path = os.environ.get('PATH', '')
        # 将想要添加的路径追加到path变量中，用分号分隔
        path = sox_path+";" + path
        # 将修改后的path变量设置为新的环境变量
        os.environ['PATH'] = path
        self.title=os.path.basename(map_path).split(".")[0]
    def change_speed_and_pitch(self,input_file, output_file,speed):
        import sox
        # 创建一个 transformer 对象
        tfm = sox.Transformer()
        # 设置音频的速度和音调
        if speed<1:
            tfm.tempo(factor=speed)
        else:
            tfm.speed(factor=speed)
        tfm.build(input_file, output_file)
        print("processing:",input_file,"->",output_file,"speed:",speed,"... done!")
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
        input("All done!Press Enter to check...")
        os.startfile("out")
    #maptype:osu ||malody ||etterna
    def run(self,maptype):
        if not self.version:
            print("0:No Name")
        for mapp in self.version:
            #当没有难度名时，输出"No Name"
            if not mapp:
                print(self.version.index(mapp),":","No Name")
            else:
                print(self.version.index(mapp),":",mapp)
        selected_map=int(input("input choice(eg:0)：\n"))
        speed_rate = [float(rate) for rate in input("input Speed (eg:1.1 1.3 1.4)：\n").split()]
        begin=time.time()
        print("start processing!\n"
              "if the audio file is an MP3 file, the speed may be slower please wait patiently!")
        with ThreadPoolExecutor() as executor:
            executor.map(partial(self.process,selected_map),speed_rate)
        print(f"Total cost:{time.time()-begin:.2f}s")
        #packed 
        self.pack(maptype)
