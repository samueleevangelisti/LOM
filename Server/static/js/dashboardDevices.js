var globalDeviceArr = [];



function orderObj(obj) {
  let orderedObj = {};
  Object.keys(obj)
    .sort()
    .forEach((key) => {
      orderedObj[key] = obj[key]
    });
  return orderedObj;
}

function generateCommandLiArr(obj) {
  let li;
  let label;
  let ul;
  let input;
  let select;
  let option;
  return Object.keys(obj)
    .sort()
    .map((key) => {
      li = document.createElement('li');
      if(typeof(obj[key]) == 'object') {
        if(Array.isArray(obj[key])) {
          li.setAttribute('key', key);
          label = document.createElement('label');
          label.innerHTML = `${key}:`;
          li.appendChild(label);
          select = document.createElement('select');
          option = document.createElement('option');
          select.appendChild(option);
          obj[key].forEach((value) => {
            option = document.createElement('option');
            option.value = value;
            option.innerHTML = value;
            select.appendChild(option);
          });
          li.appendChild(select);
        } else {
          li.setAttribute('key', key);
          label = document.createElement('label');
          label.innerHTML = `${key}:`;
          li.appendChild(label);
          ul = document.createElement('ul');
          generateCommandLiArr(obj[key]).forEach((li) => {
            ul.appendChild(li);
          });
          li.appendChild(ul);
        }
      } else {
        switch(obj[key]) {
          case 'boolean':
            li.setAttribute('key', key);
            label = document.createElement('label');
            label.innerHTML = `${key}:`;
            li.appendChild(label);
            input = document.createElement('input');
            input.type = 'checkbox'
            li.appendChild(input);
            break;
          case 'number':
            li.setAttribute('key', key);
            label = document.createElement('label');
            label.innerHTML = `${key}:`;
            li.appendChild(label);
            input = document.createElement('input');
            input.type = 'number'
            li.appendChild(input);
            break;
          case 'string':
            li.setAttribute('key', key);
            label = document.createElement('label');
            label.innerHTML = `${key}:`;
            li.appendChild(label);
            input = document.createElement('input');
            input.type = 'text'
            li.appendChild(input);
            break;
          default:
            break;
        }
      }
      return li;
    });
}

