# Simple-ASS-Mergetool
一个简单的从ai要来的ASS文件合并脚本。

用法：

``` Bash
格式: python <脚本名> <文件1> <文件2> [可选的输出文件名]
python merge_ass_v3.py "字幕 A.ass" "字幕 B.ass" -o "合并后的字幕.ass"

如果不提供-o参数，将使用默认输出名 "merged.ass"
python merge_ass_v3.py file1.ass file2.ass

查看帮助信息
python merge_ass_v3.py -h
```

# License
licensed under `The Unlicense` .
