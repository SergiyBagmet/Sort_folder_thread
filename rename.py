import re



class TextNormalizer:

    __CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    __TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    
    __TRANS = {ord(c):t for c, t in zip(__CYRILLIC_SYMBOLS, __TRANSLATION)} | {ord(c.upper()):t.upper() for c, t in zip(__CYRILLIC_SYMBOLS, __TRANSLATION)}
    
    @classmethod
    def normalize(cls, name: str) -> str:
        """
        Normalize a given string by replacing non-alphanumeric characters with underscores.

        Args:
            name (str): The input string to be normalized.
        Returns:
            str: The normalized string with non-alphanumeric characters replaced by underscores.
        """
        t_name = name.translate(cls.__TRANS)
        t_name = re.sub(r'\W', '_', t_name)
        return t_name
    

if __name__ == "__main__":
    pass
    