from dataclasses import dataclass
from enum import Enum

from tortoise import fields
from tortoise.models import Model


class Site(Model):
    id = fields.IntField(pk=True)
    masked_url = fields.CharField(max_length=255, unique=True)
    url = fields.CharField(max_length=255, unique=True)
    is_extracted = fields.BooleanField(default=False)
    has_rc_analysis = fields.BooleanField(default=False)
    rc_analysis = fields.TextField()
    has_sentiment_analysis = fields.BooleanField(default=False)
    sentiment_analysis = fields.TextField()
    has_prominent_analysis = fields.BooleanField(default=False)
    prominent_analysis = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Status(Enum):
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ResponseJSON:
    status: Status
    message: str
