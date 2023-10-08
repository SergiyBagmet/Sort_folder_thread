import argparse
import concurrent.futures
from pathlib import Path
import time
from threading import Thread
from functools import wraps

from file_mover import FileMover
from rename import TextNormalizer 
from my_logger import MyLogger
logger = MyLogger("sort").get_logger()

"""
--source [-s] 
--output [-o] default folder = dist
--mode [-m] modification = category(default) or ext
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")
parser.add_argument("--mode", "-m", help="modification for sort ", default="category")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))
mode = args.get("mode")


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Execution time for {func.__name__}: {elapsed_time:.2f} seconds")
    return wrapper

def get_data_folder(path: Path, data=None) -> list[Path]:
        if data is None : data = []
        for item in path.iterdir():
            if item.is_file():
                data.append(item)
            elif item.is_dir():
                get_data_folder(item, data)
        return data

class PathModifier:
    
    EXT_FORM = {
            'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.PNG'],
            'video': ['.avi', '.mp4', '.mov', '.mkv'],
            'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
            'audio': ['.mp3', '.ogg', '.wav', '.amr'],
            'archives': ['.zip', '.gz', '.tar'],
        }
    
    def __init__(self, source: Path, target_dir: Path) -> None:
        self.source = source
        self.categoty = self.__get_category(source)
        self.target_dir = target_dir
        self.mode = mode
        
    def __get_category(self, path: Path) -> str:
        name_dir = ""
        for key, val in self.EXT_FORM.items():
            if path.suffix in val:
                name_dir = key
                break
        if not name_dir:  # если нет совпадений 
            name_dir = "others"
        return name_dir
    
    def get_mode_path(self, mode: str) -> Path:
        if self.categoty == 'archives':
            return self.target_dir / self.categoty / self.source.stem
        else:
            match mode:
                case 'category':  
                    return self.target_dir / self.categoty 
                case 'ext':
                    return self.target_dir / self.source.suffix[1:].upper() 
                case 'hard':
                    return self.target_dir / self.categoty / self.source.suffix[1:].upper() 
                case _:
                    raise KeyError("Unknowan modification")
        
            
class SortWorker:
    def __init__(self, output: Path, mode: str) -> None:
        self.output = output
        self.mode = mode
        
    def __call__(self, source_path: Path) -> None:
        file = FileMover(source_path)
        modeificator = PathModifier(source_path, self.output)
        destination_path = modeificator.get_mode_path(self.mode)
        if modeificator.categoty == 'archives':
            file.extract_to(destination_path)
        else:
            file.copy_to(destination_path)
        
        file.rename_from(TextNormalizer.normalize)        

@timing_decorator
def sort_thread_pool_executor(source: Path, output: Path, mode: str):
    
    list_arg_path = get_data_folder(source)
    sort_worker = SortWorker(output, mode)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(sort_worker, list_arg_path)
        
    logger.info(f"finish sorted dir whit mode '{mode}' - {source} >>> {output}")    

@timing_decorator
def sort_simple_thread(source: Path, output: Path, mode: str):
    list_arg_path = get_data_folder(source)
    
    sort_worker = SortWorker(output, mode)
    for arg_path in get_data_folder(source):
        th = Thread(target=sort_worker, args=(arg_path, ))
        th.start()
        th.join()
    logger.info(f"finish sorted dir whit mode '{mode}' - {source} >>> {output}")  
    
def sort_(source: Path, output: Path, mode: str):
    pass

if __name__ == "__main__":
    # sort_thread_pool_executor(source, output, mode)
    sort_simple_thread(source, output, mode)
        