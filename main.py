import Module.malody as malody,Module.osu as osu
if __name__ == "__main__":
    print("osu or malody? 1.osu 2.malody")
    maptype = input("input choice(eg:1)：")
    if maptype=="1":
        oosu=osu.Osu()
        oosu.run("osu")
    elif maptype=="2":
        mmalody=malody.Malody()
        mmalody.run("malody")
    else:
        print("敬请期待（coming sooooooon）")

