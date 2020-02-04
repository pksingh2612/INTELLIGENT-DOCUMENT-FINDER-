import  sys  # built-in
import  os  

import  comtypes.client
#pip install comtypes

def  word_to_pdf(inputFileName,outputFileName):
    pdf_format_key = 17
    file_in = inputFileName 
    file_out = outputFileName 
    worddoc = comtypes.client.CreateObject('Word.Application')
    doc = worddoc.Documents.Open(file_in)
    doc.SaveAs(file_out, FileFormat = pdf_format_key)
    doc.Close()
    worddoc.Quit()

def PPTtoPDF(inputFileName, outputFileName, formatType = 32):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName + ".pdf"
    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType) # formatType = 32 for ppt to pdf
    deck.Close()
    powerpoint.Quit()

def fun():
    d1 = '../projecthostpython/static'
    l=[]
    for path in os.listdir(d1):
        l.append(path)
        print(l)
        for i in l:
            name,ext=os.path.splitext(i)
            print(name,ext,i)
            if ext=='.docx':
                # word_to_pdf(UPLOAD_FOLDER+"/"+i,UPLOAD_FOLDER+"/"+name+".pdf")
                word_to_pdf(os.path.abspath("./static/"+i),os.path.abspath("./static/"+name+".pdf"))
                l.remove(i)
            elif ext=='.pptx':
                PPTtoPDF(os.path.abspath("./static/"+i),os.path.abspath("./static/"+name+".pdf"), formatType = 32)
                l.remove(i)
            else:
                print('no need')

fun()

