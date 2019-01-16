import hashlib
import logging
import os
import shutil
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport


class FileUtil:

    def _validate_import_file_params(self, params):
        """
        _validate_import_matrix_from_excel_params:
            validates params passed to import_matrix_from_excel method
        """
        # check for required parameters
        for p in ['msa_name', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        if params.get('input_file_path'):
            file_path = params.get('input_file_path')
        elif params.get('input_shock_id'):
            file_path = self.dfu.shock_to_file(
                {'shock_id': params['input_shock_id'],
                 'file_path': self.scratch}).get('file_path')
        elif params.get('input_staging_file_path'):
            file_path = self.dfu.download_staging_file(
                        {'staging_file_subdir_path': params.get('input_staging_file_path')}
                        ).get('copy_file_path')
        else:
            error_msg = "Must supply either a input_shock_id or input_file_path "
            error_msg += "or input_staging_file_path"
            raise ValueError(error_msg)

        return file_path, params.get('workspace_name'), params.get('structure_name')

    def _upload_to_shock(self, file_path):
        """
        _upload_to_shock: upload target file to shock using DataFileUtil
        """
        logging.info('Start uploading file to shock: {}'.format(file_path))

        file_to_shock_params = {
            'file_path': file_path,
            'pack': 'gzip',
            'make_handle': True,
        }
        shock_id = self.dfu.file_to_shock(file_to_shock_params)['handle']['hid']

        return shock_id

    def _fasta_file_to_data(self, file_path):
        """Do the FASTA conversion"""
        raise NotImplementedError
        return data, message

    def _generate_report(self, msa_ref, workspace_name, message):
        """
        _generate_report: generate summary report for upload
        """
        report_params = {'message': message,
                         'objects_created': [{'ref': msa_ref,
                                              'description': 'Imported MSA'}],
                         'workspace_name': workspace_name,
                         'report_object_name': f'import_msa_file_{uuid.uuid4()}'}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _get_object(self, params):
        ret = self.dfu.get_objects(
            {'object_refs': [params['input_ref']]}
        )['data'][0]
        obj_name = ret['info'][1]
        obj_data = ret['data']
        return obj_name, obj_data

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)

    def import_fasta_file(self, params):

        file_path, workspace_name, msa_name = self._validate_import_file_params(params)

        if not isinstance(workspace_name, int):
            workspace_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            workspace_id = workspace_name

        data, message = self._fasta_file_to_data(file_path)
        data['description'] = params.get('description', '')
        data['sequence_type'] = params.get('sequence_type', '')
        logging.info(data)

        info = self.dfu.save_objects({
            'id': workspace_id,
            'objects': [
                {'type': 'KBaseTrees.MSA',
                 'name': msa_name,
                 'data': data}]
        })[0]
        obj_ref = f"{info[6]}/{info[0]}/{info[4]}"

        returnVal = {'msa_obj_ref': obj_ref}

        report_output = self._generate_report(obj_ref, workspace_name, message)

        returnVal.update(report_output)

        return returnVal

    def msa_to_fasta_file(self, params):
        if "input_ref" not in params:
            raise ValueError("input_ref not in supplied params")
        if "destination_dir" not in params:
            raise ValueError("destination_dir not in supplied params")

        obj_name, obj_data = self._get_object(params)
        keys = obj_data.get('row_order', obj_data['alignment'].keys)
        row_labels = obj_data.get('default_row_labels', {})
        file_path = os.path.join(self.scratch, f'{obj_name}.fasta')

        with open(file_path, 'w') as outfile:
            for key in keys:
                # header
                outfile.write(f'>{key} {row_labels.get(key, "")}\n')
                # sequence
                outfile.write(f"{obj_data['alignment'][key]}\n")

        return {'file_path': file_path}

    def msa_to_clustal_file(self, params):
        raise NotImplementedError

    def export_file(self, params, file_type='fasta'):
        params['destination_dir'] = os.path.join(self.scratch, str(uuid.uuid4()))
        os.mkdir(params['destination_dir'])

        if file_type == 'fasta':
            file_path = self.msa_to_fasta_file(params)['file_path']
        elif file_type == 'clustal':
            file_path = self.msa_to_clustal_file(params)['file_path']
        else:
            raise ValueError(f"Invalid file type: {file_type}. Must be 'fasta' or 'clustal")

        return {'shock_id': self._upload_to_shock(file_path)}
