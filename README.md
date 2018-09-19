# Power Supply [![Build Status](https://travis-ci.com/vmaraccini/power-supply.svg?branch=master)](https://travis-ci.com/vmaraccini/power-supply)

**A testable, open hardware power supply project**


### Rationale

The purpose of this project is to try a somewhat test-driven approach to design hardware components.

Inspired heavily by software design, creating tests based on the specifications before actually creating the implementation often aid and offer guidance to the project, as well as guaranteeing the requirements from the start.

When designing this project, each step (pull-request) will be validated against the specifications and design rules (when applicable) to make sure no regressions are introduced and that modifications did not cause unforeseen side-effects.

### Features

Minimum functional requirements include:

- User-selectable constant voltage
- Constant current limiting

Additional features may include:

- USB/Serial communication
- Bluetooth/Wifi communication
- Built-in user interface (front pannel with knobs and display)

### Specifications

|Description|Range|Units|
|---|---|---|
|Output voltage|0 - 12|V|
|Output voltage resolution|10|mV|
|Output current|0 - 1|A|
|Output current resolution|100|mA|

> Based on [Dave Jone's EEVBlog µSupply project](https://www.eevblog.com/projects/usupply/)