function showDevices() {
  document.getElementById('add-device-div').removeAttribute('hidden')
  getRequest('/devices')
    .then((response) => {
      console.log(response);
      if(response.success) {
        globalDeviceArr = response.data;
        let columnArr = ['id', 'name', 'url', 'status', 'command']
        let table;
        let tr;
        let th;
        let td;
        let pre;
        let button;
        let ul;
        let li;
        table = document.createElement('table');
        tr = document.createElement('tr');
        for(let i = 0; i < columnArr.length; i++) {
          th = document.createElement('th');
          th.innerHTML = columnArr[i];
          tr.appendChild(th);
        }
        th = document.createElement('th');
        tr.appendChild(th);
        table.appendChild(tr);
        globalDeviceArr.forEach((device) => {
          tr = document.createElement('tr');
          for(let i = 0; i < columnArr.length; i++) {
            td = document.createElement('td');
            switch(columnArr[i]) {
              case 'status':
                pre = document.createElement('pre');
                pre.id = `${device.id}-status-pre`;
                pre.innerHTML = 'Loading...'
                td.appendChild(pre);
                button = document.createElement('button');
                button.innerHTML = 'Refresh';
                button.addEventListener('click', () => {
                  refresh(device.id);
                });
                td.appendChild(button);
                break;
              case 'command':
                ul = document.createElement('ul');
                ul.id = `${device.id}-command-ul`;
                li = document.createElement('li');
                li.innerHTML = 'Loading...';
                ul.appendChild(li);
                td.appendChild(ul);
                button = document.createElement('button');
                button.innerHTML = 'Apply';
                button.addEventListener('click', () => {
                  apply(device.id);
                });
                td.appendChild(button);
                break;
              default:
                td.innerHTML = device[columnArr[i]];
                break;
            }
            tr.appendChild(td);
          }
          td = document.createElement('td');
          button = document.createElement('button');
          button.innerHTML = 'Delete'
          button.addEventListener('click', () => {
            deleteDevice(device.id);
          });
          td.appendChild(button);
          tr.appendChild(td);
          table.appendChild(tr);
        });
        showContent(table);

        (function bodyAll(idArr, index=0) {
          if(index < idArr.length) {
            bodyPromise(idArr[index])
              .finally(() => {
                refreshPromise(idArr[index])
                  .finally(() => {
                    bodyAll(idArr, index + 1);
                  });
              });
          }
        })(globalDeviceArr.map((device) => {
          return device.id;
        }));

      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function addDevice() {
  let nameInput = document.getElementById('device-name');
  let urlInput = document.getElementById('device-url');
  if(!nameInput.value) {
    alert('Empty name');
    return;
  }
  if(!urlInput.value) {
    alert('Empty url');
    return;
  }
  postRequest('/devices', {
    name: nameInput.value,
    url: urlInput.value
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        showDevices();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    })
    .finally(() => {
      nameInput.value = '';
      urlInput.value = '';
    });
}

function bodyPromise(id) {
  return new Promise((resolve, reject) => {
    postRequest('/proxy', {
      url: `${globalDeviceArr.filter((device) => {
        return device.id == id;
      })[0].url}/info`,
      method: 'GET',
      data: null
    })
      .then((response) => {
        console.log(response);
        if(response.success) {
          let ul = document.getElementById(`${id}-command-ul`);
          ul.innerHTML = '';
          generateCommandLiArr(response.data).forEach((li) => {
            ul.appendChild(li);
          });
          resolve();
        } else {
          alert(response.error);
          reject();
        }
      })
      .catch((error) => {
        console.log(error);
        alert(error.toString());
        reject();
      });
  });
}

function refreshPromise(id) {
  return new Promise((resolve, reject) => {
    postRequest('/proxy', {
      url: globalDeviceArr.filter((device) => {
        return device.id == id;
      })[0].url,
      method: 'GET',
      data: null
    })
      .then((response) => {
        console.log(response);
        if(response.success) {
          let pre = document.getElementById(`${id}-status-pre`);
          pre.innerHTML = JSON.stringify(orderObj(response.data), null, 2);
          resolve();
        } else {
          alert(response.error);
          reject();
        }
      })
      .catch((error) => {
        console.log(error);
        alert(error.toString());
        reject();
      });
  });
}

function refresh(id) {
  document.getElementById(`${id}-status-pre`).innerHTML = 'Loading...';
  refreshPromise(id)
    .then()
    .catch();
}

function getCommandObj(ul) {
  let commandObj = {};
  ul.childNodes.forEach((li) => {
    switch(li.childNodes[1].tagName) {
      case 'UL':
        commandObj[li.getAttribute('key')] = getCommandObj(li.childNodes[1]);
        break;
      case 'INPUT':
        switch(li.childNodes[1].type) {
          case 'checkbox':
            commandObj[li.getAttribute('key')] = li.childNodes[1].checked;
            break;
          case 'number':
            commandObj[li.getAttribute('key')] = parseInt(li.childNodes[1].value) || null;
            break;
          case 'text':
            commandObj[li.getAttribute('key')] = li.childNodes[1].value || null;
            break;
          default:
            break;
        }
        break;
      case 'SELECT':
        commandObj[li.getAttribute('key')] = li.childNodes[1].value || null;
        break;
      default:
        break;
    }
  });
  return commandObj;
}

function apply(id) {
  postRequest('/proxy', {
    url: globalDeviceArr.filter((device) => {
      return device.id == id;
    })[0].url,
    method: 'PATCH',
    data: getCommandObj(document.getElementById(`${id}-command-ul`))
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        refresh(id);
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function deleteDevice(id) {
  deleteRequest(`/devices/${encodeURIComponent(id)}`)
    .then((response) => {
      console.log(response);
      if(response.success) {
        showDevices();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}
