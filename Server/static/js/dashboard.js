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
      alert(JSON.stringify(error));
    });
});

function showContent(element) {
  document.getElementById('main').setHTML('');
  document.getElementById('main').appendChild(element);
}

function showDevices() {
  getRequest('/dashboard/devices')
    .then((response) => {
      console.log(response);
      if(response.success) {
        let table;
        let tr;
        let th;
        let td;
        let button;
        table = document.createElement('table');
        tr = document.createElement('tr');
        th = document.createElement('th');
        th.innerHTML = 'id';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'name';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'body';
        tr.appendChild(th);
        table.appendChild(tr);
        response.data.forEach((device) => {
          tr = document.createElement('tr');
          device.forEach((column) => {
            td = document.createElement('td');
            td.innerHTML = column;
            tr.appendChild(td);
          });
          table.appendChild(tr);
        });
        showContent(table);
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(JSON.stringify(error));
    });
}

function showUsers() {
  getRequest('/dashboard/users')
    .then((response) => {
      console.log(response);
      if(response.success) {
        let table;
        let tr;
        let th;
        let td;
        let button;
        table = document.createElement('table');
        tr = document.createElement('tr');
        th = document.createElement('th');
        th.innerHTML = 'id';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'level';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'username';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'pin';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'rfid';
        tr.appendChild(th);
        th = document.createElement('th');
        tr.appendChild(th);
        table.appendChild(tr);
        response.data.forEach((user) => {
          tr = document.createElement('tr');
          user.forEach((column, index) => {
            td = document.createElement('td');
            td.innerHTML = column;
            switch(index) {
              case 3:
                button = document.createElement('button');
                if(column) {
                  button.id = 'delete-pin-button';
                  button.innerHTML = 'delete';
                  button.addEventListener('click', () => {
                    deletePin(user[0]);
                  });
                } else {
                  button.innerHTML = 'create';
                  button.addEventListener('click', () => {
                    createPin(user[0]);
                  });
                }
                td.appendChild(button);
                break;
              case 4:
                if(column) {
                  button = document.createElement('button');
                  button.id = 'delete-rfid-button';
                  button.innerHTML = 'delete';
                  button.addEventListener('click', () => {
                      (user[0]);
                  });
                  td.appendChild(button);
                }
                break;
            }
            tr.appendChild(td);
          });
          td = document.createElement('td');
          button = document.createElement('button');
          button.innerHTML = 'delete';
          button.addEventListener('click', () => {
            deleteUser(user[0]);
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
      alert(JSON.stringify(error));
    });
}

function createPin(id) {
  patchRequest(`/dashboard/users/${encodeURIComponent(id)}`, {
    pin: '0'
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
      alert(JSON.stringify(error));
    });
}

function deletePin(id) {
  patchRequest(`/dashboard/users/${encodeURIComponent(id)}`, {
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
      alert(JSON.stringify(error));
    });
}

function deleteRfid(id) {
  patchRequest(`/dashboard/users/${encodeURIComponent(id)}`, {
    rfid: ''
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
      alert(JSON.stringify(error));
    });
}

function deleteUser(id) {
  deleteRequest(`/dashboard/users/${encodeURIComponent(id)}`)
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
      alert(JSON.stringify(error));
    });
}
