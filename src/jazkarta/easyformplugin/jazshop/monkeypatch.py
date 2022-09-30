from lxml import etree
from collective.easyform.migration.actions import TYPES_MAPPING as ACTIONS_TYPES_MAPPING
from collective.easyform.migration.actions import PROPERTIES_MAPPING as ACTIONS_PROPERTIES_MAPPING
from collective.easyform.migration.fields import append_field
from collective.easyform.migration.fields import Type
from collective.easyform.migration.fields import Property
from collective.easyform.migration.fields import append_node
from collective.easyform.migration.fields import TYPES_MAPPING as FIELDS_TYPES_MAPPING
from collective.easyform.migration.fields import PROPERTIES_MAPPING as FIELDS_PROPERTIES_MAPPING


def append_use_radio_node(field, name, value):
    node = etree.SubElement(field, name)
    if value == "select":
        node.text = "False"
    else:
        node.text = "True"
    return node


def patch_easyform():
    FIELDS_TYPES_MAPPING["JazShopSelectStringField"] = Type("JazShopProductSelect", append_field)
    FIELDS_TYPES_MAPPING["JazShopMultiSelectStringField"] = Type("JazShopProductMultiSelect", append_field)
    FIELDS_TYPES_MAPPING["JazShopArbitraryPriceStringField"] = Type("JazShopArbitraryPriceStringField", append_field)
    FIELDS_PROPERTIES_MAPPING["availableProducts"] = Property("available_products", append_node)
    FIELDS_PROPERTIES_MAPPING["selectionFormat"] = Property("use_radio", append_use_radio_node)
    ACTIONS_TYPES_MAPPING["JazShopCheckoutAdapter"] = Type("jazkarta.easyformplugin.jazshop.action.JazShopCheckout", append_field)
    ACTIONS_PROPERTIES_MAPPING["formIdExpression"] = Property("form_id_expression", append_node)
