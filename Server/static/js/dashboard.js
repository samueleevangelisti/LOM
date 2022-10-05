globalDeviceArr = [];



window.addEventListener('DOMContentLoaded', () => {
  getRequest('/dashboard/sections')
    .then((response) => {
      console.log(response);
      if(response.success) {
        if(response.data.is_devices) {
          document.getElementById('devices-button').removeAttribute('disabled');
        }
        if(response.data.is_users) {
          document.getElementById('users-button').removeAttribute('disabled');
        }
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
});

function showContent(element) {
  document.getElementById('main').setHTML('');
  document.getElementById('main').appendChild(element);
}

function showDevices() {
  document.getElementById('add-device-div').removeAttribute('hidden')
  getRequest('/devices')
    .then((response) => {
      console.log(response);
      if(response.success) {
        globalDeviceArr = response.data;
        let columnArr = ['id', 'name', 'url', 'body']
        let table;
        let tr;
        let th;
        let td;
        let pre;
        let button;
        table = document.createElement('table');
        tr = document.createElement('tr');
        for(let i = 0; i < columnArr.length; i++) {
          th = document.createElement('th');
          th.innerHTML = columnArr[i];
          tr.appendChild(th);
        }
        th = document.createElement('th');
        th.innerHTML = 'status';
        tr.appendChild(th);
        th = document.createElement('th');
        tr.appendChild(th);
        table.appendChild(tr);
        globalDeviceArr.forEach((device) => {
          tr = document.createElement('tr');
          for(let i = 0; i < columnArr.length; i++) {
            td = document.createElement('td');
            switch(columnArr[i]) {
              case 'body':
                pre = document.createElement('pre');
                pre.innerHTML = JSON.stringify(JSON.parse(device.body), null, 2);
                td.appendChild(pre);
                break;
              default:
                td.innerHTML = device[columnArr[i]];
                break;
            }
            tr.appendChild(td);
          }
          td = document.createElement('td');
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
          tr.appendChild(td);
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

        (function refreshAll(idArr, index = 0) {
          if(index < idArr.length) {
            refreshPromise(idArr[index])
              .finally(() => {
                refreshAll(idArr, index + 1);
              });
          }
        })(response.data.map((device) => {
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
  let bodyInput = document.getElementById('device-body');
  if(!nameInput.value) {
    alert('Empty name');
    return;
  }
  if(!urlInput.value) {
    alert('Empty url');
    return;
  }
  if(!bodyInput.value) {
    alert('Empty body');
    return;
  }
  try {
    JSON.parse(bodyInput.value);
  } catch(error) {
    alert('Invalid json in body');
    return;
  }
  postRequest('/devices', {
    name: nameInput.value,
    url: urlInput.value,
    body: bodyInput.value
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
      bodyInput.value = '';
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
          pre.innerHTML = JSON.stringify(response.data, null, 2);
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

function showUsers() {
  document.getElementById('add-device-div').setAttribute('hidden', '')
  getRequest('/users')
    .then((response) => {
      console.log(response);
      if(response.success) {
        let columnArr = ['id', 'username', 'pin', 'rfid', 'level', 'active']
        let table;
        let tr;
        let th;
        let td;
        let button;
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
        response.data.forEach((user) => {
          tr = document.createElement('tr');
          for(let i = 0; i < columnArr.length; i++) {
            td = document.createElement('td');
            switch(columnArr[i]) {
              case 'pin':
                td.innerHTML = user.pin;
                button = document.createElement('button');
                if(user.pin) {
                  button.id = 'delete-pin-button';
                  button.innerHTML = 'Delete';
                  button.addEventListener('click', () => {
                    deletePin(user.id);
                  });
                } else {
                  button.innerHTML = 'Create';
                  button.addEventListener('click', () => {
                    createPin(user.id);
                  });
                }
                td.appendChild(button);
                break;
              case 'rfid':
                if(user.rfid) {
                  td.innerHTML = user.rfid;
                  button = document.createElement('button');
                  button.id = 'delete-rfid-button';
                  button.innerHTML = 'Delete';
                  button.addEventListener('click', () => {
                    deleteRfid(user.id);
                  });
                  td.appendChild(button);
                }
                break;
              case 'active':
                button = document.createElement('button');
                if(user.active) {
                  button.innerHTML = 'Deactivate';
                  button.addEventListener('click', () => {
                    setActive(user.id, false);
                  });
                } else {
                  button.innerHTML = 'Activate';
                  button.addEventListener('click', () => {
                    setActive(user.id, true);
                  });
                }
                td.appendChild(button);
                break;
              default:
                td.innerHTML = user[columnArr[i]];
                break;
            }
            tr.appendChild(td);
          }
          td = document.createElement('td');
          button = document.createElement('button');
          button.innerHTML = 'Delete';
          button.addEventListener('click', () => {
            deleteUser(user.id);
          });
          td.appendChild(button);
          tr.appendChild(td);
          table.appendChild(tr);
        });
        showContent(table);
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function createPin(id) {
  patchRequest(`/users/${encodeURIComponent(id)}`, {
    pin: ''
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        showUsers();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function deletePin(id) {
  patchRequest(`/users/${encodeURIComponent(id)}`, {
    pin: null
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        showUsers();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function deleteRfid(id) {
  patchRequest(`/users/${encodeURIComponent(id)}`, {
    rfid: null
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        showUsers();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function setActive(id, active) {
  patchRequest(`/users/${encodeURIComponent(id)}`, {
    active: active
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        showUsers();
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}

function deleteUser(id) {
  deleteRequest(`/users/${encodeURIComponent(id)}`)
    .then((response) => {
      console.log(response);
      if(response.success) {
        if(id == retrieveId()) {
          location.href = '/login';
        } else {
          showUsers();
        }
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(error.toString());
    });
}
