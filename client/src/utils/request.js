import axios from 'axios';

const { CancelToken } = axios;

// create an axios instance
const service = axios.create({
  baseURL: '/api/v1', // url = base url + request url
  timeout: 30000,
  withCredentials: true, // send cookies when cross-domain requests
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

// request interceptor
service.interceptors.request.use(
  (config) => {
    if (config.cancelable) {
      const source = { cancelId: config.cancelId };
      config.cancelToken = new CancelToken((c) => {
        source.cancel = c;
      });
      window.$_cancelToken.push(source);
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// response interceptor
service.interceptors.response.use(
  (response) => response.data,
);

export default service;
