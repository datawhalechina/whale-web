<template>
  <v-app>
    <v-app-bar dense app>
      <v-img
          alt="Logo"
          class="shrink mr-2"
          contain
          src="../assets/bluewhale.png"
          max-height="48"
        />
      <v-btn plain to="/articles">
        <v-icon>mdi-newspaper-variant-multiple</v-icon>
        最新
      </v-btn>
      <v-btn plain to="/qa">
        <v-icon>mdi-frequently-asked-questions</v-icon>
        问答
      </v-btn>
      <v-btn plain to="/subscribes">
        <v-icon>mdi-table-heart</v-icon>
        关注
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon to="/articles/editor/add" v-show="isAuthenticated">
        <v-icon>mdi-book-plus</v-icon>
      </v-btn>
      <v-menu
        open-on-click
        left bottom
        offset-y>
          <template v-slot:activator="{ on, attrs }">
          <!-- <v-btn icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-incognito</v-icon>
          </v-btn> -->
          <v-avatar
            v-bind="attrs"
            v-on="on">
            <img v-if="isAuthenticated"
              :src="gravatar"
            >
            <v-icon v-else>
              mdi-incognito
            </v-icon>
          </v-avatar>
        </template>
        <v-list dense nav>
          <v-list-item to="/login" v-if="!isAuthenticated">
            <v-list-item-icon>
              <v-icon>mdi-login</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              Login
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-else @click="signOutUser">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              Logout
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <Snackbar/>
      <router-view></router-view>
    </v-main>
    <v-footer app>
      <v-col
        class="text-center"
        cols="12"
      >
        Datawhale - Bluewhale
        <v-icon color="pink" small>mdi-heart</v-icon>
        {{ new Date().getFullYear() }}
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import Snackbar from '@/components/Snackbar';

export default {
  name: 'Layout',
  components: {
    Snackbar,
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'user/isAuthenticated',
      gravatar: 'user/gravatar',
    }),
  },
  methods: {
    ...mapActions({
      setUserInfo: 'user/setUserInfo',
      showSnack: 'snackbar/showSnack',
    }),
    signOutUser() {
      this.$store.dispatch('user/signOutUser', this);
    },
  },
  created() {
    this.$store.dispatch('user/fetchUserInfo', this);
  },
};
</script>
