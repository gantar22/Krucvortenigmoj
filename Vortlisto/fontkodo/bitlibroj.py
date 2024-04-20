from radikoj import DecomposedWord, generate_derivative_words, load_roots, base_word_score
import html.parser
import os
import zipfile

def get_words(path_to_epub : str, roots : set[str]) -> list[DecomposedWord]:
    """Loads an epub and extracts all the valid words
    """

    def get_text(path_to_epub : str) -> str:
        zip = zipfile.ZipFile(path_to_epub)
        text = ""
        for file_name in os.listdir(path_to_epub):
            file_bytes = zip.read(file_name)
            text += os.fsencode(file_bytes) # fixme


    pass

def get_epub_paths() -> list[str]:
    """Return a list of all paths to epub.
    """

def main():
    outputfile = open('./artefaktoj/bitlibroj.dict','w',encoding='utf8')

    roots : dict[str,int] = load_roots()
    for path in get_epub_paths():
        words = get_words(path)
        for word in words:
            outputfile.write(f'{word};{base_word_score(word,roots)}\n')

main()