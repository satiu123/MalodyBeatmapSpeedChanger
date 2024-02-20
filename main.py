import Module.malody as malody,Module.osu as osu,Module.etterna as etterna
if __name__ == "__main__":
    print("osu or malody or etterna? 1.osu 2.malody 3.etterna(.sm)")
    maptype = input("input choice(eg:1)：")
    if maptype=="1":
        oosu=osu.Osu()
        oosu.run("osu")
    elif maptype=="2":
        mmalody=malody.Malody()
        mmalody.run("malody")
    elif maptype=="3":
        eetterna=etterna.Etterna()
        eetterna.run("etterna")
    else:
        print("敬请期待（coming sooooooon）")
