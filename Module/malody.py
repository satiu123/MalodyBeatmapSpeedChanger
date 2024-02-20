from Module.map import Map
import os,json
class Malody(Map):
    def __init__(self) -> None:
        super().__init__()
        #traverse the temp directory
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
                if file.endswith(".mc"):
                    #obtain the file address
                    file_path=os.path.join(self.root,file)
                    self.maplist.append(file_path)
                    self.get_info(file_path)
    def get_info(self,file_path) -> None:
        with open(file_path,encoding='utf-8') as f:
            mc = json.load(f)
            self.version.append(mc["meta"]["version"])
            for note in reversed(mc["note"]):
                if note.get("sound") != None:
                    self.music.append(os.path.join(self.root,note["sound"]))
            for time in mc["time"]:
                if time.get("bpm") != None:
                    self.bpmlist.append(time["bpm"])
    def change_info(self,selected_map,speed_rate) -> None:
        with open(self.maplist[selected_map],encoding='utf-8') as f:
            mc = json.load(f)
            mc["meta"]["version"]=mc["meta"]["version"]+"x"+str(speed_rate)
            for note in reversed(mc["note"]):
                if note.get("sound") != None:
                    note["sound"]=note["sound"].replace(self.get_split(selected_map,1),f"x{speed_rate}{self.get_split(selected_map,1)}")
            for time in mc["time"]:
                if time.get("bpm") != None:
                    time["bpm"]=time["bpm"]*speed_rate
        # create a new file
        new_file_path = os.path.join(self.root, os.path.splitext(os.path.basename(self.maplist[selected_map]))[0]+f'x{speed_rate}.mc')
        # write the modified json to a new file
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(mc, f, ensure_ascii=False)