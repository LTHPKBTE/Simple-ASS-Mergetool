# merge_ass_v3.py

import os
import sys
import argparse # 导入argparse模块

def parse_ass_file(file_path):
    """
    解析ASS文件，并将其内容按部分（如 [Script Info]）分离开。
    """
    sections = {}
    current_section_name = None
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith('[') and stripped_line.endswith(']'):
                    current_section_name = stripped_line
                    sections[current_section_name] = [line]
                elif current_section_name:
                    sections[current_section_name].append(line)
    except FileNotFoundError:
        print(f"错误: 文件未找到 '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件 '{file_path}' 时发生错误: {e}")
        sys.exit(1)
        
    return sections

def merge_ass_files(file1_path, file2_path, output_path):
    """
    合并两个ASS文件，使用文件1的头部，合并样式（处理冲突）和事件。
    """
    # 检查输入文件是否存在
    if not os.path.exists(file1_path):
        print(f"错误: 输入文件 '{file1_path}' 不存在。")
        return
    if not os.path.exists(file2_path):
        print(f"错误: 输入文件 '{file2_path}' 不存在。")
        return

    print("开始解析文件...")
    ass1_sections = parse_ass_file(file1_path)
    ass2_sections = parse_ass_file(file2_path)
    
    # ... [此处省略与上一版本完全相同的合并逻辑代码] ...
    # 为了简洁，此处省略了样式和事件合并的详细代码，它们保持不变。
    # 实际使用时请将上一版本中的这部分代码复制到这里。
    # --- 1. 合并样式 [V4+ Styles] ---
    print("正在合并样式...")
    if '[V4+ Styles]' not in ass1_sections or '[Events]' not in ass1_sections or '[V4+ Styles]' not in ass2_sections or '[Events]' not in ass2_sections:
        print("错误: 一个或多个输入文件缺少 '[V4+ Styles]' 或 '[Events]' 部分。")
        return
    styles1_definitions = [line for line in ass1_sections['[V4+ Styles]'] if line.strip().startswith('Style:')]
    styles1_names = set(line.split(':', 1)[1].split(',')[0].strip() for line in styles1_definitions)
    styles2_definitions = [line for line in ass2_sections['[V4+ Styles]'] if line.strip().startswith('Style:')]
    style_rename_map = {}
    final_styles2_definitions = []
    for style_line in styles2_definitions:
        original_name = style_line.split(':', 1)[1].split(',')[0].strip()
        if original_name in styles1_names:
            new_name = original_name
            suffix = 2
            while f"{original_name}_{suffix}" in styles1_names: suffix += 1
            new_name = f"{original_name}_{suffix}"
            style_rename_map[original_name] = new_name
            print(f"样式冲突: '{original_name}' 已重命名为 '{new_name}'")
            style_data_parts = style_line.split(':', 1)[1].split(',')
            style_data_parts[0] = f" {new_name}"
            final_styles2_definitions.append(f"Style:{','.join(style_data_parts)}")
        else:
            final_styles2_definitions.append(style_line)
    # --- 2. 合并事件 [Events] ---
    print("正在合并事件...")
    events_format_line = next((line for line in ass1_sections['[Events]'] if line.strip().startswith('Format:')), None)
    format_fields = [field.strip() for field in events_format_line.split(':', 1)[1].split(',')]
    style_index = format_fields.index('Style')
    events1_lines = [line for line in ass1_sections['[Events]'] if line.strip().startswith(('Dialogue:', 'Comment:'))]
    events2_lines_raw = [line for line in ass2_sections['[Events]'] if line.strip().startswith(('Dialogue:', 'Comment:'))]
    updated_events2_lines = []
    for event_line in events2_lines_raw:
        line_type, data = event_line.split(':', 1)
        data_parts = data.split(',', len(format_fields) - 1)
        event_style = data_parts[style_index].strip()
        if event_style in style_rename_map:
            data_parts[style_index] = style_rename_map[event_style]
            updated_events2_lines.append(f"{line_type}:{','.join(data_parts)}")
        else:
            updated_events2_lines.append(event_line)
    # --- 3. 写入输出文件 ---

    print(f"正在写入合并文件到 '{output_path}'...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if '[Script Info]' in ass1_sections:
                f.writelines(ass1_sections['[Script Info]'])
                f.write('\n')
            styles_header_and_format = [line for line in ass1_sections['[V4+ Styles]'] if not line.strip().startswith('Style:')]
            f.writelines(styles_header_and_format)
            f.writelines(styles1_definitions)
            f.writelines(final_styles2_definitions)
            f.write('\n')
            events_header_and_format = [line for line in ass1_sections['[Events]'] if not line.strip().startswith(('Dialogue:', 'Comment:'))]
            f.writelines(events_header_and_format)
            f.writelines(events1_lines)
            f.writelines(updated_events2_lines)
        print(f"成功合并！输出文件: '{output_path}'")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 创建解析器
    parser = argparse.ArgumentParser(
        description="合并两个ASS字幕文件。保留文件1的头部和样式，并追加文件2的样式和事件。自动处理样式名冲突。",
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助信息格式
    )

    # 2. 添加参数
    parser.add_argument("file1", help="第一个ASS字幕文件 (作为基准的文件)")
    parser.add_argument("file2", help="第二个ASS字幕文件 (要追加内容的文件)")
    parser.add_argument(
        "-o", "--output", 
        default="merged.ass", 
        help="指定输出文件名 (可选, 默认是 'merged.ass')"
    )

    # 3. 解析参数
    args = parser.parse_args()

    # 4. 调用主函数
    merge_ass_files(args.file1, args.file2, args.output)