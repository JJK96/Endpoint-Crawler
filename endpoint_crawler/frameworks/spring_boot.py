from .base import BaseCrawler, Endpoint, Parameter
from ..util import Url
from javalang.parse import parse
from javalang.tree import ElementValuePair, ElementArrayValue

class SpringBootCrawler(BaseCrawler):
    filetypes = ["java"]
    mappings = ["GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping"]
    variable_annotations = ["RequestBody", "PathVariable", "RequestParam"]

    def get_annotation_value(self, annotation):
        if isinstance(annotation.element, list):
            for e in annotation.element: 
                if isinstance(e, ElementValuePair) and e.name == "value":
                    return e.value.values[0].value.strip('"')
        elif isinstance(annotation.element, ElementArrayValue):
                return annotation.element.values[0].value.strip('"')
        return None

    def get_parameter_type(self, parameter):
        parameter_type = []
        for parameter_annotation in parameter.annotations:
            if parameter_annotation.name not in self.variable_annotations:
                continue
            parameter_type.append("@" + parameter_annotation.name)
        if not parameter_type:
            return None
        parameter_type.append(parameter.type.name)
        return " ".join(parameter_type)

    def find_endpoints_file(self, file):
        with open(file) as f:
            tree = parse(f.read())
        for c in tree.types:
            base = Url("")
            for annotation in c.annotations:
                if annotation.name == "RequestMapping":
                    base = Url(annotation.element.values[0].value.strip('"'))
                    break
            for method in c.methods:
                for annotation in method.annotations:
                    if annotation.name in self.mappings:
                        value = self.get_annotation_value(annotation)
                        parameters = []
                        for parameter in method.parameters:
                            parameter_type = self.get_parameter_type(parameter)
                            if not parameter_type:
                                continue
                            parameters.append(Parameter(parameter.name, parameter_type))

                        if value is None:
                            path = base
                        else:
                            path = base / value
                        request_type = annotation.name.replace("Mapping", "")
                        yield Endpoint(request_type, path, file, parameters)
