# DTDL Merger

This app pulls all the DTDL files from a folder and assembles a single DTDL file that can be either embedded in a Nuget, or used directly as part of a load.

# Getting Started

1. dotnet run --project .\Tools\DTDLMerger\DtdlMerger.csproj <inputdirectoryroot> > <outputfile>
i.e. "dotnet run --project .\Tools\DTDLMerger\DtdlMerger.csproj C:\repos\opendigitaltwins-building\Ontology\Willow\ > .\metadata\Willow.DTDLv3.jsonld"
