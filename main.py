from pathlib import Path
from threading import Thread
import concurrent.futures
import argparse
from replase_file import  FileMover
from rename import TextNormalizer


"""
--source [-s] 
--output [-o] default folder = dist
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")
parser.add_argument("--mode", "-m", help="modification for sort ", default="category")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))
mode = args.get("mode")

class GetPool:
    def __init__(self, source: Path, output: Path, mode: str) -> None:
        self.file_list = self.__get_data_folder(source)
        self.output = output
        self.mode = mode
        self.ext_form = {
            'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.PNG'],
            'video': ['.avi', '.mp4', '.mov', '.mkv'],
            'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
            'audio': ['.mp3', '.ogg', '.wav', '.amr'],
            'archives': ['.zip', '.gz', '.tar'],
        }
        
    def __get_data_folder(self, path: Path, data=None) -> list[Path]:
        if data is None : data = []
        for item in path.iterdir():
            if item.is_file():
                data.append(item)
            elif item.is_dir():
                self.__get_data_folder(item, data)
        return data
    
    def __get_dir_name(self, path: Path) -> str:
        name_dir = ""
        for key, val in self.ext_form.items():
            if path.suffix in val:
                name_dir = key
                break
        if not name_dir:  # если нет совпадений 
            name_dir = "others"
        return name_dir
    
    def mode_pool(self) -> dict[Path, Path]:
        match self.mode:
            case "category":
                return {f_path: self.output / self.__get_dir_name(f_path) for f_path in self.file_list}
            case "ext":
                return {f_path: self.output / f_path.suffix[1:].upper() for f_path in self.file_list}
            case _:
                raise KeyError("Unknowan modification for get pool")
        
            
def file_worker(source_path: Path, destination_path: Path):
    file = FileMover(source_path, rename=TextNormalizer.normalize)
    if not file.is_archive:
        file.copy_to(destination_path)
    else:
        file.extract_to(destination_path)        

if __name__ == "__main__":
    get_pool = GetPool(source, output, mode)
    pool = get_pool.mode_pool()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(file_worker, pool.keys(), pool.values())