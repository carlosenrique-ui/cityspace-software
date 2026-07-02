# IPT CitySpace – Event Contracts

This directory defines the **core software contracts** used by the IPT CitySpace Digital Twin Runtime Engine.

Contracts establish the **communication interfaces between system components**, ensuring that modules such as:

- UI
- Simulation timeline
- Visualization
- Runner engine
- Physical table actuators

remain **loosely coupled and maintainable**.

The system follows an **event-driven architecture**, where components exchange structured messages defined in this directory.

---

# Architectural Role

The contracts form the backbone of the runtime pipeline:


UI
↓
TemporalEvent
↓
State Machine / EventBus
↓
ConstructionFrame
↓
Renderer
↓
ActuatorCommand
↓
Runner
↓
Virtual or Physical Table


This architecture allows the same system to operate in:

- **Virtual simulation mode**
- **Physical table execution mode**

without modifying the core logic.

---

# Contracts

## TemporalEvent

Defined in:


temporal_event.py


Represents control commands sent to the **temporal engine**.

Typical sources:
- UI controls
- automated scripts
- event bus

Supported events:

| Event | Description |
|------|-------------|
| PLAY | Start simulation playback |
| PAUSE | Pause simulation |
| STEP_FORWARD | Advance one temporal step |
| STEP_BACKWARD | Go back one step |
| SEEK | Jump to a specific timeline position |

Example:

```python
TemporalEvent(
    event_type=TemporalEventType.PLAY
)

or

TemporalEvent(
    event_type=TemporalEventType.SEEK,
    t=1945
)
ConstructionFrame

Defined in:

construction_frame.py

Represents a temporal state snapshot of the construction evolution.

Each frame contains the delta of changes that occurred at a given moment.

Fields:

Field	Description
frame_id	unique frame identifier
t	temporal position (e.g. year or step)
created	elements created in this frame
removed	elements removed
updated	elements modified
metadata	optional additional information

Example:

ConstructionFrame(
    frame_id=12,
    t=1954,
    created=[...],
    removed=[...],
    updated=[]
)
ActuatorCommand

Defined in:

actuator_commands.py

Represents commands sent to renderers or physical actuators.

These commands are produced by the simulation engine and consumed by:

visualization renderers

hardware runner

virtual table renderer

Supported command types:

Command	Description
DRAW	create element or raise pin
ERASE	remove element or lower pin
UPDATE	modify existing element

Example:

ActuatorCommand(
    type=ActuatorCommandType.DRAW,
    payload={"row":3, "col":5, "height":120},
    layer="terrain"
)
Layers

Commands can target different logical layers:

Examples:

terrain

buildings

scanner

debug

Layers allow visualization toggling and separation of concerns between data sources.

Design Principles

The contract system follows several architectural principles:

Event Driven

The system communicates through events instead of direct method calls.

Loose Coupling

Modules do not depend on each other's implementation details.

Hardware Independence

The same simulation pipeline can run with:

virtual renderer

physical table

Temporal Simulation

The contracts support historical evolution of urban structures, allowing visualization of the development of IPT buildings from 1940 onward.

Integration with Table Hardware

The contracts ultimately drive the physical table through the runner engine.

Pipeline:

ConstructionFrame
      ↓
Renderer
      ↓
ActuatorCommand
      ↓
RunnerEngine
      ↓
Table Hardware

The hardware layer interprets commands such as:

(row, col, height)

which are mapped to actuator movements.

Future Extensions

The contract system is designed to support:

larger tables

different grid resolutions

multiple actuators

advanced simulation layers

alternative visualization engines

without changing the core architecture.

Project

IPT CitySpace

A tangible digital twin system for urban visualization and simulation.

Developed at:

Instituto de Pesquisas Tecnológicas (IPT)
São Paulo – Brazil

---

✅ Esse README já está adequado para:

- **GitHub empresarial**
- **documentação técnica**
- **auditoria institucional**
- **artigos científicos**

---

Se quiser, no próximo passo posso criar também um documento extremamente útil para o projeto:

**`docs/architecture/IPT_CITYSPACE_SYSTEM_ARCHITECTURE.md`**

que vai descrever **todo o sistema (offline + online + mesa física)** em nível institucional. Isso costuma ser exigido em projetos do IPT.