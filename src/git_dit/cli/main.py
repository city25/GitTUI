import subprocess


def get_git_version():
    try:
        result = subprocess.run(
            ["git", "version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        version_output = result.stdout.strip()
        version = version_output.replace("git version ", "")
        version_parts = version.split('.')
        if len(version_parts) >= 3:
            return '.'.join(version_parts[:3])
        return version
    except Exception:
        return "unknown"

version = get_git_version()

print("+---------------------------------------------+")
print("|             Git-DIT Terminal UI             |")
print("| A simple and powerful ASCII-based Git client|")
print("| for your terminal environment.              |")
print(f"| Git Version: {version}                         |")
print("| Press [ENTER] to begin...                   |")
print("+---------------------------------------------+")

users_input = input()  # 等待用户按下回车键

if users_input == "":
    print("Starting Git-DIT...")
    print("Try to return Navigation Interface...")
    try:
        # 正确导入并调用
        from command.main_menu_navigation import MainMenuNavigation
        menu = MainMenuNavigation()
        menu.main()
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
