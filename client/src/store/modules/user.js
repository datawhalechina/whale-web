import md5 from 'md5';

function getInitialUserInfo() {
  return {
    id: -1,
    email: '',
    phone: '',
    nickname: '',
    date_joined: '',
    last_login: '',
    last_login_ip: '',
    description: '',
    groups: [],
  };
}

// getters
const getters = {
  isAuthenticated(state) {
    return state.id > 0;
  },
  gravatar(state) {
    let hash = '00000000000000000000000000000000';
    if (state.email) {
      hash = md5(state.email.trim().toLowerCase());
    }
    return `https://www.gravatar.com/avatar/${hash}?d=retro`;
  },
};

// actions
const actions = {
  setUserInfo({ commit }, userInfo) {
    return new Promise((resolve) => {
      commit('SET_USER_INFO', userInfo);
      resolve();
    });
  },
  fetchUserInfo({ commit }, vm) {
    vm.$axios.get('/me').then((data) => {
      commit('SET_USER_INFO', data.data);
    }).catch(() => {
      commit('RESET_USER_INFO');
    });
  },
  signOutUser({ commit }, vm) {
    vm.$axios.post('/logout').finally(() => {
      commit('RESET_USER_INFO');
    });
  },
};

// mutations
const mutations = {
  SET_USER_INFO: (state, userInfo) => {
    Object.assign(state, userInfo);
  },
  RESET_USER_INFO: (state) => {
    Object.assign(state, getInitialUserInfo());
  },
};

export default {
  namespaced: true,
  state: getInitialUserInfo(),
  getters,
  actions,
  mutations,
};
