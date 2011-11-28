#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import obp_postbank_get_csv
import obp_import_post_bank
import libs.to_utf8.py



csv_file = os.path.join(obp_postbank_get_csv.csv_save_path,obp_postbank_get_csv.csv_files[0])

libs.to_utf8.main(csv_file)

# This no working right now! 

obp_import_post_bank.main(csv_file)







