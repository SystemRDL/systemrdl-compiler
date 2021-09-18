#!/usr/bin/env python3

import json

from systemrdl.importer import RDLImporter
from systemrdl import component as comp
from systemrdl.rdltypes import AccessType

class JSONImporter(RDLImporter):

    def import_file(self, path: str) -> None:
        super().import_file(path)

        # Load the JSON from a file and convert it to primitive Python objects
        with open(path, 'r', encoding='utf-8') as f:
            json_obj = json.load(f)

        # Make sure top level object is an addrmap type
        if json_obj.get('type', None) != "addrmap":
            self.msg.fatal(
                "Top JSON object must be an addrmap type",
                self.default_src_ref
            )

        # Decode the JSON object
        # Set is_top=True so that decode returns a definition rather than an instance
        top_addrmap_def = self.decode_addrmap(json_obj, is_top=True)

        # Register the top definition in the root namespace
        self.register_root_component(top_addrmap_def)


    def decode_field(self, json_obj: dict) -> comp.Field:
        # validate that this json object contains all the required fields
        if 'inst_name' not in json_obj:
            self.msg.fatal("JSON object is missing 'inst_name'", self.default_src_ref)
        if 'lsb' not in json_obj:
            self.msg.fatal("JSON object is missing 'lsb'", self.default_src_ref)
        if 'msb' not in json_obj:
            self.msg.fatal("JSON object is missing 'msb'", self.default_src_ref)
        if 'reset' not in json_obj:
            self.msg.fatal("JSON object is missing 'reset'", self.default_src_ref)
        if 'sw_access' not in json_obj:
            self.msg.fatal("JSON object is missing 'sw_access'", self.default_src_ref)

        # Create an RDL field definition
        comp_def = self.create_field_definition()

        # Apply reset property if it was set
        if json_obj['reset'] is not None:
            self.assign_property(comp_def, 'reset', json_obj['reset'])

        # decode and apply the sw access property.
        # Since it uses the native enumeration name, we can do this directly
        sw = AccessType[json_obj['sw_access']]
        self.assign_property(comp_def, 'sw', sw)

        # Instantiate the component definition
        inst = self.instantiate_field(
            comp_def,
            json_obj['inst_name'],
            json_obj['lsb'],
            json_obj['msb'] - json_obj['lsb'] + 1
        )
        return inst


    def decode_reg(self, json_obj: dict) -> comp.Reg:
        # validate that this json object contains all the required fields
        if 'inst_name' not in json_obj:
            self.msg.fatal("JSON object is missing 'inst_name'", self.default_src_ref)
        if 'addr_offset' not in json_obj:
            self.msg.fatal("JSON object '%s' is missing 'addr_offset'" % json_obj['inst_name'], self.default_src_ref)
        if 'children' not in json_obj:
            self.msg.fatal("JSON object is missing 'children'", self.default_src_ref)

        comp_def = self.create_reg_definition()

        # Collect children
        for child_json in json_obj['children']:
            # Check that the child is the correct type. Reg can only contain fields
            t = child_json.get('type', None)
            if t != "field":
                self.msg.fatal(
                    "Invalid child type '%s'" % t,
                    self.default_src_ref
                )

            # Convert each child component and add it to our reg definition
            child_inst = self.decode_field(child_json)
            self.add_child(comp_def, child_inst)

        # Convert the definition into an instance
        inst = self.instantiate_reg(
            comp_def,
            json_obj['inst_name'],
            json_obj['addr_offset']
        )
        return inst


    def decode_regfile(self, json_obj: dict) -> comp.Regfile:
        if 'inst_name' not in json_obj:
            self.msg.fatal("JSON object is missing 'inst_name'", self.default_src_ref)
        if 'addr_offset' not in json_obj:
            self.msg.fatal("JSON object '%s' is missing 'addr_offset'" % json_obj['inst_name'], self.default_src_ref)
        if 'children' not in json_obj:
            self.msg.fatal("JSON object is missing 'children'", self.default_src_ref)

        comp_def = self.create_regfile_definition()

        for child_json in json_obj['children']:
            t = child_json.get('type', None)
            if t == "regfile":
                child_inst = self.decode_regfile(child_json)
            elif t == "reg":
                child_inst = self.decode_reg(child_json)
            else:
                self.msg.fatal(
                    "Invalid child type '%s'" % t,
                    self.default_src_ref
                )
            self.add_child(comp_def, child_inst)

        inst = self.instantiate_regfile(
            comp_def,
            json_obj['inst_name'],
            json_obj['addr_offset']
        )
        return inst


    def decode_addrmap(self, json_obj: dict, is_top: bool=False) -> comp.Addrmap:
        # validate that this json object contains all the required fields
        if 'inst_name' not in json_obj:
            self.msg.fatal("JSON object is missing 'inst_name'", self.default_src_ref)
        if 'addr_offset' not in json_obj:
            self.msg.fatal("JSON object '%s' is missing 'addr_offset'" % json_obj['inst_name'], self.default_src_ref)
        if 'children' not in json_obj:
            self.msg.fatal("JSON object is missing 'children'", self.default_src_ref)

        if is_top:
            # if this is the top node, then instantiation is skipped, and the
            # definition inherits the inst name as its type name
            comp_def = self.create_addrmap_definition(json_obj['inst_name'])
        else:
            # otherwise, create an anonymous definition
            comp_def = self.create_addrmap_definition()

        # Collect children
        for child_json in json_obj['children']:
            # Lookup the child type and call the appropriate conversion function
            t = child_json.get('type', None)
            if t == "addrmap":
                child_inst = self.decode_addrmap(child_json)
            elif t == "regfile":
                child_inst = self.decode_regfile(child_json)
            elif t == "reg":
                child_inst = self.decode_reg(child_json)
            else:
                self.msg.fatal(
                    "Invalid child type '%s'" % t,
                    self.default_src_ref
                )

            # Add the child component to this
            self.add_child(comp_def, child_inst)

        if is_top:
            # keep top-level addrmap as a definition. Skip instantiation
            return comp_def

        # For everything else, convert the definition into an instance
        inst = self.instantiate_addrmap(
            comp_def,
            json_obj['inst_name'],
            json_obj['addr_offset']
        )
        return inst


#-------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import os

    from systemrdl import RDLCompiler, RDLCompileError, RDLWalker
    from systemrdl.messages import FileSourceRef

    # Create a compiler session, and an importer attached to it
    rdlc = RDLCompiler()
    json_importer = JSONImporter(rdlc)

    # import each JSON file provided from the command line
    input_files = sys.argv[1:]
    try:
        for input_file in input_files:
            # compile or import based on the file extension
            ext = os.path.splitext(input_file)[1]
            if ext == ".rdl":
                rdlc.compile_file(input_file)
            elif ext == ".json":
                json_importer.import_file(input_file)
            else:
                rdlc.msg.fatal(
                    "Unknown file extension: %s" % ext,
                    FileSourceRef(input_file)
                )
        # Elaborate when done
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    # Lets use the first example's listener to display the imported model
    from print_hierarchy import MyModelPrintingListener
    walker = RDLWalker()
    listener = MyModelPrintingListener()
    walker.walk(root, listener)
