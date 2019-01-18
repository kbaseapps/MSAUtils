/*
A KBase module: MSAUtils
*/

module MSAUtils {
  /* A boolean - 0 for false, 1 for true.
    @range (0, 1)
  */
  typedef int boolean;

  /* An X/Y/Z style reference
    @id ws
  */
  typedef string obj_ref;

    typedef structure {
      string input_shock_id;
      string input_file_path;
      string input_staging_file_path;
      string file_format;
      string msa_name;
      string description;
      string workspace_name;
  } ImportMSAParams;

  /* @optional report_name report_ref */
  typedef structure {
      string report_name;
      obj_ref report_ref;
      obj_ref msa_obj_ref;
  } ImportMSAOutput;

  /* import_msa_file: import a MSA from FASTA*/
  funcdef import_msa_file (ImportMSAParams params) returns (ImportMSAOutput result) authentication required;

    typedef structure {
        string file_path;
    } MSAFilesOutput;

    typedef structure {
        string msa_name;
        string workspace_name;
    } MSAToFileParams;

    funcdef msa_to_fasta_file(MSAToFileParams params)
                returns(MSAFilesOutput files) authentication required;

    funcdef msa_to_clustal_file(MSAToFileParams params)
                returns(MSAFilesOutput files) authentication required;


    typedef structure {
        obj_ref input_ref;
    } ExportParams;

    typedef structure {
        string shock_id;
    } ExportOutput;

    funcdef export_msa_as_fasta_file(ExportParams params)
                returns (ExportOutput output) authentication required;

    funcdef export_msa_as_clustal_file(ExportParams params)
                returns (ExportOutput output) authentication required;
};
