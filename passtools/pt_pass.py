##########################################
# pass.py
#
# Models PassTools Pass
#
# Copyright 2012, Tello, Inc.
##########################################

"""
Define and provide methods for manipulating PassTools Pass objects.

"""

try:
    import simplejson as json
except ImportError:
    import json


import exceptions

class Pass(object):

    def __init__(self, template_id = None, template_fields_model = None):
        """
        Init, optionally populate, new pass.Pass instance
        If template_id and template_fields_model are supplied, will create new complete instance,
        else just create empty instance.
        
        API call used is v1/pass/<template_id> (POST)
        
        @type template_id: int
        @param template_id: ID of the template used to create new pass [Optional]
        @type template_fields_model: dict
        @param template_fields_model: template_fields_model dict of the template used to create new pass [Optional]
        @return: None
        """
        super(Pass, self).__init__()
        self.created_at = None
        self.pass_fields = None
        self.pass_id = None
        self.template_id = None
        self.url = None
        from client import PassToolsClient
        self.api_client = PassToolsClient()
        if template_id and template_fields_model:
            new_pass = self.create(template_id, template_fields_model)
            if new_pass:
                self.created_at = new_pass.created_at
                self.pass_fields = json.loads(new_pass.pass_fields, encoding="ISO-8859-1")
                self.pass_id = new_pass.pass_id
                self.template_id = new_pass.template_id
                self.url = new_pass.url


    def __str__(self):
        pretty_pass_fields = json.dumps(self.pass_fields, sort_keys = True, indent = 2, encoding="ISO-8859-1")
        return "id: %s\ntemplate_id: %s\nurl: %s\npass_fields: %s" % (self.pass_id,
                                                                        self.template_id,
                                                                        self.url,
                                                                        pretty_pass_fields)

    def __load_from_pass(self, pass_obj):
        # Any unset fields will be assigned to corresponding value present in pass_json
        field_name_map = {"created_at":"createdAt", "pass_fields":"passFields",
                                                                "pass_id":"id","template_id":"templateId", "url":"url"}
        for obj_field, db_field in field_name_map.items():
            if not getattr(self,obj_field,None):
                # if the object attribute is set to None, set it
                setattr(self, obj_field, pass_obj[db_field])



    def create(self, template_id = None, template_fields_model = None):
        """
        Create new Pass from specified template.

        API call used is v1/pass/<template_id> (POST)

        @type template_id: int
        @param template_id: ID of the template used to create new pass
        @type template_fields_model: dict
        @param template_fields_model: template_fields_model dict of the template used to create new pass
        @return: pass.Pass instance
        """
        if template_id is None:
            raise exceptions.InvalidParameterException("Pass.create() called without required parameter: template_id")
        try:
            test = float(template_id)
        except TypeError:
            raise exceptions.InvalidParameterException("Pass.create() called with non-numeric parameter: template_id ('%s')" % template_id)
        if template_fields_model is None:
            raise exceptions.InvalidParameterException("Pass.create() called without required parameter: template_fields_model")

        request_url = "/pass/%s" % (str(template_id))
        request = {"json":json.dumps(template_fields_model, encoding="ISO-8859-1")}
        response_code, response_data = self.api_client.post(request_url, request)

        new_pass = None
        if response_code == 200:
            new_pass = Pass()
            new_pass.pass_fields = json.dumps(template_fields_model, encoding="ISO-8859-1")
            new_pass.template_id = template_id
            new_pass.__load_from_pass(json.loads(response_data))

        return new_pass

    def update(self, update_fields = None):
        """
        Update existing pass

        API call used is v1/pass/<pass_id> (PUT)

        @type update_fields: dict
        @param update_fields: Pass.pass_fields dict
        @return: pass.Pass instance
        """
        updated_pass = None
        if update_fields is None or update_fields.pass_id is None:
            raise exceptions.InvalidParameterException("Pass.update() called without required parameter: update_fields")

        request_url = "/pass/%s" % (str(self.pass_id))
        request = {"json":json.dumps(update_fields.pass_fields, encoding="ISO-8859-1")}
        response_code, response_data = self.api_client.put(request_url, request)
        if response_code == 200:
            updated_pass = self.get()
        return updated_pass

    def push_update(self, pass_id = None):
        """
        Update installed passes using push method

        API call used is v1/pass/<pass_id>/push (PUT)

        @type pass_id: int
        @param pass_id: ID of desired pass.Pass. [Optional: If not supplied, = self.pass_id]
        @return: Dict
        """
        ret_data = {}
        if pass_id is None: pass_id = self.pass_id
        if pass_id is None:
            raise exceptions.InvalidParameterException("Pass.push_update() called without required parameter: pass_id")
        try:
            test = float(pass_id)
        except TypeError:
            raise exceptions.InvalidParameterException("Pass.push_update() called with non-numeric parameter: pass_id ('%s')" % pass_id)

        request_url = "/pass/%s/push" % (str(pass_id))
        response_code, response_data = self.api_client.put(request_url)
        if response_code == 200:
            ret_data = response_data

        return ret_data

    def get(self, pass_id = None):
        """
        Retrieve existing pass with specified ID

        API call used is v1/pass/<pass_id> (GET)

        @type pass_id: int
        @param pass_id: ID of desired pass.Pass. [Optional: If not supplied, = self.pass_id]
        @return: pass.Pass instance
        """
        if pass_id is None: pass_id = self.pass_id
        if pass_id is None:
            raise exceptions.InvalidParameterException("Pass.get() called without required parameter: pass_id")
        try:
            test = float(pass_id)
        except TypeError:
            raise exceptions.InvalidParameterException("Pass.get() called with non-numeric parameter: pass_id ('%s')" % pass_id)

        request_url = "/pass/%s" % (str(pass_id))
        response_code, response_data = self.api_client.get(request_url)

        new_pass = None
        if response_code == 200:
            new_pass = Pass()
            new_pass.__load_from_pass(response_data)

        return new_pass

    def count(self, template_id = None):
        """
        Retrieve count of existing passes created by owner of API-key
        If template_id is specified, count only passes associated with that template

        API call used is v1/pass (GET)

        @type templateId: int
        @param templateId: ID of the template used to create new pass
        @return: Integer
        """
        request = {}
        if template_id:
            request["templateId"] = template_id
        request_url = "/pass"
        response_code, response_data = self.api_client.get(request_url, request)

        ret_val = 0
        if response_code == 200:
            ret_val = int(response_data["Count"])

        return ret_val

    def list(self, **kwargs):
        """
        Retrieve list of existing passes created by owner of API-key
        If template_id is specified, retrieve only passes associated with that template
        Other parameters are translated into query-modifiers

        Note that list() returns abbreviated form of passes. Use get() to retrieve full pass.

        API call used is v1/pass (GET)

        @type templateId: int
        @param templateId: ID of the template used to create new pass
        @type pageSize: int
        @param pageSize: Maximum length of list to return [Optional; Default = 10]
        @type page: int
        @param page: 1-based index of page into list, based on page_size [Optional; Default = 1]
        @type order: string
        @param order: Name of field on which to sort list [Optional; From (ID, Name, Created, Updated)]
        @type direction: string
        @param direction: Direction which to sort list [Optional; From (ASC, DESC); Default = DESC]
        @return: List of pass.Pass instances
        """

        request_url = "/pass"
        response_code, response_data = self.api_client.get(request_url, **kwargs)

        pass_list = []
        if response_code == 200:
            for p in response_data["Passes"]:
                new_pass = Pass()
                new_pass.__load_from_pass(p)
                pass_list.append(new_pass)

        return pass_list

    def download(self, destination_path = None, pass_id = None):
        """
        Download pkpass file corresponding to existing pass with specified ID

        API call used is v1/pass/<pass_id>/download (GET)

        @type destination_path: str
        @param destination_path: path to receive pass file. Path must exist, and filename must end with ".pkpass"
        @type pass_id: int
        @param pass_id: pass_id of pass.Pass instance desired  [Optional: If not supplied, = self.pass_id]
        """
        if pass_id is None:
            if self.pass_id:
                pass_id = self.pass_id
            else:
                raise exceptions.InvalidParameterException("Pass.download() called without required parameter: pass_id")
        self.__validate_pass_id(pass_id)
        if destination_path is None:
            raise exceptions.InvalidParameterException("Pass.download() called without required parameter: destination_path")

        request_url = "/pass/%s/download" % (str(pass_id))
        response_code, response_data = self.api_client.get_json(request_url)

        if response_code == 200:
            fh = open(destination_path, "wb")
            fh.write(response_data)
            fh.close()

    def delete(self, pass_id = None):
        """
        delete existing pass

        API call used is v1/pass/<pass_id> (DELETE)

        @type pass_id: int
        @param pass_id: ID of the pass to delete [Optional: If not supplied, = self.pass_id]
        @return: None
        """
        if pass_id is None:
            pass_id = self.pass_id
        self.__validate_pass_id(pass_id)
        request_url = "/pass/%s" % (str(pass_id))
        response_code, response_data = self.api_client.delete(request_url, {})
        if response_code == 200:
            self.created_at = None
            self.pass_fields = None
            self.pass_id = None
            self.template_id = None
            self.url = None
            from client import PassToolsClient
            self.api_client = PassToolsClient()

    def __validate_pass_id(self, pass_id):
        try:
            test = float(pass_id)
        except (ValueError, TypeError):
            raise exceptions.exceptions.InvalidParameterException("Non-numeric parameter: pass_id ('%s')" % pass_id)

