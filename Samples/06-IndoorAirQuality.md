# Digital Twin Samples - Indoor Air Quality

Indoor Air Quality (IAQ) is a common sensor scenario which is used for building health and wellness metrics.

## Indoor Air Quality Sensor

![IAQ-Example1](Images/IAQ-Example1.png)

1. When creating twins for scenarios where sensors are measuring properties of a space (i.e. IAQ, Occupancy, Temperature, Illuminance), we leverage the Zone concept which allows for flexibility in defining the spatial extent that the sensor is meant to be considered as measuring. In this example, we show the flexibility in a Zone where there are multiple Rooms within one Zone. Because both Zones and Rooms are Spaces, we use the relationship isPartof.

2. The IAQ Sensor Equipment is the physical asset which is installed in the space. Generally, each equipment is aligned 1:1 with a Zone. The relationship servedBy is used between the IAQ Sensor Equipment (Asset) and the Zone (Space).

3. In this example, the IAQ Sensor Equipment has several Sensor Capabilities – PM 2.5, TVOC, and Relative Humidity. We use the isCapabilityOf relationship between the Capabilities and the IAQ Sensor Equipment.
