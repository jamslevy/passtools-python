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

class Template(object):

    def __init__(self, template_id = None):
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
        self.api_client = client.PassToolsClient()
        self.template_id = template_id
        self.name = None
        self.description = None
        self.fields_model = {}
        if self.template_id:
            new_template = self.get(self.template_id)
            if new_template:
                self.name = new_template.name
                self.description = new_template.description
                self.fields_model = new_template.fields_model

    def __str__(self):
        pretty_template_fields = json.dumps(self.fields_model, sort_keys = True, indent = 2, encoding="ISO-8859-1")
        return "id=%s\nname=%s\ndescription:%s\nfields_model:%s" % (self.template_id,
                                                                    self.name,
                                                                    self.description,
                                                                    pretty_template_fields)

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
            new_template = Template()
            try:
                new_template.template_id = int(response_data["templateHeader"]["id"])
            except:
                raise exceptions.InvalidParameterException("No template returned for template_id: %s" % template_id)
            new_template.name = response_data["templateHeader"]["name"]
            new_template.description = response_data["templateHeader"]["description"]
            new_template.fields_model = response_data["fieldsModel"]
        else:
            new_template = None
        return new_template

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
                new_template = Template()
                new_template.template_id = int(template_item["id"])
                new_template.name = template_item["name"]
                new_template.description = template_item["description"]
                new_template.fields_model = {}
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
            self.api_client = client.PassToolsClient()
            self.template_id = None
            self.name = None
            self.description = None
            self.fields_model = {}

    def __validate_template_id(self, template_id):
        try:
            test = float(template_id)
        except (ValueError, TypeError):
            raise exceptions.InvalidParameterException("Non-numeric parameter: template_id ('%s')" % template_id)


