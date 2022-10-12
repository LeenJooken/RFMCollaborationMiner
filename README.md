# RFM Collaboration Miner

RFM Collaboration Miner is a project that extracts and constructs a collaboration network from an event log and calculates RFM values for both the resources and collaboration relationships.

Documentation on usage etc. will be provided soon.

## Supported input formats

Currently only extracted Git logs are supported. 

Parses a git log extracted by this commando in the git bash:
```python
git log --name-status --abbrev-commit --pretty=format:'%h,%an,%ad,%(trailers:key=Co-Authored-by,separator=%x2C,valueonly=TRUE)' --date=iso-local --diff-merges=c --no-renames > log.git
`````
    

## Supported output formats

The program constructs a collaboration network, which can be written to CSV files: 1 file for the collaboration relationships (edges), 1 file for the resources (nodes).

The node file has columns for: node ID, node label, summarized weight, recency value, frequency value, monetary value

The edge file has columns for: source node ID, target node ID, summarized weight, recency value, frequency value, monetary value


## Usage

```python
MainRFM.py -s log.git -nf nodes.csv -ef edges.csv
```
Possible arguments:

-s [git log source file to be read; must have extension .git]

-nf [file name of the output CSV file that will contain the nodes]

-ef [file name of the output CSV file that will contain the edges]


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT License

Copyright (c) [2021] [Leen Jooken]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
