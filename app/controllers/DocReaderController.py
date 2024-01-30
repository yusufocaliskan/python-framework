
from flask import request, jsonify


from libs.DocReaderAI import DocReaderAI
import os


class DockReaderController():

    path = os.getcwd()

    # Agent
    docAI: DocReaderAI

    def __init__(self):
        self.docAI = DocReaderAI()

        self.docAI.addFile(userId=1, docId=1, defs="Hasan Özkul's resume",  filePath=self.path +
                           "/libs/DocReaderAI/DocDocument/Document/hasan_ozkul.pdf")

        self.docAI.addFile(userId=2, docId=2, defs="Ramazan Burak Korkmaz's resume",  filePath=self.path +
                           "/libs/DocReaderAI/DocDocument/Document/RamazanBurakKorkmaz_16072023.pdf")

        self.docAI.setFiles2TheAgentsMind(userId=1)

    def askQuestion(self):
        q = request.args.get('q')
        answer = self.docAI.getAnswer(q)

        print(answer)
        return jsonify({'question': q, 'answer': answer})

    def uploadFiles(self):
        self.docAI.getAnswer('Do you know Ramazan Burak Korkmaz')
        return jsonify({'message': 'FromClasss Uploaddinggg'})
