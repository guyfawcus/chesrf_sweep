# chesrf_sweep

This script is a wrapper around the [`hackrf_sweep`](https://github.com/mossmann/hackrf/wiki/hackrf_sweep) tool, it takes the output and formats it for use in Wireless Workbench.
The output is a simple .CSV file that contains the frequency (in MHz), and the corresponding power (in dB).

    606.250,-50.00
    606.500,-45.00

To use this script, you'll need:
* A HackRF! (https://greatscottgadgets.com/hackrf/one/)
* Python 3 (https://www.python.org/downloads/)
* The HackRF tools (https://github.com/mossmann/hackrf/wiki/Operating-System-Tips)
* This script (https://raw.githubusercontent.com/guyfawcus/chesrf_sweep/master/chesrf_sweep.py)
