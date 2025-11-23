import json
import subprocess
import os
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
# from prompt_toolkit.widgets import Label, TextArea, Checkbox, RadioList, Button
# from prompt_toolkit.layout.containers import HSplit, VSplit
# from prompt_toolkit.shortcuts import message_dialog


"""
+--------------------------------------------+
|               New Repository               |
+--------------------------------------------+
| 1. 仓库名称: [ ]                            |
| 2. 仓库描述: [ ]                            |
| 3. 本地路径: [ ]                            |
| 4. 初始化 README: [ ]                       |
| 5. .gitignore 模板: [ ]                     |
| 6. 许可证: [ ]                              |
+--------------------------------------------+
|      create                    cancel       |
+--------------------------------------------+
"""

def select_from_list(title: str, items: list) -> int:
    """交互式列表选择器，返回选中项的索引"""
    kb = KeyBindings()
    index = {'i': 0}

    @kb.add('up')
    def _(event):
        index['i'] = (index['i'] - 1) % len(items)
        event.app.invalidate()

    @kb.add('down')
    def _(event):
        index['i'] = (index['i'] + 1) % len(items)
        event.app.invalidate()

    @kb.add('enter')
    def _(event):
        event.app.exit()

    style = Style.from_dict({'selected': '#00ff00'})

    def get_text():
        fragments = [( '', title + '\n')]
        for i, it in enumerate(items):
            fragments.append(('class:selected' if i == index['i'] else '', f"{'►' if i == index['i'] else ' '} {it}\n"))
        return fragments

    control = FormattedTextControl(get_text)
    win = Window(content=control, height=len(items) + 1)
    app = Application(layout=Layout(win), key_bindings=kb, style=style, full_screen=False)
    app.run()
    return index['i']


def toggle_readme(title: str) -> bool:
    """交互式复选框，返回是否选中"""
    kb = KeyBindings()
    state = {'selected': False}

    @kb.add('space')
    def _(event):
        state['selected'] = not state['selected']
        event.app.invalidate()

    @kb.add('enter')
    def _(event):
        event.app.exit()

    style = Style.from_dict({'selected': '#00ff00'})

    def get_text():
        mark = '[X]' if state['selected'] else '[ ]'
        return [( 'class:selected' if state['selected'] else '', f"{mark} {title}\n"), ('', '\n(按空格切换，回车继续)')]

    control = FormattedTextControl(get_text)
    win = Window(content=control, height=3)
    app = Application(layout=Layout(win), key_bindings=kb, style=style, full_screen=False)
    app.run()
    return state['selected']


def left_right_choice(left: str, right: str) -> str:
    """左右选择对话框，返回选中的字符串"""
    kb = KeyBindings()
    state = {'i': 0}

    @kb.add('left')
    def _(event):
        state['i'] = 0
        event.app.invalidate()

    @kb.add('right')
    def _(event):
        state['i'] = 1
        event.app.invalidate()

    @kb.add('enter')
    def _(event):
        event.app.exit()

    style = Style.from_dict({'selected': '#00ff00'})

    def get_text():
        left_frag = ('class:selected' if state['i'] == 0 else '', f" {left} ")
        right_frag = ('class:selected' if state['i'] == 1 else '', f" {right} ")
        return [left_frag, ('', '   '), right_frag, ('', '\n\n(左右切换，回车确认)')]

    control = FormattedTextControl(get_text)
    win = Window(content=control, height=3)
    app = Application(layout=Layout(win), key_bindings=kb, style=style, full_screen=False)
    app.run()
    return left if state['i'] == 0 else right


