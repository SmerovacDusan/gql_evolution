from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader

import src.DBDefinitions
from src.DBDefinitions import BaseDBModel, EventModel, EventInvitationModel, ProgramModel, CallModel


class LoaderMap(LoaderMapBase[BaseDBModel]):
    BaseModel = BaseDBModel

    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    ProgramModel: IDLoader[src.DBDefinitions.ProgramModel] = None
    CallModel: IDLoader[src.DBDefinitions.CallModel] = None

    def __init__(self, session):
        super().__init__(session)
        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.ProgramModel = self.get(ProgramModel)
        self.CallModel = self.get(CallModel)

    def get_by_name(self, name: str):
        return getattr(self, name)


def createLoadersContext(session):
    """Compatibility helper for places expecting a dict context."""
    return {'loaders': LoaderMap(session)}
