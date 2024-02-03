# A Simple BeatMap SpeedChanger

simplely use sox,ffmpeg,json to edit



# Contens

- [A Simple BeatMap SpeedChanger](#a-simple-beatmap-speedchanger)
- [Contens](#contens)
  - [ScreenShots](#screenshots)
  - [Tips](#tips)
  - [Update](#update)

## ScreenShots
- 在终端中运行,每次可自由多倍速，先选择谱面格式
  
  ![Alt text](image-4.png)
  ![Alt text](image.png)
- 简单调用 sox实现变速
  ![Alt text](image-1.png)
- 会暂时创建 temp 目录并解包到此目录，最后生成 mcz 文件后删除

  ![Alt text](image-2.png)

- 最后导入到 malody/osu 就行啦ヾ(≧▽≦\*)o
  ![Alt text](image-3.png)
  ![Alt text](image-5.jpg)

## Tips
- 使用前请先安装SoX，可以在[sourceforge](https://sourceforge.net/projects/sox/files/sox/)下载并添加到path,[ffmpeg](https://ffmpeg.org/download.html)也是需要的
- 加速会升高音调，减速不会改变音调
- 因为只是复习累了所以随便写的，所以异常处理全都没写
- bug 懒得测了，随便吧
- 以后有可能会支持更多格式的谱面(?咕咕咕)
## Update

- 2024/1/31:使用sox替代了ffmpeg实现变速，之前变调有问题
- 2024/2/3:因为sox默认不支持mp3，所以使用ffmpeg转码，增加了对.osu谱面的支持，下一步应该是etterna🤤
