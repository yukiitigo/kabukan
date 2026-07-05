code = open('main.py').read()
old = '''            results = []
            for item in data.get("quotes", []):
                symbol = item.get("symbol", "")
                if symbol.endswith(".T"):
                    code = symbol.replace(".T", "")
                    name = item.get("longname") or item.get("shortname") or code
                    results.append({"code": code, "name": name})
            return {"results": results[:10]}'''
new = '''            results = []
            for item in data.get("quotes", []):
                symbol = item.get("symbol", "")
                if symbol.endswith(".T"):
                    code = symbol.replace(".T", "")
                    name = item.get("longname") or item.get("shortname") or item.get("dispSecIndFlag") or code
                    results.append({"code": code, "name": name})
            return {"results": results[:10]}'''
open('main.py', 'w').write(code.replace(old, new))
print('完了')

