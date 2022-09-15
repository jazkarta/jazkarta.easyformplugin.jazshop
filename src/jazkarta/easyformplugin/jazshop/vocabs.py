from jazkarta.shop.interfaces import IProduct
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def get_available_products_vocab(context):
    terms = []
    products = context.portal_catalog(
        object_provides=IProduct.__identifier__,
        sort_on='sortable_title',
        sort_order='ascending')
    for product in products:
        terms.append(SimpleTerm(
            value=product.UID,
            token=product.UID,
            title=product.Title,
        ))
    return SimpleVocabulary(terms)
directlyProvides(get_available_products_vocab, IVocabularyFactory)


def get_selected_products(context, value):
    selected = []
    products = context.portal_catalog(
        object_provides=IProduct.__identifier__,
        sort_on='sortable_title',
        sort_order='ascending')
    product_dict = {product.UID: ("{}|{}".format(product.Title, product.UID), "$" + str(product.getObject().price) + ' - ' + product.Title) for product in products}
    for product in value:
        if product in product_dict:
            selected.append(product_dict[product])
    selected = sorted(selected, key=lambda(x): float(x[1].split()[0][1:]))
    if context.portal_type == 'JazShopSelectStringField' and context.fgDefault:
        selected.insert(0, ('{}|0'.format(context.fgDefault), context.fgDefault))
    return selected
