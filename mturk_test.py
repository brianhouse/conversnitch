#!/usr/bin/env python3

import mturkcore

m = mturkcore.MechanicalTurk()
m.create_request("GetAccountBalance")
if m.is_valid():
    print(m.get_response_element("AvailableBalance"))
else:
    print("failed")
