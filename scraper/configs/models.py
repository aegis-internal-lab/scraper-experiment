from dataclasses import dataclass
from email.policy import default
from enum import Enum

from tortoise import fields
from tortoise.models import Model


class Site(Model):
    id = fields.IntField(pk=True)
    title= fields.TextField(null=True)
    content= fields.TextField(null=True)
    masked_url = fields.CharField(max_length=500)
    url = fields.CharField(max_length=500, unique=True)
    is_extracted = fields.BooleanField(default=False)
    has_rc_analysis = fields.BooleanField(default=False)
    rc_analysis = fields.TextField(null=True)
    has_sentiment_analysis = fields.BooleanField(default=False)
    sentiment_analysis = fields.TextField(null=True)
    has_prominent_analysis = fields.BooleanField(default=False)
    prominent_analysis = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Status(Enum):
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ResponseJSON:
    status: Status
    message: str

@dataclass
class ResponseContent:
    content: str
    title: str