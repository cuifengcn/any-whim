# 需要预装 pdfminer3k 库

from pdfminer.pdfinterp import PDFResourceManager,process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import tempfile, os

import requests
r = requests.get("http://www.commonlii.org/sg/journals/SGYrBkIntLaw/2006/19.pdf")

def readPDF(bitfile,filename='temp'):
    def mk_file(filename,bitfile):
        path = tempfile.mkdtemp()
        pfile = path + filename
        with open(pfile,'wb') as f:
            f.write(bitfile)
        return open(pfile,'rb'),pfile
    f,pfile     = mk_file(filename,bitfile)
    rsrcmgr     = PDFResourceManager()
    retstr      = StringIO()
    laparams    = LAParams()
    device      = TextConverter(rsrcmgr,retstr,laparams=laparams)
    process_pdf(rsrcmgr,device,f)
    content     = retstr.getvalue()
    device.close()
    retstr.close()
    f.close()
    if os.path.exists(pfile):
        os.remove(pfile)
    return content

bitfile = r.content
outputString=readPDF(bitfile)
print(outputString)
