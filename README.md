# WillowTwin DTDL Ontology - Buildings
WillowTwin open digital twin definition language (DTDL) ontology for buildings and real estate

## Prerequisites

Before getting started:
* Install a code editor such as [Visual Studio Code](https://code.visualstudio.com/) to view, manage, and update the files.
* Install git to allow for cloning and working with this repo and its submodules. For Windows, we recommend [Git for Windows](https://gitforwindows.org/).
* Learn [basic git techniques](https://docs.github.com/en/github/using-git) such as creating a branching, committing, pulling, and pushing.
* Learn about the [Digital Twin Definition Language (DTDL)](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v2/dtdlv2.md) which defines the language used to describe models of digital twins.
* Learn about the [DTDL-based RealEstateCore ontology](https://github.com/Azure/opendigitaltwins-building) which forms the base ontology from which this WillowTwin ontology extends.
* Learn about [Azure Digital Twins](https://docs.microsoft.com/en-us/azure/digital-twins/) which is the service WillowTwin is built upon and this ontology gets loaded into as [Models](https://docs.microsoft.com/en-us/azure/digital-twins/concepts-models).

## Getting Started

* Clone this repo and its submodules to your local machine by running `git clone --recurse-submodules`.

    NOTE: This project includes `git submodules` which are references to other repos. If this repo was cloned by default, such as running `git clone`, this project will only include the directories of the submodules but not the files within them yet. To initialize and pull down the submodule files, run the command: `git submodule update --init --recursive`. Read more about working with submodules [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

* After successfully cloning the submodules, there should be files in the following directories:

    | Submodule | Description |
    | --------- | ----------- |
    | DTDL-Validator | Tool to parse and validate the DTDL ontology |
    | Ontology\opendigitaltwins-building | DTDL-based RealEstateCore ontology |

* Confirm all of the DTDL files have been downloaded by navigating to the Ontology directory in a command prompt and running `DTDLValidator.exe`. The output should include **Validated all files - Your DTDL is valid**. After making changes to the DTDL files, it is recommended to run this command prior to committing changes.

* Start browsing the Ontology which has the following top-level directories:

    | Directory | Description |
    | --------- | ----------- |
    | opendigitaltwins-building\Ontology | DTDL-based RealEstateCore ontology. This is the base set of DTDL models from which the Willow models extend |
    | Willow | This is the set of WillowTwin DTDL models which are used for creating digital twins |

    NOTE: When creating twins in the WillowTwin, they are always based on a Willow DTDL model id which begins with `dtmi:com:willowinc:`.

## Key Concepts

### Ontology Overview

A model which **extends** another model recusively inherits all of the Properties, Relationships, and Components from the referenced model. The following table describes the set of top-level models for this ontology. These form the base from which all other models extend from.

| Model | Description |
| --------- | ----------- |
| Agent | Any basic types of stakeholder that can have roles or perform activities, e.g., people, companies, departments. |
| Asset | An object such which is located inside (or outside) a building, but is not an integral part of that building's structure, for example architectural, furniture, and equipment. Assets are typically products that have a manufacturer, model, and serial number |
| Building Component | A part that constitutes a piece of a building's structural makeup, for example Facade, Wall, Slab, RoofInner, etc. These are typically constructed onsite. |
| Capability | A capability indicates the capacity of a entity, be it a Space, an Asset, or a LogicalDevice, to produce or ingest data. This is equivalent to the term "point" in Brick Schema and generic Building Management System. Specific subclasses specialize this behavior: Sensor entities harvest data from the real world, Actuator entities accept commands from a digital twin platform, and Parameter entities configure some capability or system. |
| Collection | An administrative grouping of entities that are addressed and treated as a unit for some purpose. These entities may have some spatial arrangement (e.g., a Tenant Unit is typically contiguous), however that is not a requirement (see, e.g., a distributed Campus consisting of spatially disjoint plots or buildings). |
| Document | A formal piece of written, printed or electronic matter that provides information or evidence or that serves as an official record, for example LeaseContract, Building Specification, Warranty, Drawing, etc. |
|Event | A spatiotemporally indexed entity with participants, something which occurs somewhere, and that has or takes some time, for example a Lease or Rent. |
| Space | A contiguous part of the physical world that has a 3D spatial extent and that contains or can contain sub-spaces. For example a Region can contain many pieces of Land, which in turn can contain many Buildings, which in turn can contain Levels and Rooms. |

NOTE: Many of the models include **Components**. These are not intended to be instantiated as digital twins. They can be thought of as a reusable interface by many models or a folder to organize a related set of Properties and Relationships.

Models define the possible set of Properties, Relationships, and Components that a twin may have; however, a twin does not have to include all of these at runtime. A twin is only required to have an **id** and a reference **model**.

### Relationships

```
Coming Soon
```

## Frequency Asked Questions

**How do I determine which model to use when deciding between a model which extends another?**

It is recommended to be as specific as possible when creating twins to provide the most detailed classification. As such, the "child" model which extends the "parent" should always be used. For example, when creating a twin of a Fan Powered Box that is known to have a heating element, the model `dtmi:com:willowinc:FanPoweredBoxReheat;1` should be used instead of a more generic model from which it extends such as `dtmi:willowinc:TerminalUnit;1`, `dtmi:willowinc:VAVBox;1`, or `dtmi:willowinc:FanPoweredBox;1`.