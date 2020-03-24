from urllib.parse import unquote
from flask import Flask, request
app = Flask(__name__)

mainhtml = r'''
<html>
<head>
<script type="text/javascript">

function formSubmit() {
  function cback(){
    try{
      document.getElementById("decode").value = xml.response;
    }catch{
      document.getElementById("decode").value = '解混淆失败';
    }
  }
  function POST(url, headers, body){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('POST', url, true);
    Object.keys(headers).map((eachKey)=>{ xml.setRequestHeader(eachKey, headers[eachKey]); })
    xml.send(Object.keys(body).map((eachKey)=>{ return encodeURIComponent(eachKey) + '=' + encodeURIComponent(body[eachKey]); }).join('&'));
    return xml;
  }
  var info = document.getElementById("cotest").value
  var href = '/cotest'
  var xml = POST(href, {}, {'info':info})
}
</script>
</head>

<body>
<textarea id="cotest" size="20" style="width:1500px;height:700px"></textarea>
<br />
<button onclick="formSubmit()">尝试解混肴</button>
<br />
<textarea id="decode" size="20" style="width:1500px;height:700px"></textarea>
</body>
</html>
'''


@app.route('/')
def hello_world():
    return mainhtml

@app.route('/cotest', methods=['POST'])
def cotest():
    try:
        info = unquote(request.data.decode()).split('=',1)[-1]
        # 对传过来的参数处理后返回
        return info
    except:
        return "解码失败"

if __name__ == '__main__':
    app.run()