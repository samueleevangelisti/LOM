function login() {
  postRequest('/login', {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value
  })
    .then((response) => {
      console.log(response);
      location.href = '/dashboard';
    })
    .catch((error) => {
      console.log(error);
    });
}
