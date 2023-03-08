tags_in_div_content = ['div', 'top-matter', 'md', 'media', 'entry', 'comment', 'form']

schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer",
      "minimum": 0
    }
  },
  "required": ["name"]
}



object_1 = {
    'website':'reddit',
    'site_ratio':0.8,
    'schema':{},
    'html_tags':[]
}