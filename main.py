import os,zipfile,json,subprocess,sox
#unpacking
def unzip_file(zip_filepath, dest_path) -> None:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
#pack
def zip_dir(dirname, zipfilename) -> None:
    with zipfile.ZipFile(zipfilename, 'w') as zipf:
        for root, dirs, files in os.walk(dirname):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dirname))
def get_sample_rate(audio_file_path) -> int | None:
    cmd = f'ffprobe -v quiet -print_format json -show_streams'
    args = cmd.split()
    args.append(audio_file_path)
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_output = json.loads(ffprobe_output)
    for stream in ffprobe_output['streams']:
        if stream['codec_type'] == 'audio':
            return int(stream['sample_rate'])    
def change_speed_and_pitch(input_file, output_file,speed):
    print("processing:",input_file,"->",output_file,"speed:",speed,"...")
    # 创建一个 transformer 对象
    tfm = sox.Transformer()
    # 设置音频的速度和音调
    if speed<1:
        tfm.tempo(factor=speed)
    else:
        tfm.speed(factor=speed)
    # 应用 transformer 到音频文件
    tfm.build(input_file, output_file)
    print("done")
class map:
    version:list=[] #record the name of the beatmap
    music:list=[]   #record music paths
    bpmlist:list=[] #record the bpm
    maplist:list=[] #record the beatmap path
    title:str=""    #record the beatmap title
    root:str=""     #record the beatmap root
    
    def __init__(self) -> None:
        map_path=input("Please input FilePath(eg：d:/malody/export/Grief & Malice.mcz)：\n")
        unzip_file(map_path, "./temp")
        #traverse the temp directory
        for self.root, dirs, files in os.walk("./temp"):
            for file in files:
                if file.endswith(".mc"):
                    #obtain the file address
                    file_path=os.path.join(self.root,file)
                    self.maplist.append(file_path)
                    self.get_info(file_path)
    def get_info(self,file_path) -> None:
        with open(file_path,encoding='utf-8') as f:
            superHeroSquad = json.load(f)
            self.version.append(superHeroSquad["meta"]["version"])
            for note in superHeroSquad["note"]:
                if note.get("sound") != None:
                    self.music.append(os.path.join(self.root,note["sound"]))
            for time in superHeroSquad["time"]:
                if time.get("bpm") != None:
                    self.bpmlist.append(time["bpm"])
    def change_info(self,selected_map,speed_rate) -> None:
        with open(self.maplist[selected_map],encoding='utf-8') as f:
            superHeroSquad = json.load(f)
            self.title=superHeroSquad["meta"]["song"]["title"]
            superHeroSquad["meta"]["version"]=superHeroSquad["meta"]["version"]+"x"+str(speed_rate)
            for note in superHeroSquad["note"]:
                if note.get("sound") != None:
                    note["sound"]=note["sound"].replace(self.get_split(selected_map,1),f"x{rate}{self.get_split(selected_map,1)}")
            for time in superHeroSquad["time"]:
                if time.get("bpm") != None:
                    time["bpm"]=time["bpm"]*speed_rate
        # create a new file
        new_file_path = os.path.join(self.root, os.path.splitext(os.path.basename(self.maplist[selected_map]))[0]+f'x{speed_rate}.mc')
        # write the modified json to a new file
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(superHeroSquad, f, ensure_ascii=False)
    def get_split(self,selected_map,pos):
        return os.path.splitext(self.music[selected_map])[pos]
        
if __name__ == '__main__':
    maps=map()
    for mapp in maps.version:
        print(maps.version.index(mapp),":",mapp)
    selected_map=int(input("input choice(eg:0)：\n"))
    speed_rate = [float(rate) for rate in input("input Speed (eg:1.1 1.3 1.4)：\n").split()]
    for rate in speed_rate:
        change_speed_and_pitch(maps.music[selected_map],maps.music[selected_map].replace(maps.get_split(selected_map,1),f"x{rate}{maps.get_split(selected_map,1)}"),rate)
        maps.change_info(selected_map,rate)
    #packed into mcz
    zip_dir('temp', f'{maps.title}.mcz')
    os.system("rd /s/q temp")