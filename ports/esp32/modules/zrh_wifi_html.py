from micropython import const

html = const('''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0,user-scalable=no"
    />
    <title>WiFi配置</title>
    <style>
      :root {
        --bg-color: #fff;
        --main-color: #3388ff;
      }
      html,
      body {
        padding: 10px;
        margin: 0;
        background-color: var(--bg-color);
        font-size: 16px;
        overflow: hidden;
      }
      * {
        box-sizing: border-box;
      }
      #ssid,
      #password {
        height: 45px;
        line-height: 45px;
        outline-color: var(--main-color);
        padding: 4px;
        font-size: 16px;
        border-style: solid;
        border-color: #dfdfdf;
        outline: none;
      }
      input:focus {
        border-color: var(--main-color);
      }
      .btn-send {
        display: flex;
        padding: 10px 30px;
        background-color: var(--main-color);
        border: 1px solid;
        color: #fff;
        margin: 0 auto;
      }

      .item {
        display: flex;
        flex-direction: column;
        row-gap: 6px;
        margin-bottom: 6px;
      }
      .item-inline {
        display: flex;
        row-gap: 8px;
        margin-bottom: 20px;
        align-items: center;
      }
      #input-show-password {
        cursor: pointer;
        width: 20px;
        height: 20px;
      }
      .label-show-password {
        cursor: pointer;
        user-select: none;
        outline: none;
      }
    </style>
  </head>
  <body>
    <form id="form">
      <div class="item ssid">
        <label for="ssid">SSID</label>
        <input type="text" id="ssid" />
      </div>
      <div class="item password">
        <label for="password">密码</label>
        <input type="password" id="password" autocomplete />
      </div>
      <div class="item-inline">
        <input
          type="checkbox"
          id="input-show-password"
          onclick="onShowPassword(this.checked)"
        />
        <label class="label-show-password" for="input-show-password">
          显示密码
        </label>
      </div>
      <button id="btn-send" class="btn-send">
        <span id="btn-text">确认</span>
      </button>
    </form>
    <script>
      document.getElementById('form').addEventListener('submit', (e) => {
        e.preventDefault();
        onSend();
      });
      async function onSend() {
        const ssid = document.getElementById('ssid');
        const password = document.getElementById('password');
        const ssidValue = ssid.value;
        const passwordValue = password.value;

        if (!ssidValue) {
          alert('请输入SSID');
          return;
        }
        if (!passwordValue) {
          alert('请输入密码');
          return;
        }
        const btnSend = document.getElementById('btn-send');
        const btnText = document.getElementById('btn-text');
        if (btnSend.classList.contains('btn-loading')) {
          console.log('请求中...');
          return;
        }
        ssid.setAttribute('disabled', 'disabled');
        password.setAttribute('disabled', 'disabled');
        btnText.innerText = '正在提交';
        btnSend.classList.toggle('btn-loading');
        console.log(ssidValue, passwordValue);
        const res = await fetch(`/setWifi`, {
          method: 'POST',
          body: JSON.stringify({
            ssid: ssidValue,
            password: passwordValue,
          }),
        });
        const json = await res.json();

        ssid.removeAttribute('disabled');
        password.removeAttribute('disabled');
        btnSend.classList.toggle('btn-loading');
        btnText.innerText = '确认';

        if (json.isSuccess) {
          ssid.value = '';
          password.value = '';
          onToast(json.message);
        } else {
          alert('配置成功');
        }
      }
      function onShowPassword(e) {
        document.getElementById('password').setAttribute('type', e ? 'text' : 'password');}
    </script>
  </body>
</html>
''')
