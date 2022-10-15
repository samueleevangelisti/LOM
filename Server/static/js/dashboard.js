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
  document.getElementById('main').innerHTML = '';
  document.getElementById('main').appendChild(element);
}
