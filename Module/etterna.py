from Module.map import Map
import os,re
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
        for self.root, dirs, files in os.walk("./temp"):
            for file in files:
                if file.endswith(".osu"):
                    #obtain the file address
                    file_path=os.path.join(self.root,file)
                    self.maplist.append(file_path)
                    self.get_info()
    def parse_etterna_file(self,file_path):
        self.data={}
        with open(file_path, 'r',encoding='utf-8') as f:
            self.get_version(f)
            for line in f:
                line = line.strip()
                key=line[1].split(":")
                value=key[1].replace(";","")
                if key[0]=="TITLE":
                    self.title=value
                if key[0]=="MUSIC":
                    self.music.append(os.path.join(value))
                if key[0]=="BPMS":
                    self.bpmlist.append(float(value))
    def get_version(self,file):
        content=file.read()
        match=re.findall(r'//---------------',content)
        for i in range(len(match)):
            file.seek(content.find(match[i]))
            self.version.append(file.readline().split(":")[1])
            
    def get_info(self)->None:
        with open(self.maplist[0], 'r',encoding='utf-8') as f:
            for line in f:
                if line.startswith("AudioFilename:"):
                    self.music.append(os.path.join(self.root,line.split(":")[1][1:]))
                if line.startswith("Version:"):
                    self.version.append(line.split(":")[1])
                if line.startswith("SliderMultiplier:"):
                    self.bpmlist.append(float(line.split(":")[1]))