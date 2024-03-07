import os,zipfile,time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from threading import Lock
class Map:
    version:list=[] #record the name of the beatmap
    music:list=[]   #record music paths
    bpmlist:list=[] #record the bpm
    maplist:list=[] #record the beatmap path
    title:str=""    #record the beatmap title
    root:str=""     #record the beatmap root
    enum={"osu":0,"mc":1,"sm":2}
    def __init__(self) -> None:
        self.lock=Lock()
        sox_path = 'Tool/sox'
        # 获取当前的path环境变量
        path = os.environ.get('PATH', '')
        # 将想要添加的路径追加到path变量中，用分号分隔
        path = sox_path+";" + path
        # 将修改后的path变量设置为新的环境变量
        os.environ['PATH'] = path
        map_path=input("Please input FilePath(eg：d:/malody/export/Grief & Malice.mcz)：\n")
        map_path=map_path.strip('"')
        if os.path.exists("temp"):
            os.system("rd /s/q temp")
        self.unzip_file(map_path, "./temp")
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
    #unpacking
    def unzip_file(self,zip_filepath, dest_path) -> None:
        self.title=os.path.basename(zip_filepath).split(".")[0]
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(dest_path)
    #pack
    def zip_dir(self,dirname, zipfilename) -> None:
        with zipfile.ZipFile(zipfilename, 'w') as zipf:
            for root, dirs, files in os.walk(dirname):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dirname)) 
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
    #maptype:osu ||malody ||etterna
    def run(self,maptype):
        for mapp in self.version:
            print(self.version.index(mapp),":",mapp)
        selected_map=int(input("input choice(eg:0)：\n"))
        speed_rate = [float(rate) for rate in input("input Speed (eg:1.1 1.3 1.4)：\n").split()]
        begin=time.time()
        print("start processing!")
        with ThreadPoolExecutor() as executor:
            executor.map(partial(self.process,selected_map),speed_rate)
        print(f"Total cost:{time.time()-begin:.2}s")
        #packed 
        if not os.path.exists("out"):
            os.makedirs("out")
        self.zip_dir('temp', f'out/{self.title}'+f'{".osz"if maptype=="osu" else ".mcz" if maptype=="malody" else ".zip"}')
        os.system("rd /s/q temp")
        input("All done!Press Enter to check...")
        os.startfile("out")
