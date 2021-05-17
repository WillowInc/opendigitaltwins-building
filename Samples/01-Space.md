# Digital Twin Samples - Space

Space is one of the most prevalent entities and thus a fundamental concept to model with a digital twin. Many other models form relationships with space such as defining an asset’s location, how an asset serves a space, a lease for a tenant unit, or a portfolio of buildings. Almost every system or platform which the WillowTwin connects to also has a concept of space.

A Space is defined as a contiguous location in the physical world that has a 3D spatial extent and can contain sub-spaces or be apart of super-spaces to define a logical hierarchy. The following describes a common hierarchy amongst spatial twins:

## Spatial Hierarchy

![Space-Example1](Images/Space-Example1.png)

1. At the core of every spatial hierarchy is a Building. A Building is a type of space which generally has an address and a well-understood boundary based on its construction profile and registration as an entity with a local government.

2. Each Building has one or more Levels. These are vertical delineations within the building which may or may not be occupiable. The levels may be above or below ground and still considered part of the Building.

3. A Room is a type of space which is typically bounded by walls and part of the Level at which the floor of the Room is located. Rooms have codes and/or names assigned which give them a unique identity within the Building.

4. A Parking Spot is a space to park a vehicle and has a unique code. A Parking Spot can be assigned to a Level as shown in this example or a Room on a Level.

5. A Land is a contiguous space upon which one or more Buildings may be located. A Land typically has a well-defined outline that is projected as a 2D bounding box. Other terms for Land include site, campus, precinct, premises, or district.

6. A Portfolio is a Collection because it is not a contiguous location. Instead, a Portfolio can be used flexibly to define a group of Buildings and/or Lands that have commonality. A customer may have several Portfolios, and Buildings and Lands may belong to multiple Portfolios if the customer wants to create different groupings. For example, a Building may belong to the Acme Joint Venture portfolio as well as the Commercial Office portfolio. Additionally, a Portfolio may contain other Portfolios.

## Leasing Space

Leasing includes scenarios where people or companies are leasing space from a landlord. The following describes a common scenario with commercial office leasing:

![Lease-Example1](Images/Lease-Example1.png)

1. A Lease is defined as an Event because it has a defined start time and duration for which it is valid. The Lease event has many relationships to other types of twins as shown in this example and is essential to this use case.

2. The Lease contract is the actual document(s) which contain the Lease event legal terms. The Lease event is related to the Lease Contract using the regulatedBy relationship.

3. A Lease also has a leasee Company which is commonly referred to as the tenant company. Not shown in this example is another Lease relationship defining the lessor which is the company owning the asset and renting it to the leasee.

4. A Tenant Unit is a collection of Spaces which are being rented by the tenant company.

5. In this example, the Tenant Unit is a collection of one or more Rooms which is defined with the includedIn relationship. This is an important relationship because it is the means by which a Tenant Unit (and Lease) attach to spatial twins such as a Building via the Room and Level twins.

6. Notice that because the Tenant Unit is a Collection, that it cannot use the “isPartOf” relationship to attach directly to a Level. Therefore, in this example, at lease one Room is always required for each Tenant Unit. The single Room includedIn this Tenant Unit may encompass the entire Tenant Unit and be named the same as the Tenant Unit. For example, the Tenant Unit may be named “Suite 1400 – Acme Enterprises” and the Room may also be named “Suite 1400 – Acme Enterprises” and isPartOf Level 14.