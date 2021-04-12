<template>
  <v-container fluid fill-height>
    <v-layout align-center
              justify-space-between
              row
              class="login">
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
              <v-btn
                :disabled="!valid"
                block
                color="blue"
                class="mr-4"
                @click="submit"
              >
                Send Verification
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
</style>>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    valid: true,
    email: '',
    sending: false,
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
      if (this.sending) return;
      this.sending = true;
      this.$axios.post('/send-verification', {
        email: this.email,
      }).then(() => {
        this.showSnack({
          text: 'Please verify email by clicking link that has been sent to your email.',
          color: 'success',
        });
      }).catch((e) => {
        let message = 'Failed to send verification to your email.';
        if (e.response && e.response.data && e.response.data.message) {
          message = e.response.data.message;
        }
        this.showSnack({
          text: message,
          color: 'error',
        });
      }).finally(() => {
        this.sending = false;
      });
    },
    handleKeyup(e) {
      if (
        e.key === 'Enter'
        && this.email
        && this.$route.path === '/register'
      ) {
        this.submit();
      }
    },
  },
};
</script>
