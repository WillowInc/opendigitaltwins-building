# WillowTwin DTDL Ontology - Buildings
WillowTwin open digital twin definition language (DTDL) ontology for buildings and real estate

asdfsdaf

## Prerequisites

Before getting started:
* Install a code editor such as [Visual Studio Code](https://code.visualstudio.com/) to view, manage, and update the files.
* Install git to allow for cloning and working with this repo and its submodules. For Windows, we recommend [Git for Windows](https://gitforwindows.org/).
* Learn [basic git techniques](https://docs.github.com/en/github/using-git) such as creating a branching, committing, pulling, and pushing.
* Learn about the [Digital Twin Definition Language (DTDL)](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL//dtdlv2.md) which defines the language used to describe models of digital twins.
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

* Confirm all of the DTDL files have been pulled to your local machine by running the [DTDL Validator](https://github.com/Azure-Samples/DTDL-Validator) self-contained executable. The output should include **Validated all files - Your DTDL is valid**. After making changes to the DTDL files, it is recommended to run this command prior to committing changes.

* Start browsing the Ontology which has the following top-level directories:

    | Directory | Description |
    | --------- | ----------- |
    | opendigitaltwins-building\Ontology | DTDL-based RealEstateCore ontology. This is the base set of DTDL models from which the Willow models extend |
    | Willow | This is the set of WillowTwin DTDL models which are used for creating digital twins |

    NOTE: When creating twins in the WillowTwin, they are always based on a Willow DTDL model id which begins with `dtmi:com:willowinc:`.

## Key Concepts

### Ontology Overview

A model which **extends** another model recusively inherits all of the Properties, Relationships, and Components from the referenced model. The following table describes the set of top-level models for this ontology. These form the base from which all other models extend.

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

Relationships between twins are what give the WillowTwin its powerful capabilities to action data. The more relationships that exist in for a given set of twins, also known as a greater graph density, the more opportunity there is for descriptive, presctiptive, predicitive, and real-time analtyics.

We encourage twins to be created and updated with as many relationships as possible; however, it is important that users (and machines) creating twins have a common understanding of the real-world meaning of relationships just as they should have a common understanding of the real-world meaning of models. Having this alignment allows for the highest accuracy of the analytics and thus trust in the outcomes that are actioned and surfaced by the data.

Here are the commmon relationships found in the ontology:

| Relationship | Description |
| ------------ | ----------- |
| isPartOf | A simplified set of topological relations to connect sub- and super-entities within the top-level RealEstateCore interface tree. "isPartOf" operates on entities of the same type, for example Spaces have only Spaces as parts, Assets have only Assets as parts, etc. |
| isCapabilityOf | Indicates that a Space, Asset or LogicalDevice has the ability to produce or ingest data represented by sensors, actuators or parameters. |
| includedIn | Indicates that an entity is included in some Collection, for example a Building is included in a RealEstate, or an Asset is included in a System. |
| locatedIn | Indicates that a given Asset is physically located in a Space. |
| hostedBy | Indicates that a capability or logical device is hosted by another entity such as an asset. |
| servedBy | The coverage or area impacted by a given Asset or Sensor/Actuator. Note that Assets can also service one another. |
| isFedBy | Indicates that a given equipment or space is fed "something" by another equipment, like electricity, water or air. |
| hasDocument | Indicates that an entity has accompanying details or references in a Document such as a Drawing, Product Data, Warranty, or Lease Contract. |

Here are examples of how to use relationships:

| Relationship | Examples |
| ------------ | ------- |
| isPartOf | Room-->isPartOf-->Level<br>Room-->isPartof-->HVACZone |
| isCapabilityOf | ZoneAirTemperatureSetpoint-->isCapabilityOf-->FanPoweredBox<br>PeopleCountSensor-->isCapabilityOf-->OccupancyZone |
| includedIn | FanPoweredBox-->includedIn-->HVACSupplyAirSystem<br>DomesticWaterPump-->includedIn-->PlumbingPumpGroup<br>Building-->includedIn-->Portfolio |
| locatedIn | Workstation-->locatedIn-->Room<br>AirHandlingUnit-->locatedIn-->Level |
| hostedBy | ZoneAirTemperatureSetpoint-->hostedBy-->BACnetController<br>ElectricalEnergySensor-->hostedby-->ModbusController |
| servedBy | OccupancyZone-->servedBy--PeopleCountSensorEquipment<br>Room-->servedBy-->VideoSurveillanceCamera<br>Level-->servedBy-->Elevator |
| isFedBy | FireSprinklerHead-->isFedBy-->SprinklerValve<br>Sink-->isFedBy-->ElectricTankWaterHeater<br>Luminaire-->isFedBy-->ElectricalCircuit1Pole |
| hasDocument | AirHandlingUnit-->hasDocument-->Warranty<br>HVACChilledWaterSystem-->hasDocument-->TestReport<br>Level-->hasDocument-->AsBuiltDrawing |

Relationships can also have properties with all of the same semantics as properties on twins. This is an powerful feature of DTDL which allows for the graph to better model the real world. In this ontology, the **isFedBy** relationship defined on [Equipment](https://github.com/Azure/opendigitaltwins-building/blob/master/Ontology/Asset/Equipment/Equipment.json), [HVACZone](https://github.com/WillowInc/opendigitaltwins-building/blob/main/Ontology/Willow/Space/Zone/HVACZone.json), and [LightingZone](https://github.com/WillowInc/opendigitaltwins-building/blob/main/Ontology/Willow/Space/Zone/LightingZone.json) has a property **substance** which defines what is being fed such as **SupplyAir**, **HotDomesticWater**, **ACElec**, or **Light**. This property has been defined as an Enum such that the allowed values for substance must come from the list defined in the above models.

NOTE: We recommend that the **substance** proeperty be defined on all **isFedBy** relationships to enable the best WillowTwin user experience. We also recommend using the most descriptive **substance** such as **SupplyAir** instead of **Air** and **SprinklerWater**instead of **Water**.

## Samples

For more in-depth examples of common scenarios, visit the [Samples](Samples).

These include diagrams and accompanying narratives to learn how to organize the data, what models should be used when creating twins, and the types of relationships between the twins.

## Frequency Asked Questions

**How do I determine which model to use when deciding between a model which extends another?**

It is recommended to be as specific as possible when creating twins to provide the most detailed classification. As such, the "child" model which extends the "parent" should always be used. For example, when creating a twin of a Fan Powered Box that is known to have a heating element, the model `dtmi:com:willowinc:FanPoweredBoxReheat;1` should be used instead of a more generic model from which it extends such as `dtmi:willowinc:TerminalUnit;1`, `dtmi:willowinc:VAVBox;1`, or `dtmi:willowinc:FanPoweredBox;1`.

**How do I determine whether to use a given relationship or its inverse?**

In general, relationships should be defined on the "children" twins with an outgoing relationship to a common "parent". For example, there are typically many rooms on a building level so the relationship would be defined as `Room-->isPartOf-->Level`. Similarly, there are many luminaires fed by an electrical circuit so the relationship would be defined as `Luminaire-->isFedBy-->ElectricalCircuit1Pole`.

