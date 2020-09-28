import sys
import datetime
import argparse
from hamutils.adif import ADIReader
from hamutils.cabrillo import CabrilloWriter

parser = argparse.ArgumentParser(description="Convert an ADIF file to Cabrillo.")
parser.add_argument("--contest", required=True, help="contest name")
parser.add_argument("--input-file", required=True, help="input file name")
parser.add_argument("--callsign", required=True, help="operator callsign")
args = parser.parse_args()

f = open(args.input_file, "r", encoding="ascii")
adi = ADIReader(f)
output = getattr(sys.stdout, "buffer", sys.stdout)
cbr = CabrilloWriter(output)
cbr.write_tag("CALLSIGN", args.callsign)
cbr.write_tags(category="SINGLE-OP ALL LOW", contest=args.contest)
for qso in adi:
    cbr.add_qso(
        qso["freq"],
        qso["mode"],
        qso["datetime_on"],
        qso["station_callsign"],
        qso["rst_sent"],
        qso["stx_string"],
        qso["call"],
        qso["rst_rcvd"],
        qso["srx_string"],
    )
cbr.close()
