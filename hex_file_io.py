from os import rename, remove, path
import shutil


class HEXFileIO:
    def __init__(self, file_name: str, directory: str | None = None) -> None:
        """
        Если папка не существует, то поднимается ошибка FileNotFoundError
        """

        self.directory = directory
        self.file_name = file_name

        if self.directory is None:
            self.original = file_name
            self.tmp = file_name + ".tmp"
            if path.isfile(file_name):
                shutil.copyfile(self.original, self.tmp)
            else:
                with open(self.tmp, "w+") as _:
                    pass
            self.tmp_file = open(self.tmp, "r+b")
            return

        self.original = path.join(directory, file_name)
        self.tmp = path.join(directory, file_name + ".tmp")
        if path.isfile(self.original):
            shutil.copy2(self.original, self.tmp)
        else:
            with open(self.tmp, "w+") as _:
                pass
        self.tmp_file = open(self.tmp, "r+b")

    def overwrite(self, start_byte: int, hex_bytes: str) -> None:
        self.tmp_file.seek(start_byte, 0)
        self.tmp_file.write(bytes.fromhex(hex_bytes))

    def read(self, start_byte: int, lenght: int) -> str:
        self.tmp_file.seek(start_byte, 0)
        data = self.tmp_file.read(lenght).hex(':')
        # if (len(data) // 2 < lenght):
        #     data += "00" * (lenght - (len(data) // 2))
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
    hfio = HEXFileIO("ata.txt")  # , "test_dir")

    hfio.overwrite(15, "61")
    # hfio.overwrite(2, "3432")

    print(hfio.read(0, 4))
    print(len(hfio))

    hfio.save()
