import json,jsonpointer

with open('../rs-report-data/01.scrape.json') as f:
    scrape_data = json.load(f)

def extract_first(data, pointer_array, pointer_value):
    try:
        return jsonpointer.resolve_pointer(data, '/' + pointer_array + '/0/' + pointer_value)
    except Exception as e:
        return None

def extract_n(data, pointer_array):
    try:
        return len(jsonpointer.resolve_pointer(data, '/' + pointer_array + '/0'))
    except Exception as e:
        return None

summaries = []
for scrape_entry in scrape_data:
    summary = {
        #'executable_example_n': parse_somef['n'](scrape_entry['somef']['executable_example']),
        'somef_version': scrape_entry['somef']['somef_provenance']['somef_version'],

        # scrape_entry[]'code_repository']
        # 'license_name': extract_first(scrape_entry, 'somef/license', 'result/name'),
         'executable_example_n': extract_n(scrape_entry, 'somef/executable_example')
    }
    summaries.append(summary)

print(summaries)
