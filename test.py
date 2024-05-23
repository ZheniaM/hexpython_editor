import unittest

from hex_routines.hex_file_io import HEXFileIO


def wrapper(f):
    def wrapped(cls):
        file = HEXFileIO(cls.filename)
        f(cls, file).delete()
    return wrapped


class HexTest(unittest.TestCase):
    filename: str = "text.txt"

    def read(self, file: HEXFileIO, hex_text: str) -> str:
        return file.read(0, len(hex_text) >> 1).replace(":", "")

    @wrapper
    def test_can_read(self, file: HEXFileIO) -> HEXFileIO:
        text = b"Hello hex IO!".hex()
        file.overwrite(0, text)
        readed_text = self.read(file, text)
        self.assertEqual(readed_text, text)
        return file

    @wrapper
    def test_can_insert(self, file: HEXFileIO) -> HEXFileIO:
        text1 = b"hello".hex()
        text2 = b"world".hex()
        text_res = b"helworldlo".hex()
        file.insert(0, text1)
        file.insert(3, text2)
        readed_text = self.read(file, text_res)
        self.assertEqual(readed_text, text_res)
        return file

    @wrapper
    def test_can_save(self, file: HEXFileIO) -> HEXFileIO:
        text = b"hello world".hex()
        file.overwrite(5, text)
        file.save()
        file = HEXFileIO(self.filename)
        readed_text = self.read(file, text)
        self.assertEqual(readed_text, b"\00\00\00\00\00hello ".hex())
        return file


if __name__ == '__main__':
    unittest.main()
