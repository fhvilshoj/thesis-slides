import os
from concurrent.futures import ThreadPoolExecutor as Executor
import xml.etree.ElementTree as ET
from subprocess import run
from collections import namedtuple
from configparser import ConfigParser

import os

def main(ipe_prefix='', working_dir='.'):

    os.makedirs(os.path.join(working_dir, 'ipe'), exist_ok=True)
    os.makedirs(os.path.join(working_dir, 'svgs'), exist_ok=True)

    name = '%s/ipe-graphics' % working_dir


    pdf_fn = "%s.pdf" % name
    xml_fn = "%s/ipe/tmp.xml" % working_dir

    run('%sipeextract %s %s' % (ipe_prefix, pdf_fn, xml_fn), shell=True, check=True)

    root = ET.parse(xml_fn).getroot()
    Result = namedtuple('Result', 'page view')

    to_extract = []
    pi = 0

    for p in root:
        if p.tag != 'page': continue
        pi += 1

        vi = 0
        for v in p:
            if v.tag != 'layer': continue

            vi += 1
            to_extract.append( Result(pi, vi) )

        if vi == 0:
            to_extract.append( Result(pi, None) )

    def extract_page(res: Result):
        from subprocess import run
        import pathlib
        view = "" if res.view is None else "-view %d" % res.view
        file_suffix = "" if res.view is None else "_v%d" % res.view
        template = '%siperender -svg -resolution 200 -page %%d %s %s.pdf %s/svgs/p%%d%s.svg' % (ipe_prefix, view, name, working_dir, file_suffix)
        cmd = template % (res.page, res.page)
        r = run(cmd, check=True, shell=True)
        return r.returncode


    with Executor(max_workers=4) as exe:
        jobs = [exe.submit(extract_page, r) for r in to_extract]
        codes = [j.result() for j in jobs]

if __name__ == "__main__":
    working_dir = "/".join(os.path.realpath(__file__).split('/')[:-1])

    config = ConfigParser()
    config.read(os.path.join(working_dir, 'ipe-config.ini'))

    main(ipe_prefix=config.get('Default', 'ipe_path'), working_dir=working_dir)

