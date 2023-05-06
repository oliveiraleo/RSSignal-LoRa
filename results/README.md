## results folder

This folder contains the files with the output result of each step of the RSSignal framework. Each step has its own results saved on a different (sub)folder to avoid cluttering.

**Pattern:** Framework step -> Script/Module >> Output folder

- Preprocess the input [RSSignal 2nd step] -> [preprocess_input.sh](./../preprocess_input.sh) >> dataset-files
- Quantization [RSSignal 3rd step] -> [RSSI_to_binary.py](./../RSSI_to_binary.py) >> bit-sequence
- Index exchange (calculates the indexes to be discarded) [RSSignal 4th step] -> [discard_RSSI_values_step1.py](./../discard_RSSI_values_step1.py) >> discard
- Index exchange (erases the indexes discarded) [RSSignal 4th step] -> [discard_RSSI_values_step1.py](./../discard_RSSI_values_step3.py) >> keys
- Key reconciliation (encodes the data and generates the ecc bits) [RSSignal 5th step] -> [key_reconciliation_reed_solomon_step1.py](./../key_reconciliation_reed_solomon_step1.py) >> key-reconciliation
- Key reconciliation (reconciliates the data and ecc bits) [RSSignal 5th step] -> [key_reconciliation_reed_solomon_step3.py](./../key_reconciliation_reed_solomon_step3.py) >> key-after-reconciliation
- Privacy amplification [RSSignal 6th step] -> [rivacy_amplification_step1.py](./../privacy_amplification_step1.py) >> privacy-amplification-digest

**Note:** Changing the folder names and/or locations is easy, it's usually only a matter of changing the path on scripts' main function.