from unittest.mock import AsyncMock, patch

import apolo_sdk
from apolo_app_types_fixtures.constants import (
    APP_ID,
    APP_SECRETS_NAME,
    DEFAULT_NAMESPACE,
    DEFAULT_POSTGRES_CREDS,
)
from apolo_apps_dify.inputs_processor import DifyInputsProcessor
from apolo_apps_dify.types import (
    DifyAppApi,
    DifyAppInputs,
    DifyAppProxy,
    DifyAppRedis,
    DifyAppWeb,
    DifyAppWorker,
)

from apolo_app_types.protocols.common import ApoloSecret, IngressHttp, Preset


async def test_dify_values_generation(setup_clients):
    with patch(
        "apolo_apps_dify.inputs_processor.get_or_create_bucket_credentials",
        new_callable=AsyncMock,
    ) as mock_fetch:
        mock_fetch.return_value = apolo_sdk.PersistentBucketCredentials(
            id="cred-id",
            owner="owner",
            cluster_name="cluster",
            name="test-creds",
            read_only=True,
            credentials=[
                apolo_sdk.BucketCredentials(
                    bucket_id="bucket-id",
                    provider=apolo_sdk.Bucket.Provider.AWS,
                    credentials={
                        "bucket_name": "test-bucket",
                        "endpoint_url": "https://s3.amazonaws.com",
                        "access_key_id": "test-access-key",
                        "secret_access_key": "test-secret-key",
                    },
                )
            ],
        )

        # Create the processor instance with the client
        processor = DifyInputsProcessor(client=setup_clients)

        # Call gen_extra_values directly
        helm_params = await processor.gen_extra_values(
            input_=DifyAppInputs(
                ingress_http=IngressHttp(
                    clusterName="test",
                ),
                api=DifyAppApi(preset=Preset(name="cpu-small")),
                worker=DifyAppWorker(preset=Preset(name="cpu-small")),
                proxy=DifyAppProxy(preset=Preset(name="cpu-small")),
                web=DifyAppWeb(preset=Preset(name="cpu-small")),
                redis=DifyAppRedis(master_preset=Preset(name="cpu-small")),
                external_postgres=DEFAULT_POSTGRES_CREDS,
                external_pgvector=DEFAULT_POSTGRES_CREDS,
            ),
            app_name="dify-app-with-long-name-that-should-be-truncated",
            namespace=DEFAULT_NAMESPACE,
            app_secrets_name=APP_SECRETS_NAME,
            app_id=APP_ID,
        )
        assert helm_params["api"]["podLabels"] == {
            "platform.apolo.us/component": "api",
            "platform.apolo.us/preset": "cpu-small",
        }
        assert helm_params["worker"]["podLabels"] == {
            "platform.apolo.us/component": "worker",
            "platform.apolo.us/preset": "cpu-small",
        }
        assert helm_params["proxy"]["podLabels"] == {
            "platform.apolo.us/component": "proxy",
            "platform.apolo.us/preset": "cpu-small",
        }
        assert helm_params["web"]["podLabels"] == {
            "platform.apolo.us/component": "web",
            "platform.apolo.us/preset": "cpu-small",
        }
        assert helm_params["redis"]["master"]["podLabels"] == {
            "platform.apolo.us/component": "redis_master",
            "platform.apolo.us/preset": "cpu-small",
        }
        assert helm_params["externalPostgres"] == {
            "username": "pgvector_user",
            "password": ApoloSecret(key="pgvector_password"),
            "address": "pgbouncer_host",
            "port": 4321,
            "dbName": "db_name",
        }
        assert helm_params["externalPgvector"] == {
            "username": "pgvector_user",
            "password": ApoloSecret(key="pgvector_password"),
            "address": "pgbouncer_host",
            "port": 4321,
            "dbName": "db_name",
        }
        assert helm_params["redis"]["auth"]["password"]
        assert helm_params["redis"]["architecture"] == "standalone"
        assert helm_params["api"]["secretKey"]
        assert helm_params["api"]["initPassword"]

        # Verify Dify gets ONLY auth middleware (no strip headers)
        assert (
            helm_params["ingress"]["annotations"][
                "traefik.ingress.kubernetes.io/router.middlewares"
            ]
            == "platform-platform-control-plane-ingress-auth@kubernetescrd"
        )

        assert helm_params["externalS3"] == {
            "enabled": True,
            "endpoint": "https://s3.amazonaws.com",
            "accessKey": "test-access-key",
            "secretKey": "test-secret-key",
            "bucketName": "test-bucket",
        }
        assert mock_fetch.call_args[1]["bucket_name"] == f"app-dify-{APP_ID}"[:40]
