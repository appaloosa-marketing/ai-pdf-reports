import v1.generate as generate

import time
def mtd_report_v1():
    print('Generating Mock PDF Report, V1.')
    time.sleep(2)
    print('File will be exported to v1/mock-report.pdf')
    generate.mock_report()

mtd_report_v1()