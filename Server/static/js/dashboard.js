window.addEventListener('DOMContentLoaded', () => {
  getRequest('/dashboard/sections')
    .then((response) => {
      console.log(response);
      if(response.data.is_devices) {
        document.getElementById('devices-button').removeAttribute('disabled');
      }
      if(response.data.is_users) {
        document.getElementById('users-button').removeAttribute('disabled');
      }
    });
});

function showContent(html) {
  document.getElementById('main').setHTML(html);
}

function showDevices() {
  getRequest('/dashboard/devices')
    .then((response) => {
      console.log(response);
      showContent(`<table><tr><td>device</td></tr>${response.data.map((device) => {
        return `<tr>${device.map((column) => {
          return `<td>${column}</td>`;
        }).join('')}</tr>`;
      }).join('')}<table>`);
    })
}

function showUsers() {
  getRequest('/dashboard/users')
    .then((response) => {
      console.log(response);
      showContent(`<table><tr><td>id</td><td>level</td><td>username</td><td>pin</td><td>rfid</td></tr>${response.data.map((user) => {
        return `<tr>${user.map((column) => {
          return `<td>${column}</td>`;
        }).join('')}</tr>`;
      }).join('')}<table>`);
    });
}
