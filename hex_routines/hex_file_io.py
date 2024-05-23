from os import rename, remove, path
import shutil

# from icecream.icecream import ic


class HEXFileIO:
    def __init__(self, file_name: str) -> None:
        """
        Если папка не существует, то поднимается ошибка FileNotFoundError
        """

        self.original = file_name
        self.is_chaged = False

        self.tmp = file_name + ".tmp"
        if path.isfile(self.original):
            shutil.copy2(self.original, self.tmp)
        else:
            with open(self.tmp, "w+") as _:
                pass
        self.tmp_file = open(self.tmp, "r+b")

    def overwrite(self, start_byte: int, hex_bytes: str) -> None:
        self.tmp_file.seek(start_byte, 0)
        self.tmp_file.write(bytes.fromhex(hex_bytes))
        self.is_chaged = True

    def insert_empty_cell(self, position: int) -> None:
        self.tmp_file.seek(position, 0)
        self.tmp_file.write(b'\x00')
        self.is_chaged = True

    def read(self, start_byte: int, lenght: int) -> str:
        self.tmp_file.seek(start_byte, 0)
        data = self.tmp_file.read(lenght).hex(':')
        return data

    def save(self) -> None:
        """
        После сохранения нужно будет снова открыть файл.

        Т.е. данный экземпляр класса будет бесполезен
        """
        self.tmp_file.close()
        if path.isfile(self.original):
            remove(self.original)
        rename(self.tmp, self.original)

    def delete(self) -> None:
        self.tmp_file.close()
        remove(self.tmp)

    def __len__(self) -> int:
        self.tmp_file.seek(0, 2)
        return self.tmp_file.tell()


if __name__ == "__main__":
    hfio = HEXFileIO("ata.txt")

    hfio.overwrite(15, "61")
    # hfio.overwrite(2, "3432")

    print(hfio.read(0, 4))
    print(len(hfio))

    hfio.save()
