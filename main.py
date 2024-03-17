import Module.malody as malody,Module.osu as osu,Module.etterna as etterna
from Module.map import unzip_file,judge_maptype
def run(maptype,map_path):
    if maptype=="osu":
        game=osu.Osu(map_path)
    if maptype=="malody":
        game=malody.Malody(map_path)
    if maptype=="etterna":
        game=etterna.Etterna(map_path)
    game.run(maptype)
if __name__ == "__main__":
    map_path=input("Please input FilePath(eg：d:/malody/export/Grief & Malice.mcz)：\n")
    map_path=map_path.strip('"')
    unzip_file(map_path,"./temp")
    maptype=judge_maptype()
    run(maptype,map_path)


