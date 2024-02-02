
from src.jobs.DocReaderJobs import DocReaderJobs
from src.models.DocReaderModel import DocReaderModel
from worker.CelerySetup import celeryInstance
from flask import request, jsonify
from confs import baseDir

from src.database.seeds.clients import generateAClient

from src.libs.DocReaderAI import DocReaderAI
import os


class DockReaderController():

    # Agent
    docAI: DocReaderAI
    model: DocReaderModel
    jobs: DocReaderJobs

    def __init__(self):

        self.docAI = DocReaderAI()
        self.model = DocReaderModel()

        self.jobs = DocReaderJobs()

        self.docAI.addFile(userId=2, docId=2, defs="Ramazan Burak Korkmaz's resume",  filePath=baseDir +
                           "/src/libs/DocReaderAI/DocDocument/Document/RamazanBurakKorkmaz_16072023.pdf")

        self.docAI.addFile(userId=1, docId=1, defs="Hasan Özkul's resume",
                           filePath=baseDir+"/src/libs/DocReaderAI/DocDocument/Document/hasan_ozkul.pdf")

        self.docAI.setFiles2TheAgentsMind(userId=2)
        self.docAI.setFiles2TheAgentsMind(userId=1)

    def askQuestion(self):
        q = request.args.get('q')
        answer = self.docAI.getAnswer('Ramazan Burak Korkmaz Kac yasinda>')
        self.model.addMessage(message='Testing SVVVVV', userId=2432543245324)
        # result = self.jobs.addOne.delay()
        # result.forget()
        # return jsonify({'result': result.status, 'answer': result.get()})
        return jsonify({'answer': answer})
        return jsonify({'result': 'TEst'})

    def getResult(self):

        result = celeryInstance.send_task('app.jobs.DocReaderJobs.addOne')
        print('celeryInstanceceleryInstance-->>', dir(celeryInstance))

        return jsonify({'result': result.status, 'answer': result.get()})

    def uploadFiles(self):
        self.docAI.getAnswer('Do you know Ramazan Burak Korkmaz')
        return jsonify({'message': 'FromClasss Uploaddinggg'})
