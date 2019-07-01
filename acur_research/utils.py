import requests
from jsonschema import validate
import jsonschema
import json


def get_checkuuid_by_answ_id(survey_id, answer_id):
    schema_file_path = './acur_research/anketolog_full_report_schema.json'


    headers = {
        'X-Anketolog-ApiKey': 'dHo0dOiGB6wgJMA2fp4bI2utBbPnUr6vBwKuHXRAOqVJsh5AvG4qwNNUhYrfDuHT6dOhnGYJV8fcqlOSFYDu7rAYez0Vnd0er010',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = json.dumps({'survey_id': survey_id})
    response = requests.post('https://apiv2.anketolog.ru/survey/report/detail', headers=headers, data=data)

    if not response.ok:
        print('log error')
        return None

    try:
        resp_json = json.loads(response.content)
        validate(resp_json, schema=json.load(open(schema_file_path)))

    except (json.JSONDecodeError, jsonschema.exceptions.ValidationError):
        print('log error')
        return None

    curr_answers = [ans_elem for ans_elem in resp_json['answers'] if ans_elem['id'] == answer_id]
    if not curr_answers:
        print('log error')
        return None

    add_params = curr_answers[0]['additional_params']
    if not any(param_dict['name'] == 'check' for param_dict in add_params):
        print('log error')
        return None

    check_uuid = [param_dict['value'] for param_dict in add_params if param_dict['name'] == 'check'][0]
    return check_uuid