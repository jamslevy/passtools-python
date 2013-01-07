##########################################
# pt_template.py
#
# Models PassTools Template
#
# Copyright 2012, Tello, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Template objects.

"""

try:
    import simplejson as json
except ImportError:
    import json

import client
import exceptions
import datetime

class Template(object):

    def __init__(self, template_id = None, api_client=None):
        """
        Init, optionally populate, new pt_template.Template instance
        If template_id and template_fields_model are supplied, will retrieve complete instance,
        else just create new empty instance.

        API call used is v1/template (GET)

        @type template_id: int
        @param template_id: ID of the desired template [Optional]
        @return: None
        """
        super(Template, self).__init__()
        self.api_client = api_client or client.PassToolsClient()
        self.template_id = template_id
        self.name = None
        self.description = None
        self.fields_model = {}
        if self.template_id:
            new_template = self.get(self.template_id)
            for attr,val in new_template.__dict__.iteritems():
                setattr(self, attr, val)

    def __str__(self):
        pretty_template_fields = json.dumps(self.fields_model, sort_keys = True, indent = 2, encoding="ISO-8859-1")
        return "id=%s\nname=%s\ndescription:%s\nfields_model:%s" % (self.template_id,
                                                                    self.name,
                                                                    self.description,
                                                                    pretty_template_fields)

    def __load_from_dict(self, template_dict):

        field_name_map = {
            "fields_model": "fieldsModel",
            "header": "templateHeader"
        }       
        for obj_field, db_field in field_name_map.iteritems():
            if not getattr(self,obj_field,None):
                # if the object attribute is not set, set it
                obj_val = template_dict.get(db_field,None)        
                setattr(self, obj_field, obj_val)

        self.__load_from_header()

    def __load_from_header(self):
        header_name_map = {
            "name": "name",
            "description": "description",
            "template_id": "id"
        }
        for header_field, db_field in header_name_map.iteritems():
            if self.header and not getattr(self,header_field,None):
                # if the object attribute is not set, set it
                header_val = self.header.get(db_field,None)     
                if header_val:
                    if header_field == 'template_id':
                        header_val = int(header_val)      
                    setattr(self, header_field, header_val)  

        self.created = datetime.datetime.strptime(self.header['createdAt'], '%Y-%m-%d %H:%M:%S.%f') 
        self.updated = datetime.datetime.strptime(self.header['updatedAt'], '%Y-%m-%d %H:%M:%S.%f')     


    def get(self, template_id = None):
        """
        Retrieve Template specified by template_id

        API call used is v1/template/<template_id> (GET)

        @type template_id: int
        @param template_id: ID of the desired template
        @return: pt_template. Template instance
        """
        if template_id is None: template_id = self.template_id
        if template_id is None:
            raise exceptions.InvalidParameterException("Template.get() called without required parameter: template_id")
        self.__validate_template_id(template_id)
        request_url = "/template/%s" % (str(template_id))
        response_code, response_data = self.api_client.get(request_url)
        if response_code == 200:
            template_instance = Template(api_client=self.api_client)
            template_instance.__load_from_dict(response_data)
            if not template_instance.template_id:
                raise exceptions.InvalidParameterException("No template returned for template_id: %s" % template_id)

        else:
            template_instance = None
        return template_instance

    def count(self):
        """
        Retrieve count of existing templates created by owner of API-key

        API call used is v1/template/headers (GET)

        @return: Integer
        """
        request_url = "/template/headers"
        response_code, response_data = self.api_client.get(request_url)

        ret_val = 0
        if response_code == 200:
            ret_val = int(response_data["count"])

        return ret_val

    def list(self, **kwargs):
        """
        Retrieve list of existing templates created by owner of API-key
        Optional parameters are translated into query-modifiers

        Note that list() returns abbreviated form of templates. Use get() to retrieve full template.

        API call used is v1/template/headers (GET)

        @type pageSize: int
        @param pageSize: Maximum length of list to return [Optional; Default = 10]
        @type page: int
        @param page: 1-based index of page into list, based on page_size [Optional; Default = 1]
        @type order: string
        @param order: Name of field on which to sort list [Optional; From (ID, Name, Created, Updated)]
        @type direction: string
        @param direction: Direction which to sort list [Optional; From (ASC, DESC); Default = DESC]
        @return: List of pt_template.Template instances
        """
        template_list = []
        request_url = "/template/headers"
        response_code, response_data = self.api_client.get(request_url, **kwargs)
        if response_code == 200:
            dict_list = response_data.get("templateHeaders",[])
            for template_item in dict_list:
                new_template = Template(api_client=self.api_client)
                new_template.header = template_item
                new_template.__load_from_header()

                template_list.append(new_template)
        return template_list

    def delete(self, template_id = None):
        """
        delete existing template

        API call used is v1/template/<template_id> (DELETE)

        @type template_id: int
        @param template_id: ID of the template to delete [Optional: If not supplied, = self.template_id]
        @return: None
        """
        if template_id is None:
            template_id = self.template_id
        self.__validate_template_id(template_id)
        request_url = "/template/%s" % (str(template_id))
        response_code, response_data = self.api_client.delete(request_url, {})
        if response_code == 200:
            self.template_id = None
            self.name = None
            self.description = None
            self.fields_model = {}

    def __validate_template_id(self, template_id):
        try:
            test = float(template_id)
        except (ValueError, TypeError):
            raise exceptions.InvalidParameterException("Non-numeric parameter: template_id ('%s')" % template_id)


