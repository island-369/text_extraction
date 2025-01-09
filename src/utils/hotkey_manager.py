from keyboard import add_hotkey, remove_hotkey

class HotkeyManager:
    @staticmethod
    def register_hotkey(key_combination, callback):
        """注册全局快捷键"""
        try:
            add_hotkey(key_combination, callback)
            return True
        except Exception as e:
            print(f"注册快捷键失败: {str(e)}")
            return False

    @staticmethod
    def unregister_hotkey(key_combination):
        """注销全局快捷键"""
        try:
            remove_hotkey(key_combination)
            return True
        except Exception as e:
            print(f"注销快捷键失败: {str(e)}")
            return False 