# Digital Twin Samples - HVAC

HVAC includes scenarios where temperature control and comfort of spaces is being performed by a building management system (BMS) and/or individual equipment controllers. Use cases include energy optimization, demand response, automated and predictive maintenance, and increasing productivity by improving comfort.

At a fundamental level, HVAC systems exchange energy and move air and water to condition a space. However, the configuration of HVAC systems can vary widely based on the climate of a location, size of the building, age of the building, and many other factors. While the configurations are limitless, this example shows a common scenario of conditioning air using an Air Handling Unit.

## HVAC Multi-Room Zone

![HVAC-Example1](Images/HVAC-Example1.png)

1. An Air Handling Unit is one of the most complex equipment types to data model because it can come in many different configurations and be installed in many different scenarios. An Air Handling Unit has at least one inlet duct, conditions the air with cooling and heating elements, and sends the air out with at least one outlet duct. In this example, the conditioned air is sent to a Fan Powered Box which is a type of Terminal Unit. These equipment are connected via ductwork which is modeled using the isFedBy relationship. Not indicated on the relationship is the Supply Air substance which is being fed.

2. The Fan Powered Box conditions and regulates the air flow to the HVAC Zone space. The HVAC Zone is a core concept in the HVAC scenario. An HVAC Zone is a type of Space which has a boundary, generally aligns 1:1 with a Room, but can also be more granular or broader.

3. In this example, there are multiple Rooms within a single HVAC Zone. Because both Zones and Rooms are Spaces, we use the relationship isPartof to define the Rooms which are contained within the HVAC Zone.

4. In HVAC Systems, there is often a control network such as BACnet and controllers which host the control logic for the HVAC equipment. In this example, there is a single BACnet Controller which hosts the Capabilities that are associated with the Fan Powered Boxes. We use the hostedBy relationship to define which Capabilities the Controller manages.

5. Each Capability has a primary relationship to one or more Assets, Spaces, or Equipment Collections. In this example, the Zone Air Temperature Sensors each relate to a Fan Powered Box. We use the isCapabilityOf relationship to define which twin a Capability belongs to. By leveraging both the hostedby and isCapabilityOf relationships, this provides the flexibility to accommodate scenarios where an Asset’s Capabilities are hosted by separate Controllers as well as a Capability belonging to multiple entities.

## HVAC Multi-Zone Room

![HVAC-Example2](Images/HVAC-Example2.png)

1. In this example, we show the flexibility in a zone where there are multiple Zones within one Room. Because both Zones and Rooms are Spaces, we use the relationship isPartof.

2. The HVAC Zone has a Zone Air Temperature Sensor Capability which directly corresponds to the Fan Powered Box capability because there is only a single Zone Temperature Sensor.

3. In some scenarios, an equipment such as a Fan Powered Box may have several Zone Air Temperature Sensors in which there is logic in the controller which averages or takes the minimum of maximum of the multiple sensor readers to determine its control sequence.

4. When there are multiple Zone Air Temperature Sensors (#3) serving a single HVAC Zone and the connection solution doesn’t calculate and emit the aggregate for the Zone, the Zone’s Temperature Sensor Capability (#4) will need to be calculated by the WillowTwin by performing an average function.

## HVAC Basic Relationships with Level

![HVAC-Example3](Images/HVAC-Example3.png)

1. In this example, we show a scenario where it is not known which rooms are being conditioned by individual HVAC equipment, but it is known that the equipment is conditioning the 1st Floor. We establish the isPartOf relationship directly from the HVAC Zone to the Level. This is common when discovering HVAC equipment via a BMS connection but not having HVAC floor plans or not wanting to establish room-level fidelity.

2. The Fan Powered Box is located on the same floor that it is conditioning which is indicated by the locatedIn relationship.

3. Rooftop Units commonly condition spaces that are not on the same level in which they are located. The Rooftop Unit here is located on the Roof but conditions the 1st Floor.

## HVAC Pressurization Zone

![HVACPressurizationZone-Example1](Images/HVACPressurizationZone-Example1.png)

1. In this example, we show how to configure an HVAC Pressurization Zone which is a type of HVAC zone whose control is setup to maintain a positive or negative pressure. These are commonly used in critical spaces such as laboratory and healthcare rooms which prevent the spread of contaminants in or out of spaces. These spaces often also have different ventilation requirements than standard occupiable HVAC zones. The HVAC Pressurization Zone isPartOf a Room just as a typical HVAC Zone would be configured.

2. The isFedBy relationships indicated the direction of the airflow. The Supply VAV Airflow Control Valves bring fresh air into the space while the General/Fume Exhaust VAV Airflow Control Valves exhaust air out of the space.

3. Fume Hoods may also be location in the space in which case the zone first feeds the Fume Hoods which then feed the Fume Exhaust VAV Airflow Control Valves.

4. The Exhaust VAV Control Valves across many zones often feed a common exhaust fan manifold which is shown as the Fan Group (HVAC). This equipment group consists of several Exhaust Fans that are staged and typically provide redundancy to the critical system.

5. There are many capabilities which are associated with the overall room. These are modeled as capabilities of the HVAC Pressurization Zone. A few of these are indicated in this example such as the Discharge Airflow Setpoint and Air Changes Per Hour but this is not an exhaustive list.

6. Similarly, each of the assets and asset groups shown in this example have capabilities associated with them. For simplicity on a few of these capabilities are shown such as the Face Velocity Setpoint on the Fume Hood or the Damper Position Actuator on the Supply VAV Airflow Control Valve.
