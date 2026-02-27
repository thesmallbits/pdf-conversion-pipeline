| DETECTOR_BATCH_SIZE | RECOGNITION_BATCH_SIZE | success / failed | time | 
|----|------|------|----|
|4|512(default)|PPFP|42|
|36(Default)|120|PPFF|30|
|36(Default)|20|PPFF|30|


- Mostly failing on `fitjee_page_6_.pdf` with size 52.1KB but all are passing `fitjee_page_4.pdf` having larger size of 71.3KB ?? so most probably the memory isint being freed after each conversion


- max vram 4334
