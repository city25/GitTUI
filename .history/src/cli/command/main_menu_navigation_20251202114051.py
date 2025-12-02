import importlib
import sys
import os
from typing import Optional, List

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


class MainMenuNavigation:
    def __init__(self):
        self.kb = KeyBindings()
        self.choice_index = 0

    def main(self):
        choices = [
            "File",
            "Edit",
            "View",
            "Repository",
            "Branch",
            "Help",
        ]

        @self.kb.add('up')
        def _(event):
            self.choice_index = (self.choice_index - 1) % len(choices)
            event.app.invalidate()

        @self.kb.add('down')
        def _(event):
            self.choice_index = (self.choice_index + 1) % len(choices)
            event.app.invalidate()

        @self.kb.add('enter')
        def _(event):
            event.app.exit()

        # 样式：只设置前景色（艳绿色），无背景色
        style = Style.from_dict({
            'selected': '#00ff00',
        })

        def get_choice_text():
            title = "File"
            # 计算内容区域最大宽度
            max_choice_len = max(len(c) for c in choices)
            # 菜单项内容宽度 = 前缀("► "或"  ") + 最长选项文本
            menu_content_width = max_choice_len + 2
            
            # 内部宽度 = 标题或菜单项内容的最大值
            inner_width = max(len(title), menu_content_width) + 2  # +2 为内边距
            
            # 构建边框和内容的各个片段
            fragments = []
            
            # 上边框
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            # 标题行（居中）
            fragments.append(('', f"|{title:^{inner_width}}|\n"))
            
            # 分隔线
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            # 菜单项
            for i, choice in enumerate(choices):
                arrow = '►' if i == self.choice_index else ' '
                # 格式化菜单行内容：前缀 + 选项文本 + 填充
                line_content = f"{arrow} {choice:<{max_choice_len}}"
                # 填充至内部宽度
                padded_content = f"{line_content:<{inner_width}}"
                full_line = f"|{padded_content}|\n"
                
                # 为选中行应用艳绿色样式
                if i == self.choice_index:
                    fragments.append(('class:selected', full_line))
                else:
                    fragments.append(('', full_line))
            
            # 下边框
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            return fragments

        choice_control = FormattedTextControl(get_choice_text)
        # 窗口高度 = 菜单项数 + 4(上边框、标题、分隔线、下边框)
        window_height = len(choices) + 4
        
        choice_window = Window(content=choice_control, height=window_height)
        layout = Layout(container=choice_window)
        
        app = Application(layout=layout, full_screen=False, key_bindings=self.kb, style=style)
        app.run()
        
        return choices[self.choice_index] if self.choice_index < len(choices) else "Invalid choice"


def setup_project_path():
    """自动设置项目根目录到Python路径"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        search_dir = current_dir
        added = False

        for _ in range(6):
            candidate_src = os.path.join(search_dir, 'src')
            candidate_pkg = os.path.join(search_dir, 'git_dit')

            if os.path.isdir(candidate_src) and os.path.isdir(os.path.join(candidate_src, 'git_dit')):
                if candidate_src not in sys.path:
                    sys.path.insert(0, candidate_src)
                    print(f"调试: 已添加包路径 {candidate_src} 到 sys.path")
                added = True
                break
            if os.path.isdir(candidate_pkg):
                parent = search_dir
                if parent not in sys.path:
                    sys.path.insert(0, parent)
                    print(f"调试: 已添加包路径 {parent} 到 sys.path")
                added = True
                break

            parent_dir = os.path.abspath(os.path.join(search_dir, '..'))
            if parent_dir == search_dir:
                break
            search_dir = parent_dir

        if not added:
            project_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
                print(f"调试: 未找到标准包位置，已添加项目根目录 {project_root} 到 sys.path（兜底）")

        return True
    except Exception as e:
        print(f"警告: 设置路径失败: {e}")
        return False


# # 独立运行测试入口
# if __name__ == "__main__":
#     navigation = MainMenuNavigation()
#     result = navigation.main()
    
#     print(f"\n您选择了: {result}")

#     # 尝试动态导入相应模块
#     try:
#         # 将菜单项名称转换为可能的模块名
#         module_name = result.split()[0] if ' ' in result else result
#         imported_module = importlib.import_module(module_name)
#         print(f"成功导入 {module_name} 模块")
#         # 正确导入并调用
#         from file.file import File
#         file = File()
#         file.main()
#     except ImportError as e:
#         print(f"警告: 未找到 {module_name} 模块: {e}")

# 独立运行测试入口
# if __name__ == "__main__":
#     setup_project_path()  # 设置项目路径
#     navigation = MainMenuNavigation()
#     result = navigation.main()
    
#     print(f"\n您选择了: {result}")

#     # 尝试动态导入相应模块
#     try:
#         # 将菜单项名称转换为可能的模块名
#         module_name = result.split()[0] if ' ' in result else result
#         if module_name == "File":
#             # 使用相对导入路径
#             from .file.file import File
#             print(f"成功导入 File 模块")
#             # 正确导入并调用
#             file = File()
#             file.main()
#         else:
#             imported_module = importlib.import_module(module_name)
#             print(f"成功导入 {module_name} 模块")
#     except ImportError as e:
#         print(f"警告: 未找到 {module_name} 模块: {e}")
#     except Exception as e:
#         print(f"执行 {module_name} 时出错: {e}")

if __name__ == "__main__":
    # setup_project_path()  # 设置项目路径
    navigation = MainMenuNavigation()
    result = navigation.main()
    
    print(f"\n您选择了: {result}")

    # # 尝试动态导入相应模块
    # try:
    #     # 将菜单项名称转换为可能的模块名
    #     module_name = result.split()[0] if ' ' in result else result
    #     if module_name == "File":
    #         # 使用相对导入路径
    #         from .file.file import File
    #         print(f"成功导入 File 模块")
    #         # 正确导入并调用
    #         file = File()
    #         file.main()
    #     else:
    #         imported_module = importlib.import_module(module_name)
    #         print(f"成功导入 {module_name} 模块")
    # except ImportError as e:
    #     print(f"警告: 未找到 {module_name} 模块: {e}")
    # except Exception as e:
    #     print(f"执行 {module_name} 时出错: {e}")

    try:
        import file.file
        module_name = file.file.File().main()
    except Exception as e:
        print(f"执行 {module_name} 时出错: {e}")

    """仅仅尝试导入并调用 File 模块"""
    """尝试使用 if 语句调用所有模块"""