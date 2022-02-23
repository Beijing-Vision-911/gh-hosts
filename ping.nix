{ buildPythonPackage, fetchPypi }:
buildPythonPackage rec {
  pname = "ping3";
  version = "3.0.2";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-jiHAWHa4ZCIqtYCEcXlZBr9Nmx2TbDRey4F3KawNd60=";
  };

}
