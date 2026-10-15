import typing
import uuid

from sqlalchemy import select

import sqlalchemy
from uoishelpers.dataloaders.IDLoader import IDLoader

from src.DBDefinitions import CallModel
from src.ServiceDefinitions.BaseService import BaseService, ServiceExceptionWithCode
from src.ServiceDefinitions.ServiceContext import ServiceContext


class CallService(BaseService[IDLoader[CallModel]]):
    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[CallModel]:
        return ctx.loaders.CallModel