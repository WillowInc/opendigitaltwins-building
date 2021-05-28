# Capabilities

## Overview

A capability indicates the ability of a entity such as a Space, an Asset, or a System, to produce or ingest data. This is equivalent to the term `point` in Project Haystack, Brick Schema, or a Building Management System or the terms `trend`, `metric`, or `variable` in a time series data store. Specific subclasses specialize this behavior: `Sensor` entities harvest data from the real world, `Actuator` entities accept commands from a digital twin platform, `Parameter` entities configure some capability or system, and `State` entities maintain the status of the target twins.

When the WillowTwin connects to a system or source of data, a capability twin maintains the current value (or latest value received) and a time series record of historical values.

It's important to understand the difference between a `capability` and other entities such as an `asset`. A `capability` is a virtual concept while an `asset` is a physical object. For example, a physical asset of a `sensor equipment` may have one or more capabilities such as `occupancy sensor`, `temperature sensor`, and `illuminance sensor`.

This guide will provide an understanding of how to become familiar with the capabiltiy data model, define capabilty twins and recommendations for how to best use the ontology.

## Capabiltiy Models
The `Capability` model class has been sub-classified in several ways that enable the implementer to give semantics to the type of data that the capability is referencing. The concept of using classification and model inheritance provides a few benefits over an alternative approach such as tagging:
* Model classification promotes structure and consistancy compared to ad-hoc tags
* Model classification promotes understanding over flexibility. A tag by itself only has context in terms of how it gets used with other tags.

In order to provide the highest fidelity digital twin, the implementer should strive to create twins that have the most specific classification, or deepest inheritance. For example, an `Active Electrical Energy Sensor` should be used over `Electrical Energy Sensor` when it is known that the sensor is measuring active or real power.

### Capability Functions
The first sub-classification of `Capability` is by **function**. The function describes the purpose or behavior of that capability in the context of its parent twin(s). The **function** sub-classes are the following:

| Function | Description |
| -------- | ----------- |
| Sensor | Measures, detects, or harvests data from the real world. An `input` to a controller which is considered read-only. |
| Actuator | Executes some real-world action based on an input command. Often an `output` from a controller. |
| Parameter | Any configuration setting used by a controller or system to guide its operation. |
| Setpoint | A sub-classification to `Parameter` which is a configuration `input` to a controller defining the desired quantity or state of its parent entity. |
| State | Defines the status of an entity such as mode, position, or level which is not directly defined by a real-world sensor. An `input` to a controller which is considered read-only. |

### Capability Kinds
The second sub-classification of `Capability` is by **kind**. The kind describes the primitive schema of the values of the capability with the following sub-classes:

| Kind | Description |
| -------- | ----------- |
| Quantity | A kind of quantity values defined by measurement units. Inspired by QUDT. |
| State | A kind of unitless values such as boolean, percent, and strings. |

If the type of values and units of a Capability are known, the implementer can indentify which **kind** a capability should be classified as.

#### Quantity Kind
Within the Quantity Kind class, there are many sub-classes which are inspired by both the [DTDL Semantic types](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v2/dtdlv2.md#semantic-types) and [QUDT](http://www.qudt.org/doc/DOC_VOCAB-QUANTITY-KINDS.html). This buildings ontology focuses on applicable Quantity Kinds to the Building and Real Estate industry and has omitted many of the classes found in QUDT that are applicable to other scientific and physics-centric industries.

The Quantity Kind subclass names (i.e. Temperature, Power, and Flow) are common across each of the top-level Capability sub-classes of `Sensor`, `Actuator`, and `Parameter\Setpoint`. However, these top-level sub-classes do not use multiple inheritance of a common QuantityKind class. As such, clients can query across these top-level classes (i.e. TemperatureSensor and TemperatureSetpoint) by using a string match function such as `STARTSWITH`.

#### State Kind
Within the State Kind class, there are three sub-classes which are defined by their unitless value schema:

| State Kind | Description |
| ---------- | ----------- |
| Binary | Boolean values `true` or `false` |
| Percent | Number values between `0...1` |
| Multi-State | `String` values often defined by an enumeration |

Each of the above State Kind classes are further sub-classed to give context to the type of State that is being sensed, actuated, configured, or maintained. The State Kind subclass names (i.e. OnOff, Mode, and Position) are common across each of the top-level Capability sub-classes of `Sensor`, `Actuator`, and `Parameter\Setpoint`. However, these top-level sub-classes do not use multiple inheritance of a common StateKind class. As such, clients can query across these top-level classes (i.e. TemperatureSensor and TemperatureSetpoint) by using a string match function such as `STARTSWITH`.

## Capability Properties
The Capability models maintain several **properties** which allow additional metadata on the twin to provide context to 1) classificaiton 2) values and 3) communication configuration. The properties also maintain the latest value the twin received from the connected entity (`lastValue`) and the time at which it was sampled or reported by the connected entity (`lastValueTime`).

