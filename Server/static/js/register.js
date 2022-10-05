function register() {
  let username = document.getElementById('username').value;
  if(!username) {
    alert('Empty username');
    return;
  }
  let password = document.getElementById('password').value;
  if(!password) {
    alert('Empty password');
    return;
  }
  let password2 = document.getElementById('password2').value;
  if(password2 != password) {
    alert('Password mismatch');
    return;
  }
  postRequest('/users', {
    username: username,
    password: password
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        location.href = '/login';
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(JSON.sringify(error));
    });
}

function login() {
  location.href = '/login';
}
