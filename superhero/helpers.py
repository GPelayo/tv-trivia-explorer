import inspect
import sys
from typing import Generator, List

from django.db.models import Model
from django.db.models.query_utils import DeferredAttribute

from superhero import models


def get_all_models() -> Generator[Model, None, None]:
    for model in sys.modules['superhero.models'].__dict__.values():
        if inspect.isclass(model) and issubclass(model, Model):
            yield model


def get_fields_from_model_name(model_name: str) -> List[DeferredAttribute]:
    return [n for n, field in getattr(models, model_name).__dict__.items() if isinstance(field, DeferredAttribute)]
