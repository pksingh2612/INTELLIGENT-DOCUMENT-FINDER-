import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template,send_from_directory
from werkzeug.utils import secure_filename
import  sys
from auto_tagify import AutoTagify
import PyPDF2 
import sqlite3

UPLOAD_FOLDER ='../projecthostpython/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'pptx','docx'])
lastFilename=''
e_words=[]
csvData = ['FileName','Auto_tag','Manual_tag']
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#user-defined
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#function built-in user-defined	
@app.route('/')
def upload_form():
	return render_template('upload2.html')


@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
        #print(files)
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('File(s) successfully uploaded')
        
		return redirect('/manual')

@app.route('/manual')
def manualtag():
    li=[]
    d = UPLOAD_FOLDER
    for path in os.listdir(d):
        print(path)
        li.append(path)    
    return render_template('manual.html', paths = li)


@app.route('/window')
def window():
    global lastFilename
    name,ext=os.path.splitext(request.args.get('type'))
    filenamenew=name+ext
    lastFilename=filenamenew
    if ext==".pdf":        
        # creating a pdf file object 
        pdfFileObj = open(UPLOAD_FOLDER+"/"+filenamenew, 'rb')    
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)      
        # printing number of pages in pdf file 
        print(pdfReader.numPages) 
        #print(pdfReader.getDocumentInfo())
        #print(pdfReader.getIsEncrypted())                
        # creating a page object 
        bundle=""
        for i in range(1,pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            # extracting text from page 
            #print(pageObj.extractText())
            bundle+=pageObj.extractText()      
        #print(bundle)
        # closing the pdf file object 
        pdfFileObj.close()

        #Auto tagging
        t = AutoTagify()
        t.text = bundle
        #print(t.tag_list())
        e_words = list(dict.fromkeys(t.tag_list()))  
        #print(e_words)


    else:
        file = open(UPLOAD_FOLDER+"/"+filenamenew,"r+") 
        #print(type(file.read()))

        t = AutoTagify()
        t.text = file.read()
        #print(len(t.tag_list()))
        e_words = list(dict.fromkeys(t.tag_list()))  
        #print(e_words)
        file.close() 
    
    conn = sqlite3.connect('TAGS.db')
    #c = conn.cursor()
    # Insert a row of data
    conn.execute('''INSERT INTO Tag (Filename,Auto_tag,Manual_tag,status) VALUES (?,?,?,?)''',(filenamenew, str(e_words),str([]), 1))
    
    # Save (commit) the changes
    conn.commit()
    conn.close()
     
        
    return render_template('window.html',F=filenamenew,L=e_words)


@app.route('/convert' ,methods=['POST'])
def convert():
    if request.method == 'POST':
        flash('Converting wait for while')
        import main4
    return redirect('/manual')

@app.route('/manual_tag',methods=['POST'])
def manual_tag():
    if request.method == 'POST':
        text=[]
        text.append(request.form["manual_tag"])
        text=text[0].split()
        print(text)
        
        conn = sqlite3.connect('TAGS.db')
        #c = conn.cursor()
        conn.execute('''UPDATE Tag set Manual_tag = (?) where Filename = (?)''',(str(text),lastFilename))
        conn.commit()
        conn.close()
        
    return redirect('/manual')

if __name__ == "__main__":
    app.run(debug=True)
