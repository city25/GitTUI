from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


class File:
    def __init__(self):
        pass

    def main(self):
        choices = [
            "New Repository",
            "Add local Repository",
            "Clone repository",
            "Options",
            "Exit",
        ]

        kb = KeyBindings()
        index = {'i': 0}

        @kb.add('up')
        def _(event):
            index['i'] = (index['i'] - 1) % len(choices)
            event.app.invalidate()

        @kb.add('down')
        def _(event):
            index['i'] = (index['i'] + 1) % len(choices)
            event.app.invalidate()

        @kb.add('enter')
        def _(event):
            event.app.exit()

        # 样式：仅设置选中文字的前景色为艳绿色
        style = Style.from_dict({
            'selected': '#00ff00',
        })

        def get_text():
            title = "File"
            # 计算内容区域最大宽度
            max_choice_len = max(len(c) for c in choices)
            # 菜单项内容宽度 = 前缀("► "或"  ") + 最长选项文本
            menu_content_width = max_choice_len + 2
            
            # 内部宽度 = 标题或菜单项内容的最大值 + 内边距
            inner_width = max(len(title), menu_content_width) + 2
            
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
                arrow = '►' if i == index['i'] else ' '
                # 格式化菜单行内容：前缀 + 选项文本 + 填充
                line_content = f"{arrow} {choice:<{max_choice_len}}"
                # 填充至内部宽度
                padded_content = f"{line_content:<{inner_width}}"
                full_line = f"|{padded_content}|\n"
                
                # 为选中行应用艳绿色样式
                if i == index['i']:
                    fragments.append(('class:selected', full_line))
                else:
                    fragments.append(('', full_line))
            
            # 下边框
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            return fragments

        control = FormattedTextControl(get_text, focusable=True)
        # 窗口高度 = 菜单项数 + 4(上边框、标题、分隔线、下边框)
        window_height = len(choices) + 4
        win = Window(content=control, height=window_height)
        
        app = Application(layout=Layout(win), full_screen=False, 
                         key_bindings=kb, style=style, mouse_support=False)
        app.run()
        
        return choices[index['i']]


# 测试入口
if __name__ == "__main__":
    file_menu = File()
    result = file_menu.main()
    print(f"\n您选择了: {result}")
    
    # 根据选择结果动态导入对应模块（文件名与类名相同）
    if result == "New Repository":
        try:
            from NewRepository import NewRepository
            # 实例化并调用主方法
            NewRepository().run_interactive_flow()
        except ImportError:
            print("NewRepository 模块未找到，无法创建新仓库。")
        except AttributeError as e:
            print(f"NewRepository 类中未找到所需方法: {e}")
            
    elif result == "Add local Repository":
        try:
            from AddLocalRepository import AddLocalRepository
            # 实例化并调用主方法
            AddLocalRepository().local_path()
        except ImportError:
            print("AddLocalRepository 模块未找到，无法添加本地仓库。")
        except AttributeError as e:
            print(f"AddLocalRepository 类中未找到所需方法: {e}")
            
    elif result == "Clone repository":
        try:
            from CloneRepository import CloneRepository
            CloneRepository().clone_flow()
        except ImportError:
            print("CloneRepository 模块未找到，无法克隆仓库。")
        except AttributeError as e:
            print(f"CloneRepository 类中未找到所需方法: {e}")
            
    elif result == "Options":
        try:
            from Options import Options
            Options().show_settings()
        except ImportError:
            print("Options 模块未找到，无法打开设置。")
        except AttributeError as e:
            print(f"Options 类中未找到所需方法: {e}")