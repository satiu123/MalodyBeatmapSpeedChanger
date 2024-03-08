from Module.map import Map
from functools import partial
import os,re,io
def multiply_bpm(match,speed):
    number = float(match.group(1))
    return f"={number * speed}"  # 乘以speed参数
def multiply_offset(match, speed):
    number = float(match.group(1))
    return f"#OFFSET:{number / speed}"  # 乘以speed参数
def replace_music(match,music:str,speed:float):
    temp=music.strip().split(".")
    return f"#MUSIC:{temp[0]}x{speed}.{temp[1]}"
class Etterna(Map):
    def __init__(self):
        super().__init__()
        '''
        version:list=[] #record the name of the beatmap
        music:list=[]   #record music paths
        bpmlist:list=[] #record the bpm
        maplist:list=[] #record the beatmap path
        title:str=""    #record the beatmap title
        root:str=""
        '''
        self.info:list=[]   #record the beatmap information
        self.note:list=[]    #record the note info
        self.count:int=0
        for self.root, dirs, files in os.walk("./temp"):
            for file in files:
                if file.endswith(".sm"):
                    #obtain the file address
                    file_path=os.path.join(self.root,file)
                    self.parse_etterna_file(file_path)
                    for i in range(self.count):
                        self.maplist.append(file_path)
    def parse_etterna_file(self,file_path):
        self.data={}
        with open(file_path, 'r',encoding='utf-8') as f:
            self.count=self.get_info(f)
            f.seek(0)
            #从每一行开始读取信息
            for line in f:
                line = line.strip()
                #当行为空或者以"//"开头说明歌曲和谱面相关信息结束，后面是note信息
                if not line or line.startswith("//"):
                    break
                key=line[1:].split(":")
                value=key[1].replace(";","")
                #因为只需要修改音乐名和bpm，故只获取这两项
                if key[0]=="MUSIC":
                    for i in range(self.count):
                        self.music.append(os.path.join(self.root,value))
                if key[0]=="BPMS":
                    self.bpmlist.append(value.strip(","))
    def get_info(self,file):
        content=file.read()
        match=re.finditer(r'//---------------',content)
        pos:list=[]
        string:list=[]
        #因为一个.sm谱面文件中可能有同一首歌的不同谱面，所以要保存所有匹配的位置
        for m in match:
            pos.append(m.start())
        if pos.__len__()==1:
            string.append(content[pos[0]:])
        else:
            for i in range(pos.__len__()-1):
                string.append(content[pos[i]:pos[i+1]])
            string.append(content[pos[-1]:])
        #获取难度名(因为难度名在"//---------------"开始的第五行)
        for s in string:
            file_like_string = io.StringIO(s)
            for _ in range(4):  # 跳过前四行
                next(file_like_string)
            fifth_line = file_like_string.readline()  # 读取第五行
            self.version.append(fifth_line[:-2].strip())   
        for i in range(pos.__len__()): 
            self.info.append(content[:pos[0]])
        self.note.append(string) 
        return pos.__len__()  
    def change_info(self, select_map, speed_rate) -> None:
        #修改音频名
        replace_music_with_speed = partial(replace_music, music=os.path.basename(self.music[select_map]),speed=speed_rate)
        info:str = re.sub(r'#MUSIC:' + re.escape(os.path.basename(self.music[select_map])), 
                                       replace_music_with_speed, self.info[select_map])
        #修改offset
        multiply_with_offset = partial(multiply_offset, speed=speed_rate)
        info = re.sub(r'#OFFSET:(-?[\d\.]+)', multiply_with_offset, info)
        #修改BPM
        multiply_with_speed = partial(multiply_bpm, speed=speed_rate)
        info = re.sub(r'=([\d\.]+)', multiply_with_speed, info)
        #修改难度名
        i: int=0
        for i in range(100):
            if select_map>self.note[i].__len__():
                select_map=select_map-self.note[i].__len__()
            else:
                break
        note=re.sub(re.escape(self.version[select_map]),
                                        f'{self.version[select_map]} {speed_rate}x',self.note[i][select_map])
        #新建谱面(.sm)文件
        new_file_path = os.path.join(self.root, 
                                     os.path.splitext(os.path.basename(self.maplist[select_map]))[0]+f'x{speed_rate}.sm')
        #写入谱面信息
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(info)
            f.write(note)