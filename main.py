import v1.generate as generate

import v2.process as process
import v2.generate as pdf_report


def mtd_report_v1():
    print('Generating Mock PDF Report, V1.')
    time(2)
    print('File will be exported to v1/mock-report.pdf')
    generate.mock_report()


env_path = 'v2/env/dummy.env' # specify the correct path relative to the main file

def mtd_report_v2(path):
    print('Generating Mock PDF Report using realistic links from a .env file, V2.')
    time(2)
    print('File will be exported to v2/mock-report.pdf')
    process.configure_data(path)
    amazon_df, shopify_df, tacos_df, engagement_df = process.for_report()
    pdf_report.generate(amazon_df, shopify_df, tacos_df, engagement_df)

## uncomment below functions to generate2  ##
#mtd_report_v1()
#mtd_report_v2(env_path)