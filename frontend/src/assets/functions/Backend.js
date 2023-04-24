import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL,
  responseType: 'json'
});

instance.interceptors.request.use(config => {
  const elasUser = JSON.parse(sessionStorage.getItem('elas_user'));
  const token = elasUser ? elasUser.token : null;
  config.headers['Authorization'] = `Bearer ${token}`;
  return config;
}, error => {
  return Promise.reject(error);
});

export default instance;
