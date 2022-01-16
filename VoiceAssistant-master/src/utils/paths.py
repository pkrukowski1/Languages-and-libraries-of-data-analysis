def get_root_dir():
    from pathlib import Path
    return Path(__file__).absolute().parent.parent.parent

def get_test_path():
    from os import path
    return path.join(get_root_dir(), "test")

def get_log_path():
    from os import path
    return path.join(get_root_dir(), "logs")

if __name__=="__main__":
    print(get_log_path())