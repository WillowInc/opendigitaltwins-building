# Digital Twin Samples - Space

Space is one of the most prevalent entities and thus a fundamental concept to model with a digital twin. Many other models form relationships with space such as defining an asset’s location, how an asset serves a space, a lease for a tenant unit, or a portfolio of buildings. Almost every system or platform which the WillowTwin connects to also has a concept of space.

A Space is defined as a contiguous location in the physical world that has a 3D spatial extent and can contain sub-spaces or be apart of super-spaces to define a logical hierarchy. The following describes a common hierarchy amongst spatial twins:

![Space-Example1](Images/Space-Example1.png)

1. At the core of every spatial hierarchy is a Building. A Building is a type of space which generally has an address and a well-understood boundary based on its construction profile and registration as an entity with a local government.

2. Each Building has one or more Levels. These are vertical delineations within the building which may or may not be occupiable. The levels may be above or below ground and still considered part of the Building.

3. A Room is a type of space which is typically bounded by walls and part of the Level at which the floor of the Room is located. Rooms have codes and/or names assigned which give them a unique identity within the Building.

4. A Parking Spot is a space to park a vehicle and has a unique code. A Parking Spot can be assigned to a Level as shown in this example or a Room on a Level.

5. A Land is a contiguous space upon which one or more Buildings may be located. A Land typically has a well-defined outline that is projected as a 2D bounding box. Other terms for Land include site, campus, precinct, premises, or district.

6. A Portfolio is a Collection because it is not a contiguous location. Instead, a Portfolio can be used flexibly to define a group of Buildings and/or Lands that have commonality. A customer may have several Portfolios, and Buildings and Lands may belong to multiple Portfolios if the customer wants to create different groupings. For example, a Building may belong to the Acme Joint Venture portfolio as well as the Commercial Office portfolio. Additionally, a Portfolio may contain other Portfolios.