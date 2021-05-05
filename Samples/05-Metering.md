# Digital Twin Samples - Metering

Metering encompasses scenarios where a physical or virtual meter device is measuring the flow of a substance such as electricity, fluid volume, or fluid mass to determine consumption by the recipient of the substance. The recipient could be an individual asset but is often mapped to a broader concept such as a building, tenant company, or space.

## Electrical Metering

In this example, we expand upon the Electrical distribution example and introduce Electrical Metering which measures the energy, power, and current being transmitted by circuits and consumed by equipment.

![Metering-Example1](Images/Metering-Example1.png)

1. Electrical Meters are a physical assets that have many different configurations. In this example, we show an Electrical Meter which is measuring the 3-Pole Electrical Circuit.

2. A 3-phase Electrical Meter can have many Capabilities relating to energy, power, and current for individual phases, between phases, and total. It may also compute power quality metrics such as total harmonic distortion, phase angles, and imbalance. In this example, we show an Electrical Power Sensor as just one of many Capabilities that the Meter has. We use the hostedBy relationship between the Capability and the Meter similar to how hostedBy is used with BMS Controllers.

3. The Electrical Power Sensor is measuring the Electrical 3-Phase Circuit. We use isCapabilityOf to define this relationship. This flexibility abstracts the Meter Asset hardware from the actual Capabilities it is hosting providing flexibility for many different metering scenarios. If a physical meter asset is measuring many circuits, this allows each Capability to be assigned to its associated Electrical Circuit which it is measuring.

4. In some instances, the Electrical Meter may be directly monitoring equipment (i.e. plug load meters) or individual twins of the electrical circuits may be not be created. In this example of a branch circuit meter, the Electrical Meter is trending two Energy Sensor metrics which is defined with the hostedBy relationship. The isCapabilityOf relationship assigns the Capability to a Fan Powered Box and an Exhaust Fan.

5. In some instances, a physical meter asset may be unknown or non-existent in the design. In this example, we show that the Luminaire is reporting its Electrical Current which may be a built-in Capability of that Luminaire.
