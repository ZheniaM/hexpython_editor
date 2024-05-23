from os import rename, remove, path
import shutil

from icecream.icecream import ic


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
        if 1 & len(hex_bytes):
            hex_bytes += "0"
        self.tmp_file.seek(start_byte, 0)
        self.tmp_file.write(bytes.fromhex(hex_bytes))
        self.is_chaged = True

    def insert(self, start_byte: int, hex_bytes: str) -> None:
        self.tmp_file.seek(start_byte)
        if 1 & len(hex_bytes):
            hex_bytes += "0"
        size = len(hex_bytes) // 2
        pos_to_write = start_byte
        old = self.tmp_file.read(size)
        new = bytes.fromhex(hex_bytes)
        while len(new):
            self.tmp_file.seek(pos_to_write)
            self.tmp_file.write(new)
            new = old
            old = self.tmp_file.read(size)
            pos_to_write += size
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
    remove(hfio.original)
    hfio = HEXFileIO("ata.txt")
    ic(len(hfio))
    ic(hfio.read(0, 20))
    hfio.overwrite(0, "000102030405060708090A0B0C0D0E0F")
    ic(hfio.read(0, 20))
    hfio.insert(8, "11223")
    # hfio.overwrite(2, "3432")

    ic(len(hfio))
    ic(hfio.read(0, len(hfio)))

    hfio.save()
