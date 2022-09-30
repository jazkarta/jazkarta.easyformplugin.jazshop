from lxml import etree
from collective.easyform.migration.actions import PROPERTIES_MAPPING as ACTIONS_PROPERTIES_MAPPING
from collective.easyform.migration.actions import TYPES_MAPPING as ACTIONS_TYPES_MAPPING
from collective.easyform.migration.fields import append_field
from collective.easyform.migration.fields import append_node
from collective.easyform.migration.fields import PROPERTIES_MAPPING as FIELDS_PROPERTIES_MAPPING
from collective.easyform.migration.fields import Property
from collective.easyform.migration.fields import Type
from collective.easyform.migration.fields import TYPES_MAPPING as FIELDS_TYPES_MAPPING
from collective.easyform.migration.pfg import Field
from collective.easyform.migration.pfg import FIELD_MAPPING as PFG_FIELD_MAPPING


def append_use_radio_node(field, name, value):
    node = etree.SubElement(field, name)
    if value == "select":
        node.text = "False"
    else:
        node.text = "True"
    return node


def migrate_thanksPageOverride_field(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate the thanksPageOverride field of a PFG form.

    Splits the value into the two fields `thanksPageOverride` and `thanksPageOverrideAction`
    to conform to easyform's data model.
    """
    field = src_obj.getField(src_fieldname)
    if field:
        at_value = field.get(src_obj)
    else:
        at_value = getattr(src_obj, src_fieldname, None)
        if at_value and hasattr(at_value, '__call__'):
            at_value = at_value()
    if at_value:
        dst_obj.thanksPageOverrideAction, dst_obj.thanksPageOverride = at_value.split(":", 1)


def patch_easyform():
    FIELDS_TYPES_MAPPING["JazShopSelectStringField"] = Type("jazkarta.easyformplugin.jazshop.fields.JazShopProductSelect", append_field)
    FIELDS_TYPES_MAPPING["JazShopMultiSelectStringField"] = Type("jazkarta.easyformplugin.jazshop.fields.JazShopProductMultiSelect", append_field)
    FIELDS_TYPES_MAPPING["JazShopArbitraryPriceStringField"] = Type("jazkarta.easyformplugin.jazshop.fields.JazShopArbitraryPriceStringField", append_field)
    FIELDS_PROPERTIES_MAPPING["availableProducts"] = Property("available_products", append_node)
    FIELDS_PROPERTIES_MAPPING["selectionFormat"] = Property("use_radio", append_use_radio_node)
    ACTIONS_TYPES_MAPPING["JazShopCheckoutAdapter"] = Type("jazkarta.easyformplugin.jazshop.action.JazShopCheckout", append_field)
    ACTIONS_PROPERTIES_MAPPING["formIdExpression"] = Property("form_id_expression", append_node)
    PFG_FIELD_MAPPING["thanksPageOverride"] = Field("thanksPageOverride", migrate_thanksPageOverride_field)
