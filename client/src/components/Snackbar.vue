<template>
  <div name="snackbars">
    <v-snackbar
      v-model="show" :color="color" :timeout="timeout" top right
      outlined>
      {{ text }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="grey darken-3"
          text v-bind="attrs" @click="show = false"
          icon>
          <v-icon>mdi-close-circle</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      color: '',
      text: '',
      timeout: -1,
      unsubscribe: null,
    };
  },
  created() {
    this.unsubscribe = this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'snackbar/SHOW_MESSAGE') {
        this.text = state.snackbar.text;
        this.color = state.snackbar.color;
        this.timeout = state.snackbar.timeout;
        this.show = true;
      }
    });
  },
  beforeDestroy() {
    this.unsubscribe && this.unsubscribe();
  },
};
</script>
