# OpenDigitalTwins-Building Metadata

The files in this folder are used for assembling the Willow.Ontology.DTDLv3 nuget package.

The jsonld file must be updated locally and checked in for the Nuget to get a new version. This can be done by running the following command from your root directory (note that you may need to update the paths here slightly):

"dotnet run --project .\Tools\DTDLMerger\DtdlMerger.csproj C:\repos\opendigitaltwins-building\Ontology\Willow\ > .\metadata\Willow.DTDLv3.jsonld"
