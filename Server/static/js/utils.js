localStorageKey = {
  id: 'LOM_id',
  token: 'LOM_token'
};

function _storeElement(name, text) {
  localStorage.setItem(name, text);
}

function _retrieveElement(name) {
  return localStorage.getItem(name);
}

function _deleteElement(name) {
  localStorage.removeItem(name);
}

function storeId(id) {
  _storeElement(localStorageKey.id, id.toString());
}

function retrieveId() {
  idStr = _retrieveElement(localStorageKey.id);
  if(idStr) {
    return parseInt(idStr);
  } else {
    return null
  }
}

function storeToken(token) {
  _storeElement(localStorageKey.token, token);
}

function retrieveToken() {
  return _retrieveElement(localStorageKey.token);
}

////////////////////////////////////////////////////////////////////////////////

function getRequest(url) {
  return fetch(url, {
    method: 'GET',
    headers: {
      'Lom-Id': retrieveId(),
      'Lom-Token': retrieveToken()
    }
  })
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      if(response.id) {
        storeId(response.id);
      }
      if(response.token) {
        storeToken(response.token);
      }
      return response;
    });
}

function postRequest(url, bodyObj) {
  return fetch(url, {
    method: 'POST',
    headers: {
      'Lom-Id': retrieveId(),
      'Lom-Token': retrieveToken(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(bodyObj)
  })
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      if(response.id) {
        storeId(response.id);
      }
      if(response.token) {
        storeToken(response.token);
      }
      return response;
    });
}

function patchRequest(url, bodyObj) {
  return fetch(url, {
    method: 'PATCH',
    headers: {
      'Lom-Id': retrieveId(),
      'Lom-Token': retrieveToken(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(bodyObj)
  })
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      if(response.id) {
        storeId(response.id);
      }
      if(response.token) {
        storeToken(response.token);
      }
      return response;
    });
}