def create_repository(name: str, description: str = '', local_path: str = '',
                     initialize_with_readme: bool = False, git_ignore: str | None = None,
                     license: str | None = None) -> bool:
    """创建仓库的核心功能：创建目录、git init、保存配置"""
    print('\n[NewRepository] 创建仓库：')
    print(f'  名称: {name}')
    print(f'  描述: {description}')
    print(f'  本地路径: {local_path}')
    print(f'  初始化 README: {initialize_with_readme}')
    print(f'  .gitignore 模板: {git_ignore}')
    print(f'  许可证: {license}')

    # 1. 创建本地目录
    try:
        os.makedirs(local_path, exist_ok=True)
        print(f"\n✅ 成功创建目录: {os.path.abspath(local_path)}")
    except Exception as e:
        print(f"\n❌ 创建目录失败: {e}")
        return False

    # 2. 执行 git init（相当于 cd xxx && git init）
    try:
        result = subprocess.run(
            ['git', 'init'],
            cwd=local_path,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Git 仓库初始化成功")
        if result.stdout:
            print(f"   {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git 初始化失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    except FileNotFoundError:
        print("\n❌ 错误: 未找到 git 命令，请确保 Git 已安装并添加到系统 PATH")
        return False

    # 3. 在当前目录创建 NewRepository.json
    try:
        repo_info = {
            "name": name,
            "description": description,
            "local_path": os.path.abspath(local_path),
            "initialize_with_readme": initialize_with_readme,
            "git_ignore": git_ignore,
            "license": license,
            "status": "created",
            "git_init_success": True
        }
        
        with open('NewRepository.json', 'w', encoding='utf-8') as f:
            json.dump(repo_info, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已创建 NewRepository.json 文件")
        print(f"   位置: {os.path.abspath('NewRepository.json')}")
    except Exception as e:
        print(f"\n❌ 创建 JSON 文件失败: {e}")
        return False

    return True


def run_interactive_flow() -> bool:
    """完整的交互式流程，收集信息并创建仓库"""
    # 验证仓库名称不能为空
    while True:
        name = prompt('repository name: ')
        if name.strip():
            break
        print("❌ 错误：仓库名称不能为空，请重新输入")

    description = prompt('description: ')
    
    # 验证本地路径不能为空且必须是绝对路径
    while True:
        local_path = prompt('local path: ')
        if local_path.strip():
            if os.path.isabs(local_path):
                break
            else:
                print(f"❌ 错误：必须使用绝对路径")
                print(f"   当前系统支持格式：{os.path.abspath('/example')}")
        else:
            print("❌ 错误：本地路径不能为空，请重新输入")

    readme_selected = toggle_readme('Initialize this repository with a README')

    git_ignore_list = [
        "None",
        "Actionscript", "Ada", "Agda", "Android", "AppEngine", "AppceleratorTitanium", "ArchLinux",
        "C", "C++", "CSharp", "Clojure", "CommonLisp",
        "Dart", "Delphi", "Drupal", "Eclipse",
        "Elisp", "Emacs", "Erlang", "Express",
        "Fortran",
        "Go",
        "Haskell",
        "Java", "JavaEE", "Joomla", "Julia",
        "Kotlin",
        "Lazarus", "Lua",
        "Magento", "Matlab",
        "Node",
        "Objective-C", "OCaml",
        "Perl", "PHP", "Python",
        "R", "Rails", "React", "Ruby", "Rust",
        "Sass", "Scala", "Swift", "Symfony",
        "TeX",
        "Vim", "VisualStudio", "Vue",
        "WordPress",
        "Xcode"
    ]

    gi_index = select_from_list('Select git ignore (回车确认):', git_ignore_list)
    git_ignore_choice = git_ignore_list[gi_index]

    license_list = ["None",
        "0BSD",
        "AGPL-3.0", "Apache-2.0", "Artistic-2.0",
        "BSD-2-Clause", "BSD-3-Clause", "BSL-1.0",
        "CC0-1.0", "CDDL-1.0",
        "EPL-2.0",
        "GPL-2.0", "GPL-3.0",
        "ISC",
        "LGPL-2.1", "LGPL-3.0",
        "MIT", "MPL-2.0",
        "OFPL", "OSL-3.0",
        "PostgreSQL", "Proprietary", "PSF", "Python-2.0",
        "Ruby",
        "Unlicense",
        "WTFPL",
        "Zlib",
        "openssl"
    ]

    lic_index = select_from_list('Select license (回车确认):', license_list)
    license_choice = license_list[lic_index]

    final = left_right_choice('create repository', 'cancel')
    if final == 'create repository':
        # 最终确认的路径也不能为空且必须是绝对路径
        while True:
            final_path = prompt('请确认创建路径: ')
            if final_path.strip():
                if os.path.isabs(final_path):
                    break
                else:
                    print(f"❌ 错误：必须使用绝对路径")
                    print(f"   当前系统支持格式：{os.path.abspath('/example')}")
            else:
                print("❌ 错误：创建路径不能为空，请重新输入")
            
        return create_repository(name, description, final_path, readme_selected, git_ignore_choice, license_choice)
    else:
        print('\nCancelled by user')
        return False


if __name__ == '__main__':
    success = run_interactive_flow()
    exit(0 if success else 1)