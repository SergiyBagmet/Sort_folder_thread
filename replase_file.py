from pathlib import Path
import shutil
import typing as t

            
class FileMover:
    def __init__(self, source_path: Path, rename: t.Callable | None=None ) -> None:
        self.source_path = source_path
        self.rename = rename
        self.is_archive = True if source_path.suffix in ['.zip', '.gz', '.tar', '.rar', '.7z', '.tgz', '.tbz2', '.zipx', '.txz'] else False
    
    def replace_to(self, destination_path : Path) -> Path:
        destination_path.mkdir(exist_ok=True, parents=True)  # создаем новую папку если такой нет
        new_name = self.rename(self.source_path.stem) + self.source_path.suffix if self.rename is not None else self.source_path.name
        self.source_path.replace(destination_path / new_name)  # перенос файлов в папки по категориям
   
    def copy_to(self, destination_path: Path) -> Path:
        destination_path.mkdir(exist_ok=True, parents=True)  # создаем новую папку если такой нет
        new_name = self.rename(self.source_path.stem) + self.source_path.suffix if self.rename is not None else self.source_path.name
        shutil.copy2(self.source_path, destination_path / new_name)  # копирование файла
      
    def extract_to(self, target_dir: Path, del_archive=False) -> None:
        new_name =  self.rename(self.source_path.stem)  if self.rename is not None else self.source_path.stem
        target_dir = target_dir / new_name
        target_dir.mkdir(exist_ok=True, parents=True)  # создаем папку для архива
        try:
            shutil.unpack_archive(self.source_path, target_dir)  # распаковка
            if del_archive:  # удаляем архив по флагу после распаковки
                self.source_path.unlink()
        except ValueError:
            print(f"Failed to unpack the archive: {self.source_path.name}")
        except shutil.ReadError:
            print(f"Archive - {self.source_path.stem} not unpacked\tunknown extension({self.source_path.suffix})")

if __name__ == "__main__":
    pass

