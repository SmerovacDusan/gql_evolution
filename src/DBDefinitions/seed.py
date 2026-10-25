from __future__ import annotations

import datetime
import os
import uuid

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy import select

from uoishelpers.dataloaders import readJsonFile
from uoishelpers.feeders import ImportModels

from src.DBDefinitions import BaseDBModel
from src.DBDefinitions.Domain_Programs.CallModel import CallModel


DEFAULT_EVENT_TYPES = (
    {
        'id': uuid.UUID('11111111-1111-1111-1111-111111111111'),
        'name': 'Událost',
        'name_en': 'Event',
    },
    {
        'id': uuid.UUID('22222222-2222-2222-2222-222222222222'),
        'name': 'Schůzka',
        'name_en': 'Meeting',
    },
)
DATETIME_FIELDS = {
    "created",
    "lastchange",
    "announced",
    "submission_start",
    "submission_end",
    "evaluation_end",
}

def is_sqlalchemy_model(cls: type) -> bool:
    """Return True only for SQLAlchemy mapped model classes."""
    try:
        mapper = sa_inspect(cls, raiseerr=False)
        return mapper is not None
    except NoInspectionAvailable:
        return False


def convert_datetime_values(value):
    """Convert ISO-formatted datetime strings in JSON data."""
    if isinstance(value, dict):
        result = {}

        for key, item in value.items():
            if key in DATETIME_FIELDS and isinstance(item, str):
                parsed = datetime.datetime.fromisoformat(
                    item.replace("Z", "+00:00")
                )

                # Model používá TIMESTAMP WITHOUT TIME ZONE.
                if parsed.tzinfo is not None:
                    parsed = parsed.astimezone(
                        datetime.timezone.utc
                    ).replace(tzinfo=None)

                result[key] = parsed
            else:
                result[key] = convert_datetime_values(item)

        return result

    if isinstance(value, list):
        return [convert_datetime_values(item) for item in value]

    return value

    
get_demodata = lambda :readJsonFile(jsonFileName="./systemdata.json")

async def init_database_data(session_maker, get_demodata=get_demodata) -> None:
    """Idempotent seed hook for application startup.

    Keep this function small and explicit. It is called once from
    DatabaseRuntime.start(), after metadata.create_all().
    """

    json_data = convert_datetime_values(get_demodata())
    print("DATA PO NAČTENÍ A KONVERZI:")
    print(json_data)

    Models = [
        mapper.class_
        for mapper in BaseDBModel.registry.mappers
        if is_sqlalchemy_model(mapper.class_)
    ]

    ModelNames = [Model.__name__ for Model in Models]

    TypeNames = [
        Model.__name__
        for Model in Models
        if Model.__name__.endswith("TypeModel")
    ]

    isDemo = True  # os.environ.get("DEMODATA", None) in ["True", "true", True]

    ModelNamesToImport = ModelNames if isDemo else TypeNames

    print(
        f"Importing models: (isDemo = {isDemo})\n{ModelNamesToImport}",
        flush=True,
    )

    ModelsToImport = [
        Model
        for Model in Models
        if Model.__name__ in ModelNamesToImport
        and is_sqlalchemy_model(Model)
        and hasattr(Model, "__tablename__")
    ]
    table_names = [Model.__tablename__ for Model in ModelsToImport]
    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in ModelsToImport)
    print(f"Models to import: {ModelsToImport}\nTable names: {table_names}\nModel index: {modelIndex}", flush=True)

    #@asynccontextmanager
    #async def session_maker():
     #   try:
#
 #           yield session
  #      finally:
   #         pass


    await ImportModels(session_maker, ModelsToImport, json_data)

    print("Data initialized", flush=True)

