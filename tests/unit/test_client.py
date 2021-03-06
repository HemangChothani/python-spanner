# Copyright 2016 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import mock


def _make_credentials():
    import google.auth.credentials

    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class TestClient(unittest.TestCase):

    PROJECT = "PROJECT"
    PATH = "projects/%s" % (PROJECT,)
    CONFIGURATION_NAME = "config-name"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "%s/instances/%s" % (PATH, INSTANCE_ID)
    DISPLAY_NAME = "display-name"
    NODE_COUNT = 5
    TIMEOUT_SECONDS = 80
    USER_AGENT = "you-sir-age-int"

    def _get_target_class(self):
        from google.cloud import spanner

        return spanner.Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _constructor_test_helper(
        self,
        expected_scopes,
        creds,
        expected_creds=None,
        client_info=None,
        user_agent=None,
        client_options=None,
    ):
        import google.api_core.client_options
        from google.cloud.spanner_v1 import client as MUT

        kwargs = {}

        if client_info is not None:
            kwargs["client_info"] = expected_client_info = client_info
        else:
            expected_client_info = MUT._CLIENT_INFO

        kwargs["client_options"] = client_options
        if type(client_options) == dict:
            expected_client_options = google.api_core.client_options.from_dict(
                client_options
            )
        else:
            expected_client_options = client_options

        client = self._make_one(
            project=self.PROJECT, credentials=creds, user_agent=user_agent, **kwargs
        )

        expected_creds = expected_creds or creds.with_scopes.return_value
        self.assertIs(client._credentials, expected_creds)

        self.assertIs(client._credentials, expected_creds)
        if expected_scopes is not None:
            creds.with_scopes.assert_called_once_with(expected_scopes)

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(client._client_info, expected_client_info)
        self.assertEqual(client.user_agent, user_agent)
        if expected_client_options is not None:
            self.assertIsInstance(
                client._client_options, google.api_core.client_options.ClientOptions
            )
            self.assertEqual(
                client._client_options.api_endpoint,
                expected_client_options.api_endpoint,
            )

    def test_constructor_default_scopes(self):
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds)

    @mock.patch("warnings.warn")
    def test_constructor_custom_user_agent_and_timeout(self, mock_warn):
        from google.cloud.spanner_v1 import client as MUT

        CUSTOM_USER_AGENT = "custom-application"
        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(
            expected_scopes, creds, user_agent=CUSTOM_USER_AGENT
        )
        mock_warn.assert_called_once_with(
            MUT._USER_AGENT_DEPRECATED, DeprecationWarning, stacklevel=2
        )

    def test_constructor_custom_client_info(self):
        from google.cloud.spanner_v1 import client as MUT

        client_info = mock.Mock()
        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds, client_info=client_info)

    def test_constructor_implicit_credentials(self):
        creds = _make_credentials()

        patch = mock.patch("google.auth.default", return_value=(creds, None))
        with patch as default:
            self._constructor_test_helper(
                None, None, expected_creds=creds.with_scopes.return_value
            )

        default.assert_called_once_with()

    def test_constructor_credentials_wo_create_scoped(self):
        creds = _make_credentials()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_client_options_obj(self):
        from google.api_core.client_options import ClientOptions
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(
            expected_scopes,
            creds,
            client_options=ClientOptions(api_endpoint="endpoint"),
        )

    def test_constructor_custom_client_options_dict(self):
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(
            expected_scopes, creds, client_options={"api_endpoint": "endpoint"}
        )

    def test_instance_admin_api(self):
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE

        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = mock.Mock()
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        inst_module = "google.cloud.spanner_v1.client.InstanceAdminClient"
        with mock.patch(inst_module) as instance_admin_client:
            api = client.instance_admin_api

        self.assertIs(api, instance_admin_client.return_value)

        # API instance is cached
        again = client.instance_admin_api
        self.assertIs(again, api)

        instance_admin_client.assert_called_once_with(
            credentials=credentials.with_scopes.return_value,
            client_info=client_info,
            client_options=client_options,
        )

        credentials.with_scopes.assert_called_once_with(expected_scopes)

    def test_database_admin_api(self):
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE

        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = mock.Mock()
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        db_module = "google.cloud.spanner_v1.client.DatabaseAdminClient"
        with mock.patch(db_module) as database_admin_client:
            api = client.database_admin_api

        self.assertIs(api, database_admin_client.return_value)

        # API instance is cached
        again = client.database_admin_api
        self.assertIs(again, api)

        database_admin_client.assert_called_once_with(
            credentials=credentials.with_scopes.return_value,
            client_info=client_info,
            client_options=client_options,
        )

        credentials.with_scopes.assert_called_once_with(expected_scopes)

    def test_copy(self):
        credentials = _make_credentials()
        # Make sure it "already" is scoped.
        credentials.requires_scopes = False

        client = self._make_one(project=self.PROJECT, credentials=credentials)

        new_client = client.copy()
        self.assertIs(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)

    def test_credentials_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertIs(client.credentials, credentials.with_scopes.return_value)

    def test_project_name_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        project_name = "projects/" + self.PROJECT
        self.assertEqual(client.project_name, project_name)

    def test_list_instance_configs(self):
        from google.cloud.spanner_admin_instance_v1.gapic import instance_admin_client
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2,
        )
        from google.cloud.spanner_v1.client import InstanceConfig

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = spanner_instance_admin_pb2.ListInstanceConfigsResponse(
            instance_configs=[
                spanner_instance_admin_pb2.InstanceConfig(
                    name=self.CONFIGURATION_NAME, display_name=self.DISPLAY_NAME
                )
            ]
        )

        lic_api = api._inner_api_calls["list_instance_configs"] = mock.Mock(
            return_value=instance_config_pbs
        )

        response = client.list_instance_configs()
        instance_configs = list(response)

        instance_config = instance_configs[0]
        self.assertIsInstance(instance_config, InstanceConfig)
        self.assertEqual(instance_config.name, self.CONFIGURATION_NAME)
        self.assertEqual(instance_config.display_name, self.DISPLAY_NAME)

        expected_metadata = [
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        ]
        lic_api.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstanceConfigsRequest(parent=self.PATH),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_list_instance_configs_w_options(self):
        from google.cloud.spanner_admin_instance_v1.gapic import instance_admin_client
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2,
        )

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = spanner_instance_admin_pb2.ListInstanceConfigsResponse(
            instance_configs=[
                spanner_instance_admin_pb2.InstanceConfig(
                    name=self.CONFIGURATION_NAME, display_name=self.DISPLAY_NAME
                )
            ]
        )

        lic_api = api._inner_api_calls["list_instance_configs"] = mock.Mock(
            return_value=instance_config_pbs
        )

        token = "token"
        page_size = 42
        list(client.list_instance_configs(page_token=token, page_size=42))

        expected_metadata = [
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        ]
        lic_api.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstanceConfigsRequest(
                parent=self.PATH, page_size=page_size, page_token=token
            ),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_instance_factory_defaults(self):
        from google.cloud.spanner_v1.instance import DEFAULT_NODE_COUNT
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIsNone(instance.configuration_name)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertIs(instance._client, client)

    def test_instance_factory_explicit(self):
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(
            self.INSTANCE_ID,
            self.CONFIGURATION_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
        )

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertIs(instance._client, client)

    def test_list_instances(self):
        from google.cloud.spanner_admin_instance_v1.gapic import instance_admin_client
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2,
        )
        from google.cloud.spanner_v1.client import Instance

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = spanner_instance_admin_pb2.ListInstancesResponse(
            instances=[
                spanner_instance_admin_pb2.Instance(
                    name=self.INSTANCE_NAME,
                    config=self.CONFIGURATION_NAME,
                    display_name=self.DISPLAY_NAME,
                    node_count=self.NODE_COUNT,
                )
            ]
        )

        li_api = api._inner_api_calls["list_instances"] = mock.Mock(
            return_value=instance_pbs
        )

        response = client.list_instances()
        instances = list(response)

        instance = instances[0]
        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)

        expected_metadata = [
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        ]
        li_api.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstancesRequest(parent=self.PATH),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_list_instances_w_options(self):
        from google.cloud.spanner_admin_instance_v1.gapic import instance_admin_client
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2,
        )

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = spanner_instance_admin_pb2.ListInstancesResponse(instances=[])

        li_api = api._inner_api_calls["list_instances"] = mock.Mock(
            return_value=instance_pbs
        )

        token = "token"
        page_size = 42
        list(client.list_instances(page_token=token, page_size=42))

        expected_metadata = [
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        ]
        li_api.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstancesRequest(
                parent=self.PATH, page_size=page_size, page_token=token
            ),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )
