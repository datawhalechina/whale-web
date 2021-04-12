<template>
  <v-container fluid fill-height>
    <v-layout align-center
              justify-space-between
              row
              class="login">
      <!-- login form -->
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
                :rules="[rules.required, rules.email]"
                label="Email"
                required
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
              ></v-text-field>
              <v-btn
                :disabled="!valid"
                block
                color="blue"
                class="mr-4"
                @click="submit"
              >
                LogIn
              </v-btn>
              <div class="or">OR</div>
              <v-btn
                block
                class="mr-4"
                link
                to="/register"
              >
                Register
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<style lang="scss" scoped>
.login {
  background-image: url(../assets/bluewhale.svg);
  background-size: fill;
  background-position: 50%;
}
.or {
  display: flex;
  align-items: center;
  position: relative;
  margin: 20px 0;
  color: #DADADA;
  &:after {
    content: '';
    height: 1px;
    width: 100%;
    margin-left: 5px;
    background: #DADADA;

  }
  &:before {
    content: '';
    height: 1px;
    width: 100%;
    margin-right: 5px;
    background: #DADADA;
  }
}
</style>>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    valid: true,
    email: '',
    password: '',
    showPassword: false,
    rules: {
      required: (value) => !!value || 'Required.',
      email: (value) => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return pattern.test(value) || 'Invalid e-mail.';
      },
    },
  }),
  components: {
  },
  created() {
    this.$axios.options('/login'); // get csrf cookie
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
      this.$axios.post('/login', {
        email: this.email,
        password: this.password,
      }).then((data) => {
        this.setUserInfo(data.data);
        this.$router.push({ name: 'articles' });
      }).catch(() => {
        this.showSnack({
          text: 'Failed to sign in, please check your credentials.',
          color: 'error',
        });
      });
    },
    handleKeyup(e) {
      if (
        e.key === 'Enter'
        && this.email
        && this.password
        && this.$route.path === '/login'
      ) {
        this.submit();
      }
    },
  },
};
</script>
