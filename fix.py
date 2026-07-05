code = open('main.py').read()
code = code.replace('data = json.loads(r.content.decode("utf-8"))', 'data = r.json()')
open('main.py', 'w').write(code)
print('完了')

