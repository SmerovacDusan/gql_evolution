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

    @classmethod
    async def GetByProgram(cls, ctx: ServiceContext, program_id):
        # Vrátí všechny soutěže vyhlášené v rámci daného programu.
        loader = await cls.getLoader(ctx)
        return await loader.filter_by(program_id=program_id)