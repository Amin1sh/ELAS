const elasUser = JSON.parse(sessionStorage.getItem('elas_user'));
let userToken = null;
if (elasUser) {
    userToken = elasUser.token
}

export default userToken;