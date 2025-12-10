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

    def main(self, simulate_keys: Optional[List[str]] = None):
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
        
        # 支持在非交互环境下传入模拟按键（用于测试/脚本）
        if simulate_keys is not None:
            # 延迟导入以避免在不需要时引入额外依赖
            from prompt_toolkit.input.defaults import create_pipe_input
            from prompt_toolkit.output import DummyOutput

            # create_pipe_input() 返回一个 context manager，使用 with 以保证正确关闭
            with create_pipe_input() as pipe_input:
                app = Application(
                    layout=layout,
                    full_screen=False,
                    key_bindings=self.kb,
                    style=style,
                    input=pipe_input,
                    output=DummyOutput(),
                )

                # 将所有模拟按键写入 pipe_input（按需发送转义序列或回车）
                for k in simulate_keys:
                    pipe_input.send_text(k)

                app.run()
        else:
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
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate', '-s', nargs='*', help='Simulate key inputs, e.g. "\\x1b[B" "\\r"')
    args = parser.parse_args()

    # setup_project_path()  # 设置项目路径（按需启用）
    navigation = MainMenuNavigation()
    result = navigation.main(simulate_keys=args.simulate if args.simulate else None)

    print(f"\n您选择了: {result}")

    try:
        if result == "File":
            try:
                from file.file import File
            except Exception:
                try:
                    from .file.file import File
                except Exception:
                    File = None

            if File is None:
                print("无法导入 file 菜单模块。")
            else:
                sub_result = File().main()
                print(f"\nFile 菜单返回: {sub_result}")

                if sub_result == "New Repository":
                    try:
                        try:
                            from file.file_module import new_repository
                        except Exception:
                            from .file.file_module import new_repository
                        output = new_repository.run_interactive_flow()
                        print(output)
                    except Exception as e:
                        print(f"调用 new_repository 失败: {e}")
        else:
            print("未实现的主菜单分支（跳转待实现）")
    except Exception as e:
        print(f"执行 导入时出错: {e}")
