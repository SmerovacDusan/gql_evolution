import datetime
import typing

import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension

from uoishelpers.resolvers import (
    DeleteError,
    InsertError,
    InputModelMixin,
    PageResolver,
    UpdateError,
    createInputs2,
)

from src.GraphTypeDefinitions.ApplicationInfo import ApplicationInfo
from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType


@createInputs2
class ProgramInputFilter:
    id: IDType
    provider_id: IDType
    name: str
    label: str
    description: str
    website: str


@strawberry.federation.type(
    description="Entity representing a Program",
    keys=["id"],
)
class ProgramGQLModel(BaseGQLModel):
    LoaderName = "ProgramModel"

    provider_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="ID of the provider publishing the program",
        permission_classes=[OnlyForAuthentized],
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Internal program name",
        permission_classes=[OnlyForAuthentized],
    )

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="Displayed program name",
        permission_classes=[OnlyForAuthentized],
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="Description of the program",
        permission_classes=[OnlyForAuthentized],
    )

    website: typing.Optional[str] = strawberry.field(
        default=None,
        description="Program website",
        permission_classes=[OnlyForAuthentized],
    )


@strawberry.interface(description="Program queries")
class ProgramQuery:
    program_by_id: typing.Optional[ProgramGQLModel] = strawberry.field(
        description="Get a program by ID",
        permission_classes=[OnlyForAuthentized],
        resolver=ProgramGQLModel.load_with_loader,
    )

    program_page: typing.List[ProgramGQLModel] = strawberry.field(
        description="Get a page of programs",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[ProgramGQLModel](
            whereType=ProgramInputFilter,
        ),
    )


@strawberry.input(description="Input type for creating a Program")
class ProgramInsertGQLModel(InputModelMixin):
    getLoader = ProgramGQLModel.getLoader

    provider_id: IDType = strawberry.field(
        description="Provider publishing the program",
    )

    name: str = strawberry.field(
        description="Internal program name",
    )

    label: str = strawberry.field(
        description="Displayed program name",
    )

    description: typing.Optional[str] = strawberry.field(
        description="Program description",
        default=None,
    )

    website: typing.Optional[str] = strawberry.field(
        description="Program website",
        default=None,
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="Program ID",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(description="Input type for updating a Program")
class ProgramUpdateGQLModel:
    id: IDType = strawberry.field(description="Program ID")

    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of the last change",
    )

    provider_id: typing.Optional[IDType] = strawberry.field(
        default=strawberry.UNSET,
        description="Provider publishing the program",
    )

    name: typing.Optional[str] = strawberry.field(
        default=strawberry.UNSET,
        description="Internal program name",
    )

    label: typing.Optional[str] = strawberry.field(
        default=strawberry.UNSET,
        description="Displayed program name",
    )

    description: typing.Optional[str] = strawberry.field(
        default=strawberry.UNSET,
        description="Program description",
    )

    website: typing.Optional[str] = strawberry.field(
        default=strawberry.UNSET,
        description="Program website",
    )

    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(description="Input type for deleting a Program")
class ProgramDeleteGQLModel:
    id: IDType = strawberry.field(description="Program ID")

    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of the last change",
    )


@strawberry.interface(description="Program mutations")
class ProgramMutation:

    @strawberry.mutation(
        description="Insert a Program",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[
                InsertError, ProgramGQLModel
            ](roles=["plánovací administrátor"]),
            UserRoleProviderExtension[InsertError, ProgramGQLModel](),
            RbacProviderExtension[InsertError, ProgramGQLModel](),
            LoadDataExtension[
                InsertError, ProgramGQLModel
            ](getLoader=ProgramGQLModel.getLoader),
        ],
    )
    async def program_insert(
        self,
        info: ApplicationInfo,
        program: ProgramInsertGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramGQLModel, InsertError[ProgramGQLModel]]:

        program.rbacobject_id = rbacobject_id

        service = info.ServiceCtx.Services.ProgramService

        return await service.ExecuteServiceMethod(
            service.Create(
                ctx=info.ServiceCtx,
                entity=program,
            ),
            Error=service.CreateErrorCallback(
                ErrorClass=InsertError[ProgramGQLModel],
                code="program_insert_error",
                location="program_insert",
                _input=program,
            ),
            OK=ProgramGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description="Update a Program",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[
                UpdateError, ProgramGQLModel
            ](roles=["plánovací administrátor"]),
            UserRoleProviderExtension[UpdateError, ProgramGQLModel](),
            RbacProviderExtension[UpdateError, ProgramGQLModel](),
            LoadDataExtension[UpdateError, ProgramGQLModel](),
        ],
    )
    async def program_update(
        self,
        info: ApplicationInfo,
        program: ProgramUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramGQLModel, UpdateError[ProgramGQLModel]]:

        service = info.ServiceCtx.Services.ProgramService

        return await service.ExecuteServiceMethod(
            service.Update(
                ctx=info.ServiceCtx,
                entity=program,
            ),
            Error=service.CreateErrorCallback(
                ErrorClass=UpdateError[ProgramGQLModel],
                code="program_update_error",
                location="program_update",
                _input=program,
                _entity=ProgramGQLModel.from_dataclass(db_row),
            ),
            OK=ProgramGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description="Delete a Program",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAccessControlExtension[
                DeleteError, ProgramGQLModel
            ](roles=["plánovací administrátor"]),
            UserRoleProviderExtension[DeleteError, ProgramGQLModel](),
            RbacProviderExtension[DeleteError, ProgramGQLModel](),
            LoadDataExtension[DeleteError, ProgramGQLModel](),
        ],
    )
    async def program_delete(
        self,
        info: ApplicationInfo,
        program: ProgramDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProgramGQLModel]]:

        service = info.ServiceCtx.Services.ProgramService

        return await service.ExecuteServiceMethod(
            service.Delete(
                ctx=info.ServiceCtx,
                entity=program,
            ),
            Error=service.CreateErrorCallback(
                ErrorClass=DeleteError[ProgramGQLModel],
                code="program_delete_error",
                location="program_delete",
                _input=program,
                _entity=ProgramGQLModel.from_dataclass(db_row),
            ),
            OK=lambda result: None,
        )