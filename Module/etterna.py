from Module.map import Map
from functools import partial
import os,re,io,copy
def multiply_bpm(match,speed):
    number = float(match.group(1))
    return f"={number * speed}"  # 乘以speed参数
def change_offset(offset, speed):
    offset = float(offset)
    return f"{offset / speed}"  # 乘以speed参数
def change_music_name(music:str,speed:float):
    temp=music.strip().split(".")
    return f"{temp[0]}x{speed}.{temp[1]}"
def change_displaybpm(dbpms, speed: float):
    if dbpms == "*":
        pass
    else:
        dbpms = list(map(float, dbpms.split(":")))
        for i in range(len(dbpms)):
            dbpms[i] = dbpms[i] * speed
        result = "#DISPLAYBPM:"+":".join(list(map(str, dbpms)))+";"
    return result
class Etterna(Map):
    def __init__(self,map_path):
        super().__init__(map_path)
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
        data={}
        with open(file_path, 'r',encoding='utf-8') as f:
            self.count=self.get_info(f)
            f.seek(0)
            #从每一行开始读取信息
            for line in f:
                line = line.strip()
                #当行为空或者以"//"开头说明歌曲和谱面相关信息结束，后面是note信息
                if line.startswith("//") and not line.startswith("//-"):
                    continue
                if not line or line.startswith("//-"):
                    break
                key=line[1:].split(":")
                value=key[1].replace(";","")
                data['#'+key[0]]=value
                #因为只需要修改音乐名和bpm，故只获取这两项
                if key[0]=="MUSIC":
                    for i in range(self.count):
                        self.music.append(os.path.join(self.root,value))
                if key[0]=="BPMS":
                    self.bpmlist.append(value.strip(","))
        self.info.append(data)
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
        # for i in range(pos.__len__()): 
        #     self.info.append(content[:pos[0]])
        self.note.append(string) 
        return pos.__len__()  
    def change_info(self, select_map, speed_rate) -> None:
        #修改音频名
        info=copy.deepcopy(self.info[select_map])
        info['#MUSIC']=change_music_name(info['#MUSIC'],speed_rate)
        
        #修改offset
        info['#OFFSET']=change_offset(info['#OFFSET'],speed_rate)

        #修改BPM
        info['#BPMS']=re.sub(r'=([\d\.]+)', partial(multiply_bpm, speed=speed_rate), info['#BPMS'])
        
        #修改displaybpm
        if "#DISPLAYBPM" in info.keys():
            info['#DISPLAYBPM']=change_displaybpm(info['#DISPLAYBPM'],speed_rate)
        #修改难度名
        i: int=0
        for i in range(100):
            if select_map>self.note[i].__len__():
                select_map=select_map-self.note[i].__len__()
            else:
                break
        note=self.note[i][select_map].split("\n")
        len=f'{self.version[select_map]} {speed_rate}x:'.__len__()-2
        note[4]=f'{" "*len}{self.version[select_map]} {speed_rate}x:'
        #新建谱面(.sm)文件
        new_file_path = os.path.join(self.root, 
                                     os.path.splitext(os.path.basename(self.maplist[select_map]))[0]+f'x{speed_rate}.sm')
        #写入谱面信息
        with open(new_file_path, 'w', encoding='utf-8') as f:
            for key in info.keys():
                f.write(key+":"+info[key]+";\n")
            for n in note:
                f.write(n+'\n')
