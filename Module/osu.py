from Module.map import Map
import os,copy
class Osu(Map):
    def __init__(self) -> None:
        super().__init__()
        '''
        version:list=[] #record the name of the beatmap
        music:list=[]   #record music paths
        bpmlist:list=[] #record the bpm
        maplist:list=[] #record the beatmap path
        title:str=""    #record the beatmap title
        root:str=""
        '''
        self.all_map:list = []
        self.data:dict={} #record the data of the osubeatmap
        #traverse the temp directory
        for self.root, dirs, files in os.walk("./temp"):
            for file in files:
                if file.endswith(".osu"):
                    #obtain the file address
                    file_path=os.path.join(self.root,file)
                    self.maplist.append(file_path)
                    self.parse_osu_file(file_path)
                    self.title=self.all_map[0]["Metadata"][0].split(":")[1]
                    self.get_info()
    def parse_osu_file(self,file_path):
        current_section = None
        self.data={}
        with open(file_path, 'r',encoding='utf-8') as f:
            self.data["Head"]=f.readline()
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    self.data[current_section] = []
                elif current_section is not None:
                    self.data[current_section].append(line)
        self.all_map.append(self.data)
    def get_info(self):
        self.music.append(os.path.join(self.root,self.data["General"][0].split(":")[1][1:]))
        self.version.append(self.data["Metadata"][5].split(":")[1])
        self.bpmlist.append(float(self.data["TimingPoints"][0].split(",")[1]))
    def change_info(self, select_map, speed_rate) -> None:
        self.data=copy.deepcopy(self.all_map[select_map])
        self.data["Metadata"][5]+=f"x{speed_rate}"
        self.data["General"][0]=f"AudioFilename:{os.path.basename(self.music[select_map]).replace(self.get_split(select_map,1),f'x{speed_rate}{self.get_split(select_map,1)}')}"
        self.data["TimingPoints"][0]=f"{0},{self.bpmlist[select_map]/speed_rate},4,1,0,100,1,0"
        for i in range(len(self.data["HitObjects"])):
            beat_time = self.data["HitObjects"][i].split(",")
            beat_time[2] = str(int(int(beat_time[2])/speed_rate))
            if beat_time[3]=="128":
                part=beat_time[5].split(":")
                beat_time[5]=f"{str(int(int(part[0])/speed_rate))}:{':'.join(part[1:])}:"
            self.data["HitObjects"][i] = ",".join(beat_time)

        # create a new file
        new_file_path = os.path.join(self.root, os.path.splitext(os.path.basename(self.maplist[select_map]))[0]+f'x{speed_rate}.osu')
        # write the modified json to a new file
        with open(new_file_path, 'w', encoding='utf-8') as f:
            for section in self.data:
                if section=="Head":
                    f.write(f"{self.data[section]}\n")
                    continue
                f.write(f"[{section}]\n")
                for line in self.data[section]:
                    f.write(f"{line}\n")
                f.write("\n")
        self.maplist.append(new_file_path)        