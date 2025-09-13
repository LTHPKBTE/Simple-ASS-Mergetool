# Simple-ASS-Mergetool
一个简单的从ai要来的ASS文件合并脚本。

它只会生硬的将文件合并在一起，不处理重合或出错部分。  
这是预期行为，因为我最初的使用目的是将字幕组的字幕文件和弹幕文件合并来看番。如有双语字幕需求您可能无法使用这个工具达成。

脚本假设以第一个ass文件头为基准，两个文件可以正常显示字幕。目前没有做进一步处理的打算。

用法：

``` Bash
格式: python <脚本名> <文件1> <文件2> [可选的输出文件名]
python merge.py "字幕 A.ass" "字幕 B.ass" -o "合并后的字幕.ass"

如果不提供-o参数，将使用默认输出名 "merged.ass"
python merge.py file1.ass file2.ass

查看帮助信息
python merge.py -h
```

# License
licensed under `The Unlicense` .
