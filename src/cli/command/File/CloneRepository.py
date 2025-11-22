from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


class CloneRepository:
    """克隆仓库的交互式界面类"""
    
    def __init__(self):
        """初始化克隆仓库类，设置默认值"""
        self.repository_url = ""
        self.clone_path = ""

    def clone(self) -> str:
        """
        显示克隆配置对话框，允许用户输入URL和路径
        
        +---------------------------------------------+
        |           Clone a Git Repository            |
        +---------------------------------------------+
        | URL: https://github.com/user/repo.git      |
        | path: /home/user/projects/                 |
        |             clone        cancel             |
        +---------------------------------------------+
        
        导航方式：
        - Tab/Shift+Tab: 在输入框和按钮间切换
        - 左/右箭头: 在按钮间切换
        - Enter: 确认当前按钮（仅按钮区域）
        - 普通字符: 在当前输入框中输入
        - Backspace: 删除当前输入框最后一个字符
        
        Returns:
            "clone" 或 "cancel"
        """
        kb = KeyBindings()
        
        # 焦点状态: 0=URL输入, 1=Path输入, 2=clone按钮, 3=cancel按钮
        focus_state = [0]
        
        # 输入内容（使用列表以便在闭包中修改）
        url_text = [""]
        path_text = [""]
        
        # 按钮
        buttons = ["clone", "cancel"]
        selected_button = [0]

        @kb.add('tab')
        def _(event):
            """Tab键切换到下一个字段"""
            focus_state[0] = (focus_state[0] + 1) % 4
            event.app.invalidate()

        @kb.add('s-tab')  # Shift+Tab
        def _(event):
            """Shift+Tab切换到上一个字段"""
            focus_state[0] = (focus_state[0] - 1) % 4
            event.app.invalidate()

        @kb.add('left')
        def _(event):
            """左箭头仅在按钮区域有效"""
            if focus_state[0] in [2, 3]:
                selected_button[0] = (selected_button[0] - 1) % len(buttons)
                event.app.invalidate()

        @kb.add('right')
        def _(event):
            """右箭头仅在按钮区域有效"""
            if focus_state[0] in [2, 3]:
                selected_button[0] = (selected_button[0] + 1) % len(buttons)
                event.app.invalidate()

        @kb.add('enter')
        def _(event):
            """回车键仅在按钮区域触发操作"""
            if focus_state[0] in [2, 3]:
                event.app.exit(result=buttons[selected_button[0]])

        @kb.add('backspace')
        def _(event):
            """退格键删除字符"""
            if focus_state[0] == 0:
                url_text[0] = url_text[0][:-1]
                event.app.invalidate()
            elif focus_state[0] == 1:
                path_text[0] = path_text[0][:-1]
                event.app.invalidate()

        # 处理普通字符输入
        @kb.add('<any>')
        def on_any_key(event):
            """处理任意可打印字符"""
            key = event.key_sequence[0].key
            
            # 只处理可打印字符（非控制键）
            if len(key) == 1 and key.isprintable():
                if focus_state[0] == 0:  # URL输入框
                    url_text[0] += key
                    event.app.invalidate()
                elif focus_state[0] == 1:  # Path输入框
                    path_text[0] += key
                    event.app.invalidate()

        # 样式定义（正确使用class:前缀）
        style = Style.from_dict({
            'selected': '#00ff00',      # 选中按钮的艳绿色
            'focus': 'underline',       # 聚焦输入框的下划线
        })

        def get_text():
            title = "Clone a Git Repository"
            
            # 获取当前输入值
            current_url = url_text[0]
            current_path = path_text[0]
            
            # 计算各行内容长度
            url_line = f" URL: {current_url}"
            path_line = f" path: {current_path}"
            button_line = f" {buttons[0]}    {buttons[1]} "
            
            # 确定内部宽度
            max_content_len = max(len(title), len(url_line), len(path_line), len(button_line))
            inner_width = max_content_len
            
            fragments = []
            
            # 上边框
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            # 标题
            fragments.append(('', f"|{title:^{inner_width}}|\n"))
            
            # 分隔线
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            # URL输入行 (使用class:focus样式)
            url_style = 'class:focus' if focus_state[0] == 0 else ''
            fragments.append((url_style, f"|{url_line:<{inner_width}}|\n"))
            
            # Path输入行 (使用class:focus样式)
            path_style = 'class:focus' if focus_state[0] == 1 else ''
            fragments.append((path_style, f"|{path_line:<{inner_width}}|\n"))
            
            # 按钮行
            fragments.append(('', "| "))
            
            # clone按钮
            clone_style = 'class:selected' if focus_state[0] in [2, 3] and selected_button[0] == 0 else ''
            fragments.append((clone_style, buttons[0]))
            
            # 间隙
            gap_len = inner_width - len(buttons[0]) - len(buttons[1]) - 4
            gap_len = max(gap_len, 4)
            fragments.append(('', f"{' ' * gap_len} "))
            
            # cancel按钮
            cancel_style = 'class:selected' if focus_state[0] in [2, 3] and selected_button[0] == 1 else ''
            fragments.append((cancel_style, buttons[1]))
            
            fragments.append(('', " |\n"))
            
            # 下边框
            fragments.append(('', f"+{'-' * inner_width}+\n"))
            
            return fragments

        control = FormattedTextControl(get_text)
        window_height = 7  # 上边框 + 标题 + 分隔线 + URL + Path + 按钮 + 下边框
        
        app = Application(
            layout=Layout(Window(content=control, height=window_height)), 
            full_screen=False, 
            key_bindings=kb, 
            style=style
        )
        
        result = app.run()
        
        # 将输入的值赋回实例属性
        self.repository_url = url_text[0]
        self.clone_path = path_text[0]
        
        return result

    def get_repository_info(self) -> tuple[str, str]:
        """
        获取用户输入的仓库信息和克隆路径
        
        Returns:
            tuple: (repository_url, clone_path)
        """
        return self.repository_url, self.clone_path


# 测试入口
if __name__ == "__main__":
    cloner = CloneRepository()
    action = cloner.clone()
    
    url, path = cloner.get_repository_info()
    print(f"\n您选择了: {action}")
    print(f"仓库URL: {url}")
    print(f"克隆路径: {path}")
    
    if action == "clone":
        print(f"开始克隆仓库: {url} 到 {path if path else '当前目录'}")
        # 添加实际的 git clone 逻辑
        # import subprocess
        # target_path = path if path else "."
        # subprocess.run(["git", "clone", url, target_path])










# 有问题
# 用户填写URL的时候无法回车转到填Path
