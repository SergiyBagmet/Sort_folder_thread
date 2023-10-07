from pathlib import Path
import shutil
import typing as t


from my_logger import MyLogger
logger = MyLogger("file_mover").get_logger()
            
class FileMover:
    def __init__(self, source_path: Path) -> None:
        self.source_path = source_path
        self.is_archive = True if source_path.suffix in ['.zip', '.gz', '.tar', '.rar', '.7z', '.tgz', '.tbz2', '.zipx', '.txz'] else False
    
    @property
    def source_path(self) -> Path:
        return self._source_path
    
    @source_path.setter
    def source_path(self, source_path: Path) -> None:
        self.path_exists(source_path)
        self._source_path = source_path

    def path_exists(self, source_path: Path) -> bool:
        if not source_path.exists():
            logger.error(f"Not exists path: {source_path}")
            raise FileNotFoundError(f"{source_path} not exists.")
        
    def replace_to(self, destination_path : Path) -> Path:
        destination_path.mkdir(exist_ok=True, parents=True)  # создаем новую папку если такой нет
        try:
            self.source_path = self.source_path.replace(destination_path)  # перенос файлов в папки по категориям
        except PermissionError as e:
            logger.error(f"Permission error while replacing: {e}")
        except OSError as e:
            logger.error(f"Error while replacing: {e}")
   
    def copy_to(self, destination_path: Path) -> Path:
        destination_path.mkdir(exist_ok=True, parents=True)  # создаем новую папку если такой нет
        try:
            self.source_path = shutil.copy2(self.source_path, destination_path)  # копирование файла
        except PermissionError as e:
            logger.error(f"Permission error while copying: {e}")
        except OSError as e:
            logger.error(f"Error while copying: {e}")
      
    def extract_to(self, target_dir: Path, del_archive=False) -> None:
        target_dir.mkdir(exist_ok=True, parents=True)  # создаем папку для архива
        try:
            shutil.unpack_archive(self.source_path, target_dir)  # распаковка
            self.source_path = target_dir
            if del_archive:  # удаляем архив по флагу после распаковки
                self.source_path.unlink()
        except ValueError:
            logger.error(f"Failed to unpack the archive: {self.source_path.name}")
        except shutil.ReadError:
            logger.error(f"Archive - {self.source_path.stem} not unpacked\tunknown extension({self.source_path.suffix})")
            
    def rename_from(self, func_normalize: t.Callable):
        if self.source_path.is_dir():
            new_name = func_normalize(self.source_path.name)  
        else:
            new_name = func_normalize(self.source_path.stem) + self.source_path.suffix 
             
        new_path = self.source_path.parent / new_name
        try:
            self.source_path = self.source_path.rename(new_path) 
        except PermissionError as e:
            logger.error(f"Permission error while renaming: {e}")
        except OSError as e:
            logger.error(f"Error while renaming: {e}")    

if __name__ == "__main__":
    pass

