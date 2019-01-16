# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from MSAUtils.Core.FileUtils import FileUtil
#END_HEADER


class MSAUtils:
    '''
    Module Name:
    MSAUtils

    Module Description:
    A KBase module: MSAUtils
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/MSAUtils.git"
    GIT_COMMIT_HASH = "f33d1d9d21c06cbaf4df6d3408f5d25eac54ab0d"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.futil = FileUtil(self.config)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def import_msa_file(self, ctx, params):
        """
        import_msa_file: import a MSA from FASTA
        :param params: instance of type "ImportMSAParams" -> structure:
           parameter "input_shock_id" of String, parameter "input_file_path"
           of String, parameter "input_staging_file_path" of String,
           parameter "msa_name" of String, parameter "description" of String,
           parameter "workspace_name" of String
        :returns: instance of type "ImportMSAOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of type "obj_ref"
           (An X/Y/Z style reference @id ws), parameter "structure_obj_ref"
           of type "obj_ref" (An X/Y/Z style reference @id ws)
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN import_msa_file
        logging.info('Starting √ with params:\n{}'.format(params))
        result = self.futil.import_fasta_file(params)
        #END import_msa_file

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method import_msa_file return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def msa_to_fasta_file(self, ctx, params):
        """
        :param params: instance of type "MSAToFileParams" -> structure:
           parameter "msa_name" of String, parameter "workspace_name" of
           String
        :returns: instance of type "MSAFilesOutput" -> structure: parameter
           "file_path" of String
        """
        # ctx is the context object
        # return variables are: files
        #BEGIN msa_to_fasta_file
        logging.info('Starting msa_to_fasta_file with params:\n{}'.format(params))
        files = self.futil.msa_to_fasta_file(params)
        #END msa_to_fasta_file

        # At some point might do deeper type checking...
        if not isinstance(files, dict):
            raise ValueError('Method msa_to_fasta_file return value ' +
                             'files is not type dict as required.')
        # return the results
        return [files]

    def msa_to_clustal_file(self, ctx, params):
        """
        :param params: instance of type "MSAToFileParams" -> structure:
           parameter "msa_name" of String, parameter "workspace_name" of
           String
        :returns: instance of type "MSAFilesOutput" -> structure: parameter
           "file_path" of String
        """
        # ctx is the context object
        # return variables are: files
        #BEGIN msa_to_clustal_file
        logging.info('Starting msa_to_clustal_file with params:\n{}'.format(params))
        files = self.futil.msa_to_clustal_file(params)
        #END msa_to_clustal_file

        # At some point might do deeper type checking...
        if not isinstance(files, dict):
            raise ValueError('Method msa_to_clustal_file return value ' +
                             'files is not type dict as required.')
        # return the results
        return [files]

    def export_msa_as_fasta_file(self, ctx, params):
        """
        :param params: instance of type "ExportParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference
           @id ws)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_msa_as_fasta_file
        logging.info('Starting export_msa_as_fasta_file with params:\n{}'.format(params))
        output = self.futil.export_file(params, file_type='fasta')
        #END export_msa_as_fasta_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_msa_as_fasta_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_msa_as_clustal_file(self, ctx, params):
        """
        :param params: instance of type "ExportParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference
           @id ws)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_msa_as_clustal_file
        logging.info('Starting export_msa_as_clustal_file with params:\n{}'.format(params))
        output = self.futil.export_file(params, file_type='clustal')
        #END export_msa_as_clustal_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_msa_as_clustal_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
