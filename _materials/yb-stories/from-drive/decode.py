# -*- coding: utf-8 -*-
"""
Декодер слайдов историй, скачанных с Google Диска через MCP.

MCP отдаёт base64 в JSON; крупные ответы harness складывает в файл
tool-results/*.txt. Скрипт берёт такой файл (или несколько), декодирует
и кладёт рядом JPEG 1080×1920 под нужным именем.

    python3 decode.py <tool-result.txt> <имя-без-расширения>  [ещё пара, ещё…]
"""
import base64, io, json, os, sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def main(args):
    if len(args) % 2:
        sys.exit('нужны пары: <файл> <имя>')
    for src, name in zip(args[::2], args[1::2]):
        data = json.load(open(src))
        im = Image.open(io.BytesIO(base64.b64decode(data['content'])))
        if im.mode != 'RGB':
            im = im.convert('RGB')
        out = os.path.join(HERE, name + '.jpg')
        im.save(out, quality=92)
        print(f'{name}.jpg  {im.size[0]}×{im.size[1]}  {os.path.getsize(out)//1024} КБ')


if __name__ == '__main__':
    main(sys.argv[1:])
