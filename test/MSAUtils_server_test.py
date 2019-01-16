# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
import unittest
from configparser import ConfigParser

from MSAUtils.authclient import KBaseAuth as _KBaseAuth
from MSAUtils.MSAUtilsImpl import MSAUtils
from MSAUtils.MSAUtilsServer import MethodContext
from installed_clients.WorkspaceClient import Workspace


class MSAUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MSAUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'MSAUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = MSAUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

        test_file = "MSA.fasta"
        cls.fasta_file_path = os.path.join(cls.scratch, test_file)
        shutil.copy(os.path.join('data', test_file), cls.fasta_file_path)

        file_path = 'data/MSA.json'
        data = json.load(open(file_path))
        info = cls.wsClient.save_objects({
            'workspace': cls.wsName,
            'objects': [
                {'type': 'KBaseTrees.MSA',
                 'name': os.path.splitext(os.path.basename(file_path))[0],
                 'data': data}]
        })[0]
        cls.msa_ref = f"{info[6]}/{info[0]}/{info[4]}"

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def test_import_msa_fasta(self):
        ret = self.serviceImpl.import_msa_file(self.ctx, {'workspace_name': self.wsName,
                                                          'input_file_path': self.fasta_file_path,
                                                          'msa_name': 'test_msa',
                                                          'description': 'Foo!'})

    def test_msa_to_fasta(self):
        ret = self.serviceImpl.msa_to_fasta_file(self.ctx, {'destination_dir': "./",
                                                            'input_ref': self.msa_ref})

    def test_msa_to_clustal(self):
        with self.assertRaises(NotImplementedError):
            ret = self.serviceImpl.msa_to_clustal_file(self.ctx, {'destination_dir': "./",
                                                                  'input_ref': self.msa_ref})

    def test_export_fasta(self):
        ret = self.serviceImpl.export_msa_as_fasta_file(self.ctx, {'input_ref': self.msa_ref})

    def test_export_clustal(self):
        with self.assertRaises(NotImplementedError):
            ret = self.serviceImpl.export_msa_as_clustal_file(self.ctx, {'input_ref': self.msa_ref})

    def test_bad_input(self):
        with self.assertRaisesRegex(ValueError, "parameter is required, but missing"):
            ret = self.serviceImpl.import_msa_file(self.ctx, {'msa_name': 'test_msa',
                                                              'input_file_path': "FOO!"})

        with self.assertRaisesRegex(ValueError, "parameter is required, but missing"):
            ret = self.serviceImpl.import_msa_file(self.ctx, {'workspace_name': self.wsName,
                                                              'input_file_path': "FOO!"})

        with self.assertRaisesRegex(ValueError, "supply either a input_shock_id or input_file_path"):
            ret = self.serviceImpl.import_msa_file(self.ctx, {'workspace_name': self.wsName,
                                                              'msa_name': "test_msa"})

        with self.assertRaisesRegex(ValueError, "destination_dir not in supplied params"):
            ret = self.serviceImpl.msa_to_fasta_file(self.ctx, {'input_ref': self.msa_ref})

        with self.assertRaisesRegex(ValueError, "input_ref not in supplied params"):
            ret = self.serviceImpl.export_msa_as_fasta_file(self.ctx, {})

