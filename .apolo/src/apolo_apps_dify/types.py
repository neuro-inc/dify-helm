from pydantic import BaseModel, ConfigDict, Field

from apolo_app_types.protocols.common import (
    AbstractAppFieldType,
    AppInputs,
    AppInputsDeployer,
    AppOutputsDeployer,
    IngressHttp,
    Postgres,
    Preset,
    Redis,
    SchemaExtraMetadata,
    SchemaMetaType,
)
from apolo_app_types.protocols.dify import DifyAppOutputs
from apolo_app_types.protocols.postgres import CrunchyPostgresUserCredentials


class DifyApi(AbstractAppFieldType):
    replicas: int = Field(default=1, gt=0)
    preset_name: str
    title: str


class DifyWorker(AbstractAppFieldType):
    replicas: int = Field(default=1, gt=0)
    preset_name: str


class DifyProxy(AbstractAppFieldType):
    preset_name: str


class DifyWeb(AbstractAppFieldType):
    replicas: int | None = Field(default=None, gt=0)
    preset_name: str


class DifyInputs(AppInputsDeployer):
    api: DifyApi
    worker: DifyWorker
    proxy: DifyProxy
    web: DifyWeb
    redis: Redis
    externalPostgres: Postgres  # noqa: N815
    externalPGVector: Postgres  # noqa: N815


class DifyOutputs(AppOutputsDeployer):
    internal_web_app_url: str
    internal_api_url: str
    external_api_url: str | None
    init_password: str


class DifyAppApi(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Dify API",
            description="Configure Dify Api.",
        ).as_json_schema_extra(),
    )
    replicas: int = Field(
        default=1,
        gt=0,
        json_schema_extra=SchemaExtraMetadata(
            title="Replicas Count",
            description="Configure Replicas count.",
        ).as_json_schema_extra(),
    )
    preset: Preset = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Dify API Preset",
            description="Specify preset configuration for Dify API. "
            "Minimal resources: 0.1 CPU cores, 256 MiB memory.",
        ).as_json_schema_extra(),
    )


class DifyAppWorker(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Worker",
            description="Configure Dify Worker.",
        ).as_json_schema_extra(),
    )
    replicas: int = Field(
        default=1,
        gt=0,
        json_schema_extra=SchemaExtraMetadata(
            title="Replicas Count",
            description="Configure Replicas count.",
        ).as_json_schema_extra(),
    )
    preset: Preset = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Worker Preset",
            description="Specify preset configuration for Dify Worker. "
            "Minimal resources: 1 CPU cores, 2 GiB memory.",
        ).as_json_schema_extra(),
    )


class DifyAppProxy(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Proxy",
            description="Configure Dify Proxy.",
        ).as_json_schema_extra(),
    )
    preset: Preset = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Proxy Preset",
            description="Specify preset configuration for Dify Proxy. "
            "Minimal resources: 0.5 CPU cores, 512 MiB memory.",
        ).as_json_schema_extra(),
    )


class DifyAppWeb(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Web",
            description="Configure Dify Web.",
        ).as_json_schema_extra(),
    )
    replicas: int = Field(
        default=1,
        gt=0,
        json_schema_extra=SchemaExtraMetadata(
            title="Replicas Count",
            description="Configure Replicas count.",
        ).as_json_schema_extra(),
    )
    preset: Preset = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Web Preset",
            description="Specify preset configuration for Dify Web. "
            "Minimal resources: 0.5 CPU cores, 256 MiB memory.",
        ).as_json_schema_extra(),
    )


class DifyAppRedis(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Dify Redis",
            description="Configure Dify Redis.",
        ).as_json_schema_extra(),
    )
    master_preset: Preset = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Master Preset",
            description="Configure Master Preset.",
        ).as_json_schema_extra(),
    )


class DifyAppInputs(AppInputs):
    api: DifyAppApi
    worker: DifyAppWorker
    proxy: DifyAppProxy
    web: DifyAppWeb
    redis: DifyAppRedis
    # bucket: Bucket = Field(
    #     ...,
    #     json_schema_extra=SchemaExtraMetadata(
    #         title="Bucket",
    #         description="Configure Dify Blob Storage (Bucket).",
    #     ).as_json_schema_extra(),
    # )
    external_postgres: CrunchyPostgresUserCredentials = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="Postgres Credentials",
            description="Main Postgres instance credentials",
            meta_type=SchemaMetaType.INTEGRATION,
        ).as_json_schema_extra(),
    )
    external_pgvector: CrunchyPostgresUserCredentials = Field(
        ...,
        json_schema_extra=SchemaExtraMetadata(
            title="PGVector Credentials",
            description="PGVector instance credentials for vector embeddings storage",
            meta_type=SchemaMetaType.INTEGRATION,
        ).as_json_schema_extra(),
    )
    ingress_http: IngressHttp | None = Field(
        default_factory=lambda: IngressHttp(),
        json_schema_extra=SchemaExtraMetadata(
            title="HTTP Ingress",
            description="Define HTTP ingress configuration"
            " for exposing services over the web.",
        ).as_json_schema_extra(),
    )


__all__ = [
    "DifyAppInputs",
    "DifyAppOutputs",
]
