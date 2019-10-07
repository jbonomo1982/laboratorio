import datetime
from haystack import indexes
from documentos.models import Categoria_doc


class Categoria_doc_indexes(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    descripcion = indexes.CharField(model_attr='descripcion')

    def get_model(self):
        return Categoria_doc
