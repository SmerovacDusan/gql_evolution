import typing
import uuid

from sqlalchemy import select

import sqlalchemy
from uoishelpers.dataloaders.IDLoader import IDLoader

from src.DBDefinitions import ProgramModel
from src.ServiceDefinitions.BaseService import BaseService, ServiceExceptionWithCode
from src.ServiceDefinitions.ServiceContext import ServiceContext


class ProgramService(BaseService[IDLoader[ProgramModel]]):
    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[ProgramModel]:
        return ctx.loaders.ProgramModel