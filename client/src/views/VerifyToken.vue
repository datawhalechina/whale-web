<template>
  <v-app>
    <v-main>
      <Snackbar/>
      <v-container fluid fill-height>
        <v-layout align-center
                  justify-space-between
                  row>
          <v-flex xs12
                  md4
                  offset-4
                  class="flex-box">
            <v-card class="elevation-1 login-card">
              <v-card-title>Bluewhale</v-card-title>
              <v-card-text>
                <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                  @submit.prevent
                >
                  <v-text-field
                    v-model="email"
                    readonly
                    append-icon="mdi-email"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :rules="[rules.required]"
                    label="Password"
                    required
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                    tabindex="1"
                  ></v-text-field>
                  <v-text-field
                    v-model="password2"
                    :rules="[rules.required]"
                    label="Confirm Password"
                    required
                    :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword2 ? 'text' : 'password'"
                    @click:append="showPassword2 = !showPassword2"
                    tabindex="2"
                  ></v-text-field>
                  <v-btn
                    :disabled="!valid"
                    block
                    color="blue"
                    class="mr-4"
                    @click="submit"
                  >
                    Register
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss" scoped>
main {
  background-image: url(../assets/bluewhale.svg);
  background-size: fill;
  background-position: 50%;
}
</style>>

<script>
import { mapActions } from 'vuex';
import Snackbar from '@/components/Snackbar';

export default {
  data: () => ({
    valid: true,
    email: '',
    password: '',
    password2: '',
    showPassword: false,
    showPassword2: false,
    token: '',
    rules: {
      required: (value) => !!value || 'Required.',
      email: (value) => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return pattern.test(value) || 'Invalid e-mail.';
      },
    },
  }),
  components: {
    Snackbar,
  },
  created() {
    this.$axios.options('/login'); // get csrf cookie
    const { token } = this.$route.params;
    this.token = token;
    this.$axios.get(`/verify/${token}`).then((data) => {
      this.email = data.data;
    }).catch(() => {
      this.showSnack({
        text: 'Invalid token or token has been expired.',
        color: 'error',
        timeout: 5000,
      });
    });
  },
  mounted() {
    document.addEventListener('keyup', this.handleKeyup);
  },
  beforeDestroy() {
    document.removeEventListener('keyup', this.handleKeyup);
  },
  methods: {
    ...mapActions({
      setUserInfo: 'user/setUserInfo',
      showSnack: 'snackbar/showSnack',
    }),
    submit() {
      if (!this.$refs.form.validate()) {
        return;
      }
      if (this.password !== this.password2) {
        this.showSnack({
          text: 'Password does not match.',
          color: 'error',
        });
        return;
      }
      this.$axios.post('/register', {
        token: this.token,
        password: this.password,
      }).then((data) => {
        this.setUserInfo(data.data);
        this.$router.push({ name: 'articles' });
      }).catch((e) => {
        let message = 'Failed to register.';
        if (e.response && e.response.data && e.response.data.message) {
          if (this._.isArray(e.response.data.message)) {
            message = this._.join(e.response.data.message, '');
          } else {
            message = e.response.data.message;
          }
        }
        this.showSnack({
          text: message,
          color: 'error',
          timeout: 5000,
        });
      });
    },
    handleKeyup(e) {
      if (
        e.key === 'Enter'
        && this.token
        && this.password
      ) {
        this.submit();
      }
    },
  },
};
</script>
