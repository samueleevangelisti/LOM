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
