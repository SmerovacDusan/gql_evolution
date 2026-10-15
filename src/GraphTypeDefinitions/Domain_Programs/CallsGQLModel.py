import datetime
import typing

import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension

from uoishelpers.resolvers import (
    InputModelMixin,
    PageResolver,
    createInputs2,
)

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType


@createInputs2
class CallInputFilter:
    id: IDType
    program_id: IDType
    name: str
    label: str
    description: str
    announced: datetime.datetime
    submission_start: datetime.datetime
    submission_end: datetime.datetime
    evaluation_end: datetime.datetime
    website: str


@strawberry.federation.type(
    description="Entity representing a Call",
    keys=["id"]
)
class CallGQLModel(BaseGQLModel):
    LoaderName = "CallModel"

    program_id: IDType = strawberry.field(
        description="ID of the program this call belongs to",
        permission_classes=[OnlyForAuthentized]
    )

    name: str = strawberry.field(
        description="Internal name of the call",
        permission_classes=[OnlyForAuthentized]
    )

    label: str = strawberry.field(
        description="Displayed name of the call",
        permission_classes=[OnlyForAuthentized]
    )

    description: typing.Optional[str] = strawberry.field(
        description="Description of the call",
        permission_classes=[OnlyForAuthentized]
    )

    announced: typing.Optional[datetime.datetime] = strawberry.field(
        description="Date when the call was announced",
        permission_classes=[OnlyForAuthentized]
    )

    submission_start: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start of the submission period",
        permission_classes=[OnlyForAuthentized]
    )

    submission_end: typing.Optional[datetime.datetime] = strawberry.field(
        description="End of the submission period",
        permission_classes=[OnlyForAuthentized]
    )

    evaluation_end: typing.Optional[datetime.datetime] = strawberry.field(
        description="End of the evaluation period",
        permission_classes=[OnlyForAuthentized]
    )

    website: typing.Optional[str] = strawberry.field(
        description="Website of the call",
        permission_classes=[OnlyForAuthentized]
    )


@strawberry.interface(description="Call queries")
class CallQuery:

    call_by_id: typing.Optional[CallGQLModel] = strawberry.field(
        description="Get a call by ID",
        permission_classes=[OnlyForAuthentized],
        resolver=CallGQLModel.load_with_loader
    )

    call_page: typing.List[CallGQLModel] = strawberry.field(
        description="Get a page of calls",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[CallGQLModel](
            whereType=CallInputFilter
        )
    )


@strawberry.input(description="Input for creating a call")
class CallInsertGQLModel(InputModelMixin):

    getLoader = CallGQLModel.getLoader

    program_id: IDType
    name: str
    label: str

    description: typing.Optional[str] = None
    announced: typing.Optional[datetime.datetime] = None
    submission_start: typing.Optional[datetime.datetime] = None
    submission_end: typing.Optional[datetime.datetime] = None
    evaluation_end: typing.Optional[datetime.datetime] = None
    website: typing.Optional[str] = None

    id: typing.Optional[IDType] = None

    createdby_id: typing.Optional[IDType] = strawberry.private(
        default=None
    )

    rbacobject_id: typing.Optional[IDType] = strawberry.private(
        default=None
    )


@strawberry.input(description="Input for updating a call")
class CallUpdateGQLModel:

    id: IDType
    lastchange: typing.Optional[datetime.datetime] = None

    program_id: typing.Optional[IDType] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    label: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    announced: typing.Optional[datetime.datetime] = strawberry.UNSET
    submission_start: typing.Optional[datetime.datetime] = strawberry.UNSET
    submission_end: typing.Optional[datetime.datetime] = strawberry.UNSET
    evaluation_end: typing.Optional[datetime.datetime] = strawberry.UNSET
    website: typing.Optional[str] = strawberry.UNSET

    changedby_id: typing.Optional[IDType] = strawberry.private(
        default=None
    )


@strawberry.input(description="Input for deleting a call")
class CallDeleteGQLModel:

    id: IDType
    lastchange: typing.Optional[datetime.datetime] = None


@strawberry.interface(description="Call mutations")
class CallMutation:

    @strawberry.mutation(
        description="Create a call",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[CallInsertGQLModel](
                roles=["plánovací administrátor"]
            ),
            UserRoleProviderExtension[CallInsertGQLModel](),
            RbacProviderExtension[CallInsertGQLModel](),
            LoadDataExtension[CallInsertGQLModel](
                getLoader=CallGQLModel.getLoader,
                primary_key_name="program_id"
            )
        ]
    )
    async def call_insert(
        self,
        info: strawberry.Info,
        call: CallInsertGQLModel
    ) -> typing.Optional[CallGQLModel]:

        service = info.ServiceCtx.Services.CallService

        return await service.ExecuteServiceMethod(
            service.Create(
                ctx=info.ServiceCtx,
                entity=call
            ),
            Error=service.CreateErrorCallback("call_insert_error"),
            OK=CallGQLModel.from_dataclass
        )

    @strawberry.mutation(
        description="Update a call",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[CallUpdateGQLModel](
                roles=["plánovací administrátor"]
            ),
            UserRoleProviderExtension[CallUpdateGQLModel](),
            LoadDataExtension[CallUpdateGQLModel]()
        ]
    )
    async def call_update(
        self,
        info: strawberry.Info,
        call: CallUpdateGQLModel
    ) -> typing.Optional[CallGQLModel]:

        service = info.ServiceCtx.Services.CallService

        return await service.ExecuteServiceMethod(
            service.Update(
                ctx=info.ServiceCtx,
                entity=call
            ),
            Error=service.CreateErrorCallback("call_update_error"),
            OK=CallGQLModel.from_dataclass
        )

    @strawberry.mutation(
        description="Delete a call",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[CallDeleteGQLModel](
                roles=["plánovací administrátor"]
            ),
            UserRoleProviderExtension[CallDeleteGQLModel](),
            LoadDataExtension[CallDeleteGQLModel]()
        ]
    )
    async def call_delete(
        self,
        info: strawberry.Info,
        call: CallDeleteGQLModel
    ) -> typing.Optional[CallGQLModel]:

        service = info.ServiceCtx.Services.CallService

        return await service.ExecuteServiceMethod(
            service.Delete(
                ctx=info.ServiceCtx,
                entity=call
            ),
            Error=service.CreateErrorCallback("call_delete_error"),
            OK=CallGQLModel.from_dataclass
        )