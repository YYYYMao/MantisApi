#!/usr/bin/python
# -*- coding: utf-8 -*-

from suds.client import Client
url = 'http://YourMantisIp/mantis/api/soap/mantisconnect.php?wsdl'
import base64
class MantisTest(object):

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def mc_issue_get(self,id):
        client = Client(url)
        content = client.service.mc_issue_get(self.username, self.password, id)
        return content

    def mc_issue_add(self,project,data):
        client = Client(url)
        issue = client.factory.create('IssueData')
        issue.project.name = project
        for d in data:
             issue.__setattr__(d, data[d])
        try:
            issue_id = client.service.mc_issue_add(
                username=self.username,
                password=self.password,
                issue=issue)
            return issue_id
        except Exception as e:
            print e.message

    def mc_issue_update(self,id,data):
        client = Client(url,cache=None)
        content = self.mc_issue_get(id = id)
        for d in data:
             content.__setattr__(d, data[d])
        try:
            issue = client.service.mc_issue_update(
                username=self.username,
                password=self.password,
                issueId = id,
                issue=content)
            return issue
        except Exception as e:
            print e.message

    def mc_issue_note_add(self,id,data):
        client = Client(url)
        try:
            note_id = client.service.mc_issue_note_add(
                username=self.username,
                password=self.password,
                issue_id = id,
                note=data)
            return note_id
        except Exception as e:
            print e.message

    def mc_project_get_issue_headers(self,project_id,page_number,per_page = -1):
        client = Client(url)
        try:
            issues = client.service.mc_project_get_issue_headers(
                username=self.username,
                password=self.password,
                project_id = project_id,
                page_number=page_number,
                per_page = per_page)
            return issues
        except Exception as e:
            print e.message

    def mc_project_get_issues(self,project_id,page_number,per_page = -1):
        client = Client(url)
        try:
            issues = client.service.mc_project_get_issues(
                username=self.username,
                password=self.password,
                project_id = project_id,
                page_number=page_number,
                per_page = per_page)
            return issues
        except Exception as e:
            print e.message


    def mc_project_get_notes(self,project_id):
        try:
            issues = self.mc_project_get_issues(project_id,1,-1)
            for i in issues:
                if 'notes' in i:
                    print 'issue id '+str(i.id)
                    print i.notes[0]
                    print '-----------------------'
        except Exception as e:
            print e.message

    def mc_project_get_id_from_name(self,project_name):
        client = Client(url)
        try:
            project_id = client.service.mc_project_get_id_from_name(
                username=self.username,
                password=self.password,
                project_name = project_name)
            return project_id
        except Exception as e:
            print e.message


    def mc_issue_relationship_add(self,issue_id,data):
        client = Client(url)
        try:
            relationship_id = client.service.mc_issue_relationship_add(
                username=self.username,
                password=self.password,
                issue_id = issue_id,
		relationship = data)
            return relationship_id
        except Exception as e:
            print e.message

    def mc_issue_attachment_add(self,issue_id,name,file_type,content):
        client = Client(url)
        try:
            attachment_id = client.service.mc_issue_attachment_add(
                username=self.username,
                password=self.password,
                issue_id = issue_id,
		        name = name,
                file_type = file_type,
                content = content)
            return attachment_id
        except Exception as e:
            print e.message

if __name__ == "__main__":
    r = MantisTest(username='mantisUsername', password='mantisPassword')
    print r.mc_issue_get(6673)  
    data = {
         'category':'General',
         'summary':'ssss',
         'description':'asdsdsdada',
    }
    result = r.mc_issue_add('Sandbox',data)

    r.mc_project_get_issues(16,1,-1)
    r.mc_project_get_id_from_name('Issue')

    image_bin_data = ""
    with open('ccc.jpg', 'r') as f:
        image_bin_data = base64.encodestring( f.read() )

    attach_result = r.mc_issue_attachment_add(result,u'ccc.jpg','image/jpeg',image_bin_data)

    print attach_result
