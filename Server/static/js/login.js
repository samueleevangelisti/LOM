function login() {
  postRequest('/login', {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value
  })
    .then((response) => {
      console.log(response);
      if(response.success) {
        location.href = '/dashboard';
      } else {
        alert(response.error);
      }
    })
    .catch((error) => {
      console.log(error);
      alert(JSON.stringify(error));
    });
}
