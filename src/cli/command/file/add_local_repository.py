class AddLocalRepository:
    def __init__(self, local_path):
        self.local_repository = local_path  # 修复：改为小写+下划线
    
    def local_path(self):
        local_path = input("Local path: ") # 用户输入的是绝对路径
        
if __name__ == "__main__":
    repo = AddLocalRepository()
    repo.local_path()