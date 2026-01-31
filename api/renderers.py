"""
Custom renderers for the API application.
Provides support for various output formats, such as XML, to meet diverse client requirements.
"""
from rest_framework.renderers import BaseRenderer
import xml.etree.ElementTree as ET

class MiniXMLRenderer(BaseRenderer):
    """
    A minimal XML renderer for DRF.
    """
    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the provided data into XML format.
        """
        root = ET.Element('root')
        if isinstance(data, list):
            for item in data:
                article = ET.SubElement(root, 'article')
                self._dict_to_xml(article, item)
        elif isinstance(data, dict):
            self._dict_to_xml(root, data)
        
        return ET.tostring(root, encoding='utf-8')

    def _dict_to_xml(self, parent, data):
        """
        Recursively convert a dictionary to XML elements.
        """
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            child.text = str(value) if value is not None else ""