### Classification Properties
The Capabiltiy models described above provide a great means of classifying based on **function** and **kind** which brings consistency and inheritence to these two common means by which a Capability is defined and would be queried. However, most impelementations of a digital twin desire additional metadata context to query, analyze, and filter amongs twins of the same model. Because there are many ways in which a capability could be classified in the real world, there are too many combinations to pre-define models for every possible real-world scneario. The use of classification properties allows the flexibility to add context to the base set of models which have been defined above.

The following **properties** allow the implementer to define that additional context upon creating a capability twin. These provide similar functionality of tags in that they add meaning to the type of capability; however, they differ in implementation. Because these are defined as Properties in the DTDL Capability model, the twin maintains a *key-value pair* which provides the context in the *key* as to why the *value* of the property has been set. Additionally, the properties have been defined as disjoint enumerations which provides additional structure to the ontology over a taging dictionary.

#### Phenomenon
A capability's `phenomenon` defines the aspect of scientific interest that it is measuring, actuating, or configuring. This is inspired by Project Haystack. It is the most common classification property that an implementer would define.

The Quantity Kind defines the measurable property of a phenomenon. As such, every twin within a Quantity Kind sub-class should define the phenomenon property. Common phenomenon - quantity kind pairs in the building domain include the following:

| **Phenomenon** | Quantity Kinds |
| --- | ---|
| Air | Temperature, Volume Flow, Static Pressure, Air Quality, Humidity, Humidity Ratio, Enthalpy |
| Water | Temperature, Volume Flow, Mass Flow, Pressure |
| Chilled Water | Temperature, Volume Flow, Mass Flow, Mass, Pressure |
| Natural Gas | Mass Flow, Mass |
| AC Electricity | Voltage, Current, Electrical Power, Electrical Energy, Frequency, Power Factor |
| Drive Electricity | Frequency, Voltage, Current, Electrical Power |
| Precipitation | Volume Flow |
| Wind | Wind Direction, Linear Velocity |
| Solar | Irradiance, Luminance |
| Light | Illuminance |
| Data | Data Rate, Data Size |

```
Note:
Because phenomemon is defined as a string enumeration, there is no inheritance as you would have from models that extend one another. For example, `Chilled Water`, `Hot Water`, and `Domestic Cold Water` are all considered types of `Water`. `Water` and `Air` are considered types of **fluids**. Similarly, `Precipitation` and `Wind` are considered types of **Weather**. At this time, it is recommended to query using `ENDSWITH` for the phenomenon which have a common inheritance such as `Hot Water` and `Domestic Cold Water`.
```

#### Position
A capability's `position` defines the location or placement relative to its parent entity such as an asset, system, or space. This context is often necessary to define whether the capability is related to an input, output, or net differential to the parent entity.

Different types of entities use established industry terminology to define the same semantic meaning of placement. For example, piping systems use the terms `entering` (input), `leaving` (output), and `delta` (net) whereas electrical energy uses the terms `import` (input), `export` (output), and `net` (net).

In order to encourage consistency across implementations, its extremely important to align on when to use which placement term. At this time, the ontology doesn't restrict usage to specific scenarios. Additionally, DTDL doesn't support a "sameAs" definition as found in OWL which would enable linking different terminology that have the same semantic meaning. This makes it even more critical to have a common understanding of the terminology.

Here is a reference on how to select the proper `placement` value:

| Scenario | **Placement** |
| --- | ---|
| Duct (Air) | Exhaust, Outside, Return, Discharge, Zone, Mixed, Underfloor, Economizer |
| Pipe (Water) | Entering, Leaving, Header, Bypass, Circulating, Delta |
| Electricity | Input, Output |
| Energy | Import, Export, Net |
| Solar | Azimuth, Zenith |
| Data | Download, Upload |


#### Other Classification Properties

* Asset Component
* HVAC Mode
* Occupancy Mode
* Electrical Phase
* Aggregate (TBD)

### Value Properties

* Last Value
* Last Value Time

* Unit

* Minimum Valid Value
* Maximum Valid Value

* Historization Method (Sampled, CoV, Sync/Async, Consumption)
* Value Reporting Method (Totalized)

## Capability Relationships

